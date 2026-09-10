#!/usr/bin/env cwl-runner


$namespaces:
  edam: http://edamontology.org/

$schemas:
- https://edamontology.org/EDAM.owl

baseCommand:
- python3
- code/compute_ndvi/compute_ndvi.py
class: CommandLineTool
cwlVersion: v1.2

inputs:
- default:
    class: File
    location: ../../data/reflectance.csv
  format: edam:format_3752
  id: reflectance
  inputBinding:
    prefix: --reflectance
  type: File
- default: ndvi.csv
  id: output
  inputBinding:
    prefix: --output
  type: string

outputs:
- format: edam:format_3752
  id: ndvi_csv
  outputBinding:
    glob: $(inputs.output)
  type: File

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entry:
      $include: ../../code/compute_ndvi/compute_ndvi.py
    entryname: code/compute_ndvi/compute_ndvi.py
- class: DockerRequirement
  dockerFile:
    $include: ../../Dockerfile
  dockerImageId: demo:v1.0.0
- class: InlineJavascriptRequirement
