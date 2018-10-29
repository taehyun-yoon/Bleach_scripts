Bleach script
==========

This repository contains scripts to process and analyze single photon pulses collected by TimeTagger.

Overview
--------

TimeTagger saves photon pulses in a file "tags.txt". These raw data are processed by process.c to show the arrival time of each pulse in microsecond. "analisys.py" analyze this preprocessed data to estimate the atom number inside the fiber or derive the Raman process rate from the change of atom number.

Dependencies
------------

- "process.c" is written in C

- All other codes are wrtten in python3

Description of files
--------------------

Non-Python files:

filename                     |  description
-----------------------------|------------------------------------------------------------------------------------
README.md                    |  Text file (markdown format) description of the project.

C files:

filename                     |  description
-----------------------------|------------------------------------------------------------------------------------
process.c                    |  convert raw data from TimeTagger to the microsecond unit

python files:

filename                     |  description
-----------------------------|------------------------------------------------------------------------------------
singleHist.py                |  Define a class SingleHist which makes histogram of data
readWrite.py                 |  Define a class ReadWrite which reads parameters values from file names
analysis.py                  |  Analyzed the pre-processed dat
