# Independent Research Project - clp22
## Project presentation
The project title is 'Machine learning downscaling of biofuel-driven land use change to a country-level'. 

The goal of this project is to offer a new statistical downscaling approach to downscaling Intergovernmental Panel on Climate Change (IPCC) regional value to country-level value. The program is accessible thanks to a user interface which allow to choose the parameters to run the downscaling method. 

This repository contains the code of a Python package that runs the downscaling model, notebooks to pre-process the IPCC and Eurostat datasets

## Datasets
Datasets needed to run the program are available [here](https://drive.google.com/drive/folders/1ZG0T_sTUrfcpj-HxLJAZwzoCPws_WMNe?usp=sharing)
Once the content downloaded, please place both folder as is in the '/data' folder of your local uploaded repository. 

* Only the content of the `/ipcc` and `/eurostat` folders are needed to run the `full_pipeline.ipynb` file.
* The zip file is required to run the `ipcc_preprocessing.ipynb` file.
* Only the content of the `/eurostat` folder is needed to run the `eurostat_preprocessing.ipynb` notebook.
* The file `Surface-area-in-square-kilometres.csv` is needed in the `Analysis.ipynb` notebook.

## Project organisation

The project is organized as followed: 

```
├── .github
├── Notebooks
├── biofuel-downscaling
├── data
├── info
├── reports
├── LICENSE.md
├── README.md
├── environment.yml
├── requirement.txt

```

* The `.github` folder contains files to run github workflow
* The `Notebooks` folder contains Jupyter Notebook that can be run separetely from the Python package 'biofuel-downscaling'. Four notebooks are available, two to pre-process the IPCC and Eurostat data, one allows to run the full pipeline and one with the code for results analysis. 
* The `biofuel-downscaling` folder is the python package that contains all module and the main.py file to run the program and the user interface.
* The `info` folder contains files giving information about the project
* The `reports` folder contains all the reports required during the project

## User guide
This project uses conda as a package manager. You should have conda configured on your local machine before installing the project. 

```bash
conda -V
``` 

**Installation and configuration**

* To install the project, first clone the repository: 

```bash
git clone https://github.com/ese-msc-2022/irp-clp22.git
```

* Go to the git repository on you local computer: 

```bash
cd irp-clp22
```

* Then configure the conda environment:

```bash
conda env create -f environment.yml
```

* Activate the `clp22-irp` conda environment:

```bash
conda activate clp22-irp
```

* Once you have finished using the tool, you can deactivate the conda environment using the following command:

```bash
conda deactivate
```

**Launch the interface**

Go to the `biofuel-downscaling` folder:
```bash
cd biofuel-downscaling
```

```bash
streamlit run main.py
```

Then go on the local host URL given. 

**Run Jupyter Notebooks**

Go to the root of the project:
```bash
cd irp-clp22
```

Launch Jupyter Notebook:
```bash
jupyter notebook
```

The notebooks are in the `Notebooks` folder.