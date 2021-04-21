# Drugs detail info
Scan openFDA and SEER.cancer.gov for drug details.  
FDA output is  the __exact__ match  
SEER output is the __most relevent__ match

## Installation 
### Prerequisites
+ authorization token from https://api.seer.cancer.gov/new_account
+ authorization token from https://open.fda.gov/apis/authentication  

save tokens   
`export SEER_API_KEY="{your_seer_token}"`  
`export FDA_API_KEY="{your_openfda_token}"`

### Installation
clone repository   
`git clone https://github.com/getzlab/drug_info_portal.git`  
change directory  
`cd drug_info_portal`  
set virtual environment  
`python3 -m venv .venv`  
activate environment  
`source .venv/bin/activate`  
load required packages   
`pip install -r requirements.txt`

## Usage
`python drug_info.py -i drugs.list -o drugs_info`
### Output
Two tab-separated files with the detailed info about drug 
### Options
+ `-i` `--input` File with drug names one drug per line
+ `-o` `--output` Prefix for the output files
### Example
`python drug_info.py -i example.txt -o example`

### TODO
+ add search in active ingridients
+ remove suffiex from the drug names
