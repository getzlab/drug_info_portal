# Project Title
Scan openFDA and SEER.cancer.gov for drug details.  
FDA output is  the __exact__ match  
SEER output is the most __relevent__ match

## Instalation 
### Prerequisites
+ authoritation token from https://api.seer.cancer.gov/new_account
+ authoritation token from https://open.fda.gov/apis/authentication
save tokens   
`export SEER_API_KEY="{your_seer_token}"`  
`export FDA_API_KEY="{your_openfda_token}"`

### Instalaiton
clone repository   
`git clone https://github.com/getzlab/drug_info_portal.git`  
change directory  
`cd drug_info_portal`  
set virual enviroment  
`python3 -m venv .venv`  
activate enviroment  
`source .venv/bin/activate`  
load requared packages   
`pip install -r requirements.txt`

## Usage
`python drug_info.py -i drugs.list -o drugs_info`
### Output
Two tab-separated files with the detailed info about drug 
### Options
+ `-i` `--input` File with drugs name one drug per line
+ `-o` `--output` Prefix for the output files
### Example
`python drug_info.py -i example.txt -o example`
`

### TODO
+ add search based on active ingridient
+ remove suffiex from the drug names