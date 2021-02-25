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

