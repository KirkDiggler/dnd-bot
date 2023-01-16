# Overview
These classes are internal models that are distinct for a given api. These files are specific for loading the dnd5eapi.co api data

# Description
These classes take in a dict and populate themselves. When a key is meant to be another class the init function will determine which class to load and load it. Each class here implements a to_model() function that coverts to the outward facing model. 