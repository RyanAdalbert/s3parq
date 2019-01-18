# Dev Guide

## Running Scripts

This project uses the idea of having basic (mostly) scripts to do tasks like testing, building, and serving applications - this idea was taken from https://github.com/github/scripts-to-rule-them-all. These scripts live in the /script directory and MUST be executed from the base directory of this repository.

## Getting Started
### Configurations 
    **Why?** 
    All pipelines need configurations. These range from the name of the client to the order of transformations to be applied. 
  
    We manage these configurations via a configuration application, which in turn stores them in an RDMBS. To acces these configurations you use the [Configurations module](../core/models/configuration.py)
