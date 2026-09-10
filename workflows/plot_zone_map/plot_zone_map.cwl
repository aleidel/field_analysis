#!/usr/bin/env cwl-runner


$namespaces:
  edam: http://edamontology.org/

$schemas:
- https://edamontology.org/EDAM.owl

baseCommand:
- python3
- code/plot_zone_map/plot_zone_map.py
class: CommandLineTool
cwlVersion: v1.2

inputs:
- default:
    class: File
    location: ../../ndvi.csv
  format: edam:format_3752
  id: ndvi
  inputBinding:
    prefix: --ndvi
  type: File
- default:
    class: File
    location: ../../fertility.csv
  format: edam:format_3752
  id: fertility
  inputBinding:
    prefix: --fertility
  type: File
- default: Field Management Zones
  id: title
  inputBinding:
    prefix: --title
  type: string
- default: zone_map.png
  id: output
  inputBinding:
    prefix: --output
  type: string

outputs:
- format: edam:format_3603
  id: zone_map_png
  outputBinding:
    glob: $(inputs.output)
  type: File

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entry:
      $include: ../../code/plot_zone_map/plot_zone_map.py
    entryname: code/plot_zone_map/plot_zone_map.py
- class: DockerRequirement
  dockerFile:
    $include: ../../Dockerfile
  dockerImageId: demo:v1.0.0
- class: InlineJavascriptRequirement
