# Pyseis
## Functional Requirements

### Abstract Description

The data analysis workflow is designed to facilitate the translation and validation of seismological data analysis components from the R programming language to Python. This workflow ensures that the translated components are functionally equivalent to their original counterparts by comparing the outputs from both implementations. After the UML diagram abstract description of each step in the workflow is given:

### UML Activity Diagram

![Activity Diagram](ActivityDiagram.png)


### Component Selection
Identify and select specific components from the existing `eseis` package, which are not currently available in Python.

### Translation to Python
Translate the selected R components into Python, ensuring that the functionality and logic of the original components are preserved. For details on which components each member is responsible for, see the [Task Distribution](#task-distribution) section.

### Unit Testing
Conduct unit testing on the translated Python components to verify their correctness and ensure they perform as expected.

### Output Generation
Generate outputs using both the translated Python components and the original R components. 

### Output Comparison
Compare the outputs generated from the Python implementations and R to check for consistency and accuracy.

### Validation Decision
Evaluate the outputs from Python with R:
- **If the outputs are valid**: Go to the Analyze step indicating that the Python components are functionally equivalent to the original R components.
- **If the outputs are not valid**: Debug and reiterate from translate step.

### Debug and Reiterate
If discrepancies are found during the output comparison, debug the translated Python components. This involves analyzing the differences, correcting any issues, and repeating the translation and validation steps until consistency is achieved.

### Analyze Data
Present the outputs from both the Python and R side-by-side in a Jupyter Notebook (.ipynb file).



## Component Analysis
In this section, we identify and select specific components from the existing eseis package, which are not currently available in Python. The table below lists these components, detailing their operations, inputs, outputs, and implementation. 

| Component         | Operation                                                        | Input(s)                                                                                                                           | Output(s)                                               | Implementation                              |
| ----------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------- |
| fmi_inversion     | Invert fluvial data set based on reference spectra catalogue     | reference list, seismic dataset, number of cores                                                                                   | list containing the inversion results                   | Available in R package (eseis), to be translated to Python    |
| fmi_parameters    | Create reference model reference parameter catalogue             | ground, river, and topographical parameters                                                                                       | list with model reference parameters                    | Available in R package (eseis), to be translated to Python    |
| fmi_spectra       | Create reference model spectra catalogue                         | model parameters, number of cores                                                                                                 | list containing input parameters and calculated spectra | Available in R package (eseis), to be translated to Python    |
| spatial_distance  | Calculate topography-corrected distances for seismic waves       | stations coordinates, DEM, options for topography correction, maps, interstation distances, area of interest, verbose flag         | list object with distance maps and station distance matrix | Available in R package (eseis), to be translated to Python       |
| spatial_migrate   | Migrate signals of a seismic event through a grid of locations   | seismic signals, inter-station distances, distance maps, SNR, velocity, sampling period, normalise option, verbose flag            | spatialGridDataFrame with Gaussian probability density  | Available in R package (eseis), to be translated to Python       |
| spatial_amplitude | Locate the source of a seismic event by modelling amplitude      | seismic signals, coupling factors, distance maps, area of interest, velocity, quality factor, frequency, source amplitude, verbose flag | raster object with location output metrics              | Available in R package (eseis), to be translated to Python       |
| spatial_clip      | Clip values of spatial data                                      | SpatRaster data, quantile, replacement value, normalise option                                                                    | SpatRaster object with clipped values                   | Available in R package (eseis), to be translated to Python      |
| spatial_convert   | Convert coordinates between reference systems                    | coordinates, input reference system, output reference system                                                                      | numeric data frame with converted coordinates           | Available in R package (eseis), to be translated to Python      |
| spatial_pmax      | Get most likely source location                                  | SpatRaster data set with source location estimates                                                                                | data frame with coordinates of the most likely source location(s) | Available in R package (eseis), to be translated to Python      |
| spatial_track     | Track a spatially mobile seismic source                          | seismic signals, coupling efficiency, time window, distance maps, area of interest, velocity, quality factor, frequency, CPUs, verbose flag | list object with summarising statistics of the fits     | Available in R package (eseis), to be translated to Python       |
| model_bedload     | Model the seismic spectrum due to bedload transport in rivers    | grain-size distribution, sediment parameters, fluid flow parameters, frequency range, distance to source, reference frequency, quality factor, Rayleigh wave parameters | eseis object containing the modelled spectrum           | Available in R package (eseis), to be translated to Python       |
| model_turbulence  | Model the seismic spectrum due to hydraulic turbulence           | sediment parameters, fluid flow parameters, frequency range, distance to source, reference frequency, quality factor, Rayleigh wave parameters | eseis object containing the modelled spectrum           | Available in R package (eseis), to be translated to Python       |

### Task Distribution
Each team member will be responsible for translating specific components from R to Python. The components are divided among the members as follows:


<table border="1">
  <tr>
    <th>Member</th>
    <th>Components Worked On</th>
    <th>Steps Involved</th>
  </tr>
  <tr>
    <td>Frieder</td>
    <td>fmi_inversion, fmi_parameters, fmi_spectra</td>
    <td rowspan="4">
      1. Translation <br> 
      2. Unit Testing <br> 
      3. Integration Testing <br> 
      4. Output Comparison <br>
  </tr>
  <tr>
    <td>Niaz</td>
    <td>spatial_distance, spatial_migrate, spatial_amplitude</td>
  </tr>
  <tr>
    <td>Lamia</td>
    <td>spatial_clip, spatial_convert, spatial_pmax</td>
  </tr>
  <tr>
    <td>Shahriar</td>
    <td>spatial_track, model_bedload, model_turbulence</td>
  </tr>
</table>




## Non-Functional Requirements
1. **Performance**
   - The package should handle large datasets efficiently.
   - The processes should be optimized for speed.
2. **Usability**
   - The package should have a clear and concise documentation.
   - The tool should be user-friendly.
3. **Scalability**
   - The package should be able to scale with increasing data sizes and complexity of analyses.
4. **Reliability**
   - The package should provide accurate and consistent results.
   - It should include error handling and logging mechanisms.
5. **Maintainability**
   - The code should follow best practices and be well-documented.
   - The package should be modular to facilitate updates and maintenance.
6. **Compatibility**
   - The package should be compatible with major operating systems (Windows, macOS, Linux).
   - It should support integration with other scientific Python libraries.
---