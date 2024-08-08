# Climate_Scenario_DataScience
This repository allows to calculate population statistics on the IPCC databases used for AR5, SR 1.5, and AR6.
## Installation
The installation requires `git`.

It is recommended to create an environment with Python 3.10. Using the package pyenv or pyenv-win, as shown below, allows to skip anaconda installation. Please follow these steps

'- open a terminal
'- install [pyenv](https://github.com/pyenv/pyenv) on MacOS/Linux or [pyenv-win](https://pyenv-win.github.io/pyenv-win/) on Windows
'- install Python
~~~
pyenv install 3.10
pyenv shell 3.10
python -m pip install pipx
python -m pipx ensurepath
~~~

'- create an environment and activate it
~~~
python3 -m venv env
~~~
'- activate the environment, as shwon below for Linux/MacOS/Windows

~~~
venv/bin/activate
~~~

~~~
venv/bin/activate
~~~

~~~
venv\Scripts\Activate.ps1
~~~

'- install the requirements running on the command line
~~~
pip install -r requirements.txt
~~~

## Running the model
The model can be run using an editor such as VsCode. The functions can be called running the main file pop_statistics.ipynb
## Data description
The main folder contains:
'- pop_statistics.ipynb runs statistics on population data 
'- extractor_ARs.ipynb contains functions to uploads and pre-process data from IPCC databases
'- UN_ARs.ipynb contains functions to uploads and pre-process data from UN databases

The `data` folder should be populated downloading the data from [zenodo](https://doi.org/10.5281/zenodo.8312059).

Once the zipped folder is downloaded, it should be unzipped and the content of the folder copied in the GitHub `data` folder.

At that point, the `data` folder will contain:
'- in `other_pop_data` files containing data from 
[World Bank](https://databank.worldbank.org/source/population-estimates-and-projections) (filename: `uscensus.xlsx`); 
[World Census](https://www.census.gov/data-tools/demo/idb/#/dashboard?COUNTRY_YEAR=2023&COUNTRY_YR_ANIM=2023) (filename: `worldbank.xlsx`); 
[Institute of Health Metrics and Evaluation](https://ghdx.healthdata.org/record/ihme-data/global-population-forecasts-2017-2100) (filename: `IHME.csv`).
'- in the folder `SSP` the Shared Socioeconomic drivers
[SSP](https://tntcat.iiasa.ac.at/SspDb/dsd?Action=htmlpage&page=10)
'- [UN](https://population.un.org/wpp/Download/Standard/Population/)
'- `IAMstat.xlsx`, an overview file of the scenario metadata published with the IPCC databases
'- `RFF.csv`, containing the population projections obtained by [Resources for the Future](https://zenodo.org/record/6016583#.Y42iFuzP2rP)
'- the remaining `.csv` files with names `AR6#`, `AR5#`, `IAMC15#` contain the IPCC scenarios assessed by the IPCC for preparing the IPCC assessment reports. They can be downloaded at [AR5](https://tntcat.iiasa.ac.at/AR5DB), [SR 1.5](https://data.ene.iiasa.ac.at/iamc-1.5c-explorer/#/downloads), and [AR6](https://data.ene.iiasa.ac.at/ar6/#/workspaces)

## Acknowledgments
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 101033173.

<img width="30px" src="https://github.com/sgiarols/Climate_Scenario_Data_Science/tree/main/images/EU_logo_high.png" alt="EU logo" />
![EU logo](https://github.com/sgiarols/Climate_Scenario_Data_Science/tree/main/images/EU_logo_high.png)
