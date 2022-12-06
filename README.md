# Research-Connections
## What it does:
It inputs a professor/researcher, looks them up on arxiv.org, and creates a visualization to show the professor's network based on who he/she/they have worked with as well as second-degree (or more) acquaintances.

## Setup
Install Anaconda/Miniconda if you haven't: https://conda.io/projects/conda/en/latest/user-guide/install/index.html

Run `conda env create -f environment.yml` to create the conda environment research-connections.

Run `conda activate research-connections` to activate that environment.

## How to use it:
`python connections.py authorname [-f field] [-b breadth] [-d depth]`

Required Parameters
 - authorname -- the name of the person you want to look up

Optional Parameters
 - field -- what field the author is from
 - breadth -- how many papers to look at per person
 - depth -- how many people deep to look

## Acknowledgements
Thank you to arXiv for use of its open access interoperability.
