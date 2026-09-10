#!/usr/bin/env cwl-runner


class: Workflow
cwlVersion: v1.2

inputs:
- default:
    class: File
    location: ../../data/reflectance.csv
  id: reflectance
  type: File

outputs: []
requirements:
- class: SubworkflowFeatureRequirement

steps:
- id: compute_ndvi
  in:
  - id: reflectance
    source: reflectance
  out:
  - ndvi_csv
  run: ../compute_ndvi/compute_ndvi.cwl
