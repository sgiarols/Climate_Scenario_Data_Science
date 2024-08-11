# %%
import pandas as pd
import numpy as np
import io
import itertools
import math
import os
np.seterr(invalid='ignore')

# %%
def nonharmARsextractor(folder: "str"):
    """Create a dataframe for each IPPC global database
    The assessment reports (ARs) databases are stored in csv files in the data folder
    with these names
    Receives
    folder: "str" with the name of the folder where the ARs are stored
    AR5 in "folder/AR5_Scenario_Database.csv",
    SR 1.5 "folder/IAMC15_Scenario_Database.csv",
    AR6 "folder/AR6_Scenarios_Database_World_v1.1.csv"
    Returns
    ar5: "pd.DataFrame" with the AR5 database with original period disaggregation
    ar15: "pd.DataFrame" with the SR 1.5 database with original period disaggregation
    ar6: "pd.DataFrame" with the AR6 database with original period disaggregation
    """

    non_year_col = ["Model", "Scenario", "Region", "Variable", "Unit"]
    years   =    ["2010",
                "2015",
                "2020",
                "2025", 
                "2030", 
                "2035", 
                "2040", 
                "2045", 
                "2050", 
                "2055", 
                "2060", 
                "2065", 
                "2070", 
                "2075", 
                "2080",
                "2085",
                "2090",
                "2095",
                "2100"]

    names = ["AR5", "SR15", "AR6"]
    def reading(file,non_year_col, years, name):
        data = pd.read_csv(file, encoding="latin1")
        oldcolumns = [s for s in data.columns]
        newcolumns = [str.title(s) for s in oldcolumns]
        data.columns = newcolumns
        data["Report"] = name
        newcolumns = ["Report"] + non_year_col + years
        data = data[newcolumns]
        return (data)
    
    files = [
            "AR5_Scenario_Database.csv",
            "IAMC15_Scenario_Database.csv",
            "AR6_Scenarios_Database_World_v1.1.csv"]

    files = [folder + "/" + file for file in files]
    ARsdata = []
    for f,file in enumerate(files):
        name = names[f]
        ARsdata.append(reading(file,non_year_col, years, name))

    varvalues=pd.DataFrame()
    var_list = ["Population",
                "GDP|PPP",
                "GDP|MER",
                "Emissions|CO2", 
                "Final Energy", 
                "Secondary Energy|Electricity", 
                "Primary Energy"]

    ar5=ARsdata[0]
    ar15=ARsdata[1]
    ar6=ARsdata[2]

    return ar5, ar15, ar6


def nonharmARregsextractor(folder: "str"):
    """Create a dataframe from AR6 IPPC regional database
    The assessment reports (ARs) databases are stored in csv files in the data folder
    with these names
    Receives
    folder: "str" with the name of the folder where the ARs are stored
    (e.g. "folder/AR")
    Files are:
        "AR6_Scenarios_Database_R5_regions_v1.1.csv",
        "AR6_Scenarios_Database_R6_regions_v1.1.csv",
        "AR6_Scenarios_Database_R10_regions_v1.1.csv"
    Returns
    ar6reg5HI: "pd.DataFrame" with the 5regionAR6 database with original period disaggregation
    ar6reg6HI: "pd.DataFrame" with the 6-region AR6 database with original period disaggregation
    ar6reg10HI: "pd.DataFrame" with the 10-region AR6 database with original period disaggregation
    """
    non_year_col = ["Model", "Scenario", "Region", "Variable", "Unit"]
    years   =    ["2010",
                "2015",
                "2020",
                "2025", 
                "2030", 
                "2035", 
                "2040", 
                "2045", 
                "2050", 
                "2055", 
                "2060", 
                "2065", 
                "2070", 
                "2075", 
                "2080",
                "2085",
                "2090",
                "2095",
                "2100"]

    names = ["AR6", "AR6", "AR6"]
    def reading(file,non_year_col, years, name):
        data = pd.read_csv(file, encoding="latin1")
        oldcolumns = [s for s in data.columns]
        newcolumns = [str.title(s) for s in oldcolumns]
        data.columns = newcolumns
        data["Report"] = name
        newcolumns = ["Report"] + non_year_col + years
        data = data[newcolumns]
        return (data)
    
    files = [
            "AR6_Scenarios_Database_R5_regions_v1.1.csv",
            "AR6_Scenarios_Database_R6_regions_v1.1.csv",
            "AR6_Scenarios_Database_R10_regions_v1.1.csv"]

    files = [folder + "/" + file for file in files]
            
    ARsdata = []
    for f,file in enumerate(files):
        name = names[f]
        ARsdata.append(reading(file,non_year_col, years, name))

    varvalues=pd.DataFrame()
    var_list = ["Population",
                "GDP|PPP",
                "GDP|MER",
                "Emissions|CO2", 
                "Final Energy", 
                "Secondary Energy|Electricity", 
                "Primary Energy"]

    ar6reg5HI=ARsdata[0]
    ar6reg6HI=ARsdata[1]
    ar6reg10HI=ARsdata[2]

    return ar6reg5HI, ar6reg6HI, ar6reg10HI


# %%
def readmeta(folder: "str"):
    """Create a dataframe with selected metadata:
    dataframe with number and name of projects by report
    plus dataframe with model scenarios by project
    Receives
    folder: "str" with the name of the folder where the ARs are stored
    Reuturns
    scenarios: "pd.DataFrame" with the number 
    othermeta[0]: name of projects in AR5
    othermeta[1]: name of projects in SR15
    othermeta[2]: name of projects in AR6"""
    file=os.path.join(folder, "IAMstat.xlsx")
    tabs=["allscen"]
    for tab in tabs:
        scenarios=pd.read_excel(file,tab)
    tabs = ["AR5modprj", "SR15modprj","AR6modprj"]
    dataset=["AR5", "SR 1.5", "AR6"]
    othermeta=[]
    for tab in tabs:
        data=pd.read_excel(file,tab)
        data.insert(loc=0, column="Report", value=dataset[tabs.index(tab)])
        othermeta.append(data)
    return (scenarios,othermeta[0], othermeta[1], othermeta[2])



