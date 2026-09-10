# Cheat-Sheet
This cheat sheet contains the commands that we executed during the workshop.

## Installation
[![GitHub Release](https://img.shields.io/github/v/release/fairagro/m4.4_sciwin_client)](https://github.com/fairagro/m4.4_sciwin_client/releases/latest)

The latest Version of `s4n` can be installed using the following command:
```
curl --proto '=https' --tlsv1.2 -LsSf https://fairagro.github.io/m4.4_sciwin_client/get_s4n.sh | sh 
```

The Installation can be verified using `s4n -V`.

## Creating the CommandLineTools

We start by creating a new `s4n` project:
```
s4n init
```

A CWL CommandLineTool describes a command that would usually be executed in the commandline. Later, each of the CommandLineTools will become a step in our workflow. 

### CommandLineTool for compute_ndvi

```
s4n create -c Dockerfile -t demo:v1.0.0 python3 code/compute_ndvi/compute_ndvi.py --reflectance data/reflectance.csv --output ndvi.csv
```

### CommandLineTool for compute_fertility

```
s4n create -c r-base:4.4.1 --run-container docker Rscript code/compute_fertility/compute_fertility.R --soil data/soil.csv --output fertility.csv
```
This time we execute the command with the `--run-container docker` flag because R is not installed on our machine and we want to use the provided Docker image to run it. 

### CommandLineTool for plot_zone_map

```
s4n create -c Dockerfile -t demo:v1.0.0 python3 code/plot_zone_map/plot_zone_map.py --ndvi ndvi.csv --fertility fertility.csv --title "Field Management Zones" --output zone_map.png
```

## Create a CWL workflow
The next step is to connect our CWL CommandLineTools into a workflow. For this, we can use `s4n connect <workflow-name> --from <source> --to <target>`

First, we add `reflectance` and `soil` as workflow inputs: 

```
s4n connect workflow --from reflectance --to compute_ndvi/reflectance
```
and: 
```
s4n connect workflow --from soil --to compute_fertility/soil
```

Then, we can add `zone_map_png` as output to our workflow: 

```
s4n connect workflow --from plot_zone_map/zone_map_png --to zone_map_png
```

Connections between the different workflow steps can be drawn using: 
```
s4n connect workflow --from compute_ndvi/reflectance --to plot_zone_map/ndvi
```
and:
```
s4n connect workflow --from compute_fertility/soil --to plot_zone_map/soil
```
(We could also use SciWIn-Studio to create the Workflow.)

Finally, once we have finished the workflow we can save it using: 
```
s4n save workflow
```

## Execute workflow

First, we create an `inputs.yml` file with the input files for our workflow: 
```
cd workflows/workflow
s4n execute make-template workflow.cwl > inputs.yml
```
Then, we can execute the workflow locally using: 
```
s4n execute --engine local workflow.cwl inputs.yml
```
