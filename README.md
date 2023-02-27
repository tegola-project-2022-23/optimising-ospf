# Optimising OSPF Weights to achieve balanced outgoing traffic at two gateways. 

This approach uses the existing OSPF protocol and by altering the link weights actively to achieve a load balanced outbound traffic at the 2 gateways. 

## Repository Architecture
- `old-files` contains an archive of old files that contain more information than the current files used. 
- `src` contains the pythons files intended to run the application. 
  - `Demand.py` This calculates the demand matrix. 
  - `History.py` This is used to collect data to confirm that the existing setup is unbalanced.
  - `hosts.json` This contains a list of itemIDs that correspond to interfaces we are interested in by host.
  - `Interface.py` This is a helper class used to represent an interface on a given host.
  - `Host.py` This is a helper class used to represent a Host with multiple interfaces.
- `testing-ipynb` contains preliminary testing files where concepts are tested before implemented into python files.

### To run:
- If you intend to modify and push to the repository, please do the following otherwise you may skip this.  
  - When running, you should ensure git does not track changes on the `config.ini` file where credentials are stored. You can do this by running `git update-index --assume-unchanged config.ini`. If you would like to modify the contents of the file and push to GitHub, you can allow git to track changes on the file again by running `git update-index --no-assume-unchanged config.ini`.  
  **PLEASE ENSURE CREDENTIALS ARE NOT PUSHED TO GITHUB**

#### Executing files
Files within `testing-ipynb` are self-contained and can be run using PyCharm or similar Jupyter notebook interpreters.   
`Demand.py` - This file can be executed using `python Demand.py` in the working directory of the `src` folder. Output of the program will be printed to console.  
`History.py` - This file can be executed using `python History.py` in the working directory of the `src` folder. Output of the program will be printed to console.  

## Thesis Plan

- Chapter 1 - Introduction
  - The problem - unbalanced outbound traffic at gateways.
  - The approach - reverse engineering ospf weights to achieve traffic engineering.
- Chapter 2 - Background
  - Tegola's history.
- Chapter 3 - Motivation
  - 
- Chapter 4 - Implementation
  - 
- Chapter 5 - Analysis
  - 