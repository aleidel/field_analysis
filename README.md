# Field Management Zones Workflow

The workflow computes the normalized difference vegetation index (NDVI) and soil fertility based on data from field plots. It then combines and classifies each cell and plots them. This repository is intended as a teaching example for a SciWIn workshop.

First, CWL CommandLineTools will be created for the three workflow steps using the
[SciWIn-Client (`s4n`)](https://github.com/fairagro/sciwin). Then, a CWL workflow is created using `s4n connect` and the [SciWIn-Studio](https://github.com/fairagro/sciwin_studio). Finally, an `inputs.yml` file is created and the workflow is executed. 

![the final resulting workflow](https://github.com/aleidel/field_analysis/blob/main/workflow.svg)
