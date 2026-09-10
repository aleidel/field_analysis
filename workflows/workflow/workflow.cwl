#!/usr/bin/env cwl-runner


class: Workflow
cwlVersion: v1.2

inputs:
- default:
    class: File
    location: ../../data/reflectance.csv
  id: reflectance
  type: File
- default:
    class: File
    location: ../../data/soil.csv
  id: soil
  type: File

outputs:
- id: zone_map_png
  outputSource: plot_zone_map/zone_map_png
  type: File

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
- id: compute_fertility
  in:
  - id: soil
    source: soil
  out:
  - fertility_csv
  run: ../compute_fertility/compute_fertility.cwl
- id: plot_zone_map
  in: []
  out:
  - zone_map_png
  run: ../plot_zone_map/plot_zone_map.cwl
