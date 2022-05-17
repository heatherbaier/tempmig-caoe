# Code for the Deep Learning & Migration Push-and-Pull Factors W&M CAOE Project


## Feature Extraction Replication Procedure

1. **Data Download**   
a. Navigate to https://international.ipums.org/international/mort_fert_mig.shtml  
b. Download the Mexico 2000 and Mexico 2010 Migration SPSS and Stata files and place them in a folder labeled 'data'  
c. Navigate to the data selection page and download data for the Mexico 2000 and 2010 censuses with the following variables:  

    | Type | 	Variable | 	Label                                                                    |
    |------|-------------|--------                                                                   |
    | H    | 	COUNTRY	 | Country                                                                   |
    | H    | 	YEAR	 | Year                                                                      |
    | H    | 	SAMPLE	 | IPUMS sample identifier                                                   |
    | H    | 	SERIAL	 | Household serial number                                                   |
    | H    | 	HHWT	 | Household weight                                                          |
    | H    | 	GEOLEV2	 | 2nd subnational geographic level, world [consistent boundaries over time] |  

    d. Replace any changed file paths and run the 'make_dataset.py' file


2. **Imagery Download**  
a. Install the pygee package using `pip install git+https://github.com/heatherbaier/pygee.git`