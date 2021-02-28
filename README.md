# Overview

This repository contains pre-processed data for [Manning JR, Lew TF, Li N, Sekuler R, Kahana MJ (2014) MAGELLAN: a cognitive map-based model of human wayfinding. *Journal of Experimental Psychology: General*, 143(3): 1314--1330](https://psycnet.apa.org/doi/10.1037/a0035542).  The raw experimental data may be downloaded [here](http://memory.psych.upenn.edu/files/pubs/MannEtal14a.data.tgz) (warning: large file!).

## Abstract
In an unfamiliar environment, searching for and navigating to a target requires that spatial information be acquired, stored, processed, and retrieved. In a study encompassing all of these processes, participants acted as taxicab drivers who learned to pick up and deliver passengers in a series of small virtual towns. We used data from these experiments to refine and validate MAGELLAN, a cognitive map–based model of spatial learning and wayfinding. MAGELLAN accounts for the shapes of participants’ spatial learning curves, which measure their experience-based improvement in navigational efficiency in unfamiliar environments. The model also predicts the ease (or difficulty) with which different environments are learned and, within a given environment, which landmarks will be easy (or difficult) to localize from memory. Using just 2 free parameters, MAGELLAN provides a useful account of how participants’ cognitive maps evolve over time with experience, and how participants use the information stored in their cognitive maps to navigate and explore efficiently. 

# Experiment description

A total of 108 participants played the role of "taxicab drivers" in a series of
virtual environments.  Within each environment, performed a series of 15
deliveries to a set of specific targets.  Each delivery comprised  "foraging"
phase and a "seeking" phase:
  - During the foraging phase, the participant drove freely for a short distance, until they were prompted with a notice saying that they had "picked up a passenger."  This ended the foraging phase and initiated the "seeking" phase.
  - During the seeking phase, the participant was given a "target" destination to drive their "passenger" to.
  
The order in which each participant encountered target destinations within a given environment was held constant across participants.  Every participant also encountered the same 8 environments, but the order in which the environments were visited was counterbalanced across participants, and across two testing sessions.  The environments varied in "expected difficulty," as predicted by the MAGELLAN model presented in the paper above:
  - *Easy*: environments A and E
  - *Medium-easy*: environments B and F
  - *Medium-difficult*: environments C and G
  - *Difficult*: environments D and H

Each environment was laid out on a 6 x 6 block square grid, with one landmark
(building) centered on each block.  Five of the squares in each environment held
"stores" that the passengers asked to be delivered to.  Each store was selected
as a target for a total of 3 deliveries.

# Contents

The repository is organized into two main folders:
- **data**: contains a single json file for each experimental participant
- **env**: contains a single json file for each virtual environment that participants navigated

# Recommended method for loading in data

The simplest way to load in data files is using the `pandas` Python library.  If
`'fname.json'` is the name of a given file, then its (participant or environment) data can be read in as follows:

```python
import pandas as pd
data = pd.read_json('fname.json')
```

# `magellan_loader`

Several convenience functions are provided in `magellan_loader.py`.  To use
them, you can call

```python
import magellan_loader as ml
```

## Functions for loading in or displaying information about *environments*

### `load_env`: load in information about the environment from its json file

Inputs:
- `fname`: file path to an environment's .json file, specified as a string

Outputs: 
- `env`: a pandas DataFrame describing the environment, with one row per
structure (specified in DataFrame's index) and the following columns:
  - `x`, `y`: the *x*-coordinate (or *y*-coordinate) of the given structure (in blocks).
  - `type`: either 'store' (if the structure is a potential target) or 'landmark' (if the structure is never used as a target).
  - `delivery 1`, `delivery 2`, `delivery 3`: for stores, specifies the first (or second, or third) delivery number (1-indexed) when the store is selected as a target.  For landmarks, these are set to `NaN`.

### `get_env_dims`: return the environment's width and height (in blocks)
Inputs:
- `env`: an environment's DataFrame

Outputs:
- `dims`: a tuple whose first element indicates the environment's width (in blocks) and whose second element indicates the environment's height (in blocks)

### `plot_environment`: generate a figure showing the layout of the environment
Note: stores are denoted by black circles; landmarks are denoted by gray squares; and intersections are denoted by gray dots.

Inputs:
- `env`: an environment's DataFrame

Outputs:
- `ax`: a `matplotlib` axis handle for the resulting figure

## Functions for loading in or displaying information about *behavioral data*

### `load_subj_data`: load in one subject's behavioral data from their json file

Inputs:
- `fname`: file path to an subject's .json file, specified as a string
- `freq`: optional argument specifying the sampling frequency of the data (default: use all available data)

Outputs:
- `data`: a pandas DataFrame whose rows denote data collected during a single timepoint.  Each row is indexed by the time the corresponding datapoint was collected.  The DataFrame has the following columns:
  - `x`, `y`: the subject's *x* and *y* position (in blocks)
  - `heading`: the subject's heading (in degrees; 0 degrees corresponds to "north" and 90 degrees corresponds to "west", etc.)
  - `mode`: 'forage' if the datapoint was collected while the subject was searching for a new passenger, or 'seek' if the datapoint was collected while the subject was delivering the passenger to a target (store)
  - `target`: the name of the passenger's destination while in 'seek' mode, specified as a string (set to `None` in 'forage' mode)
  - `subj`: the subject's unique identification code
  - `session`: zero-indexed session number
  - `env_num`: zero-index environment number (within the current session)
  - `env`: the current environment (corresponds to the json files for each environment)
  - `delivery`: zero-indexed delivery number (within the current environment)

### `get_conditions`: get the values of a set of columns in one or more subject DataFrames
Inputs:
- `data`: a pandas DataFrame with one subject's data, or several stacked DataFrames from multiple subjects
- `columns`: a string, list, or numpy array specifying the list of columns whose values should be read out (these must be a subset of the columns in the subject DataFrames)
- `unique`: an optional argument specifying whether or not to return the unique values for each column.  Default: `False` (return values, with potential repeats, in their original orders); if set to `True`, a sorted list of unique values from each column is returned

Outputs:
- The resulting values extracted from `data`

### `apply_by_condition`: apply a function to data corresponding to each combination of unique values from the given columns
Inputs:
- `data`: a pandas DataFrame with one subject's data, or several stacked DataFrames from multiple subjects
- `columns`: a string, list, or numpy array specifying the list of columns whose values should be read out (these must be a subset of the columns in the subject DataFrames)
- `f`: a function that takes a DataFrame (created from a subset of the rows in `data`) as input, and (optionally) produces any output
- `args`: a list of arguments that will be passed to `f` (the same values are passed to every call to `f`)
- `kwargs`: a dictionary of keyword arguments that will be passed to `f` (the same values are passed to every call to `f`)
  - Note: each call to `f` looks like: `f(data.loc[inds], *args, **kwargs)`, where `inds` is a binary array specifying which rows from `data` are from the current combination of conditions.

Outputs:
- `results`: a list of results (returned by each call to `f`)-- one for each unique combination of conditions across the specified columns

### `round_coords`: round each coordinate in a Series or DataFrame to the nearest block
Inputs:
- `data`: the object to process.  Must contain `x` and `y` fields or columns-- e.g. both `data['x']` and `data['y']` must return one or more to-be-rounded values.

Outputs:
- `rounded_data`: a copy of `data` with the coordinates in `x` and `y` rounded to the nearest integer.


### `plot_paths`: display behavioral data from each session, environment, and delivery from a single subject

The resulting figure contains one subplot per session and environment, each containing the foraging and delivery data:
- Foraging paths, denoted by `mode == 'forage'`, are colored (by delivery) using the [`crest` palette](https://seaborn.pydata.org/tutorial/color_palettes.html)
- Participant's seek paths, denoted by `mode == 'seek'`, are colored (by delivery) using the [`flare` palette](https://seaborn.pydata.org/tutorial/color_palettes.html)
- MAGELLAN's seek paths, denoted by `mode == 'autopilot'`, are colored (by delivery) using the [`seagreen` palette](https://seaborn.pydata.org/tutorial/color_palettes.html)

Inputs:
- `data`: a DataFrame containing one subject's data.  Note: the `subj` column is not checked; strange results may be generated if data from multiple subjects are included.
- `envs`: a dictionary whose keys are environment names and whose values are DataFrames for the corresponding environments.  If `root` is the current directory (containing this repository), then `envs` may be generated as follows:

```python
import magellan_loader as ml
from glob import glob as lsdir

root = 'magellan_data'
envs = {os.path.split(e)[-1].split('.')[0]: ml.load_env(e) for e in lsdir(os.path.join(root, 'env', '?.json'))}
```
- `scale`: optional argument specifying how large to draw each environment in the resulting figure (default: 4)

Outputs:
- `fig`, `ax`: handles to the matplotlib Figure and list of axes objects for the subplots, respectively


