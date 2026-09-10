#!/usr/bin/env cwl-runner


$namespaces:
  edam: http://edamontology.org/

$schemas:
- https://edamontology.org/EDAM.owl

baseCommand:
- Rscript
- code/compute_fertility/compute_fertility.R
class: CommandLineTool
cwlVersion: v1.2

inputs:
- default:
    class: File
    location: ../../data/soil.csv
  format: edam:format_3752
  id: soil
  inputBinding:
    prefix: --soil
  type: File
- default: fertility.csv
  id: output
  inputBinding:
    prefix: --output
  type: string

outputs:
- format: edam:format_3752
  id: fertility_csv
  outputBinding:
    glob: $(inputs.output)
  type: File

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entry:
      $include: ../../code/compute_fertility/compute_fertility.R
    entryname: code/compute_fertility/compute_fertility.R
- class: DockerRequirement
  dockerPull: r-base:4.4.1
- class: InlineJavascriptRequirement
