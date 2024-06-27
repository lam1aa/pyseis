import numpy as np
import rasterio
from rasterio import features
from shapely.geometry import Point, LineString

def spatial_distance(stations, dem, topography=True, maps=True, matrix=True, aoi=None, verbose=False):
    """
    Calculate topography-corrected distances for seismic waves.
    """
    # PART 0 - check input data
    if not isinstance(dem, rasterio.io.DatasetReader):
        raise ValueError("DEM must be a rasterio.io.DatasetReader object!")

    dem_array = dem.read(1)
    if np.isnan(dem_array).any():
        raise ValueError("DEM contains NaN values!")

    rows, cols = np.indices(dem_array.shape)
    xy_dem = np.column_stack(rasterio.transform.xy(dem.transform, rows, cols))

    print(f"DEM extent: {np.min(xy_dem[:, 0])}, {np.max(xy_dem[:, 0])}, {np.min(xy_dem[:, 1])}, {np.max(xy_dem[:, 1])}")
    print(f"Station coordinates:\n{stations}")

    if np.any(np.min(stations[:, 0]) < np.min(xy_dem[:, 0])) or \
       np.any(np.max(stations[:, 0]) > np.max(xy_dem[:, 0])) or \
       np.any(np.min(stations[:, 1]) < np.min(xy_dem[:, 1])) or \
       np.any(np.max(stations[:, 1]) > np.max(xy_dem[:, 1])):
        raise ValueError("Some station coordinates are outside DEM extent!")

    if aoi is None:
        aoi_ext = [np.min(xy_dem[:, 0]), np.max(xy_dem[:, 0]), np.min(xy_dem[:, 1]), np.max(xy_dem[:, 1])]
    else:
        aoi_ext = aoi

    if np.any(aoi_ext[0] < np.min(xy_dem[:, 0])) or \
       np.any(aoi_ext[1] > np.max(xy_dem[:, 0])) or \
       np.any(aoi_ext[2] < np.min(xy_dem[:, 1])) or \
       np.any(aoi_ext[3] > np.max(xy_dem[:, 1])):
        raise ValueError("AOI extent is beyond DEM extent!")

    # PART 1 - calculate distance maps
    if maps:
        aoi_array = np.zeros_like(dem_array)
        aoi_array[(xy_dem[:, 0] >= aoi_ext[0]) & (xy_dem[:, 0] <= aoi_ext[1]) &
                  (xy_dem[:, 1] >= aoi_ext[2]) & (xy_dem[:, 1] <= aoi_ext[3])] = 1

        maps = []
        for i in range(stations.shape[0]):
            if verbose:
                print(f"Processing map for station {i+1}")

            xy_stat = stations[i]
            distances = []
            for j in range(dem_array.shape[0]):
                for k in range(dem_array.shape[1]):
                    if aoi_array[j, k] == 1:
                        line_length = np.sqrt((xy_stat[0] - xy_dem[j * dem_array.shape[1] + k, 0]) ** 2 +
                                              (xy_stat[1] - xy_dem[j * dem_array.shape[1] + k, 1]) ** 2)
                        n_int = round(line_length / dem.res[0])
                        if n_int == 0:
                            n_int = 1

                        xy_pts = np.array([np.linspace(xy_stat[0], xy_dem[j * dem_array.shape[1] + k, 0], n_int),
                                           np.linspace(xy_stat[1], xy_dem[j * dem_array.shape[1] + k, 1], n_int)]).T

                        z_int = [dem_array[rasterio.transform.rowcol(dem.transform, xy_pt[0], xy_pt[1])] for xy_pt in xy_pts]

                        z_dir = np.linspace(z_int[0], z_int[-1], n_int)

                        if topography:
                            z_dir[z_dir > np.array(z_int)] = np.array(z_int)[z_dir > np.array(z_int)]

                        line_length = np.sqrt((xy_stat[0] - xy_dem[j * dem_array.shape[1] + k, 0]) ** 2 +
                                              (xy_stat[1] - xy_dem[j * dem_array.shape[1] + k, 1]) ** 2 +
                                              np.sum(np.abs(np.diff(z_dir))) ** 2)
                    else:
                        line_length = np.nan

                    distances.append(line_length)

            maps.append({'crs': dem.crs,
                         'ext': dem.bounds,
                         'res': dem.res,
                         'val': np.array(distances).reshape(dem_array.shape)})
    else:
        maps = [None] * stations.shape[0]

    if matrix:
        if verbose:
            print("Processing station distances")

        station_points = [Point(x, y) for x, y in stations]
        xyz_stat = [(x, y, dem_array[rasterio.transform.rowcol(dem.transform, x, y)]) for x, y in stations]

        M = np.zeros((stations.shape[0], stations.shape[0]))
        for i in range(len(xyz_stat)):
            dx_stations = [xyz_stat[j][0] - xyz_stat[i][0] for j in range(len(xyz_stat))]
            dy_stations = [xyz_stat[j][1] - xyz_stat[i][1] for j in range(len(xyz_stat))]
            dt_stations = [np.sqrt(dx ** 2 + dy ** 2) for dx, dy in zip(dx_stations, dy_stations)]

            for j in range(len(dt_stations)):
                n_int = round(dt_stations[j] / dem.res[0])
                if n_int == 0:
                    n_int = 1

                xy_pts = np.array([np.linspace(xyz_stat[i][0], xyz_stat[j][0], n_int),
                                   np.linspace(xyz_stat[i][1], xyz_stat[j][1], n_int)]).T

                z_int = [dem_array[rasterio.transform.rowcol(dem.transform, xy_pt[0], xy_pt[1])] for xy_pt in xy_pts]

                z_dir = np.linspace(z_int[0], z_int[-1], n_int)

                if topography:
                    z_dir[z_dir > np.array(z_int)] = np.array(z_int)[z_dir > np.array(z_int)]

                path_length = np.sum(np.sqrt(np.diff(xy_pts[:, 0]) ** 2 +
                                             np.diff(xy_pts[:, 1]) ** 2 +
                                             np.diff(z_dir) ** 2))

                M[i, j] = path_length
    else:
        M = None

    return {'maps': maps, 'matrix': M}


# Example
# if __name__ == "__main__":
#     # Example usage
#     import rasterio
#     from scipy.ndimage import gaussian_filter
#     import numpy as np

#     # Load example DEM
#     dem = gaussian_filter(np.fromfile('volcano.dat', sep="\n").reshape(99, 99), sigma=1)
#     dem = dem * 10
#     dem_dataset = rasterio.open('path/to/dem.tif', 'w', driver='GTiff',
#                                 height=dem.shape[0], width=dem.shape[1],
#                                 count=1, dtype=dem.dtype,
#                                 crs='+proj=utm +zone=10 +ellps=WGS84 +datum=WGS84 +units=m +no_defs',
#                                 transform=rasterio.transform.from_origin(0, 0, 10, 10))
#     dem_dataset.write(dem, 1)
#     dem_dataset.close()

#     # Define example stations
#     stations = np.array([[200, 220], [700, 700]])

#     # Calculate distance matrices and station distances
#     result = spatial_distance(stations, dem_dataset, verbose=True)

#     # Print station distance matrix
#     print(result['matrix'])