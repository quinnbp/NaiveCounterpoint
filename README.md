# CMUS130

A first and second species counterpoint generator. Requires midicsv. 

## Files

### cgen.py

Contains all functions to generate new first and second species counterpoint measures based on a parsed midicsv output file. 

### io.py

Contains all functions necessary to parse midicsv output files for the cgen functions, and process the output of cgen into 
a csvmidi input file. 

## Usage

Given a starting cantus firmus midi file, first generate a CSV file using midicsv, then run cgen.py with the CSV file as 
input, then run csvmidi on the resulting output file. The result will be a MIDI file of generated first or second species 
counterpoint, as specified. 

### Sample command

midicsv test.mid

python cgen.py test.csv

csvmidi test_counterpoint.csv


