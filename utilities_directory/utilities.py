import pandas as pd
import numpy as np
import os

import scipy.stats as stats
from scipy import special
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats.mstats import trim as trim


def transformUN(indata: pd.DataFrame, region: str, rename: bool):
    
    """Transforms United Nations (UN) data having horizontal series
    of years into a vertical series of years. It receives:
    indata: dataframe of probabilistic/deterministic UN data where
    data for each year is a new column
    region: name of the region selected
    rename: if True, raw labels would be changes into corresponding
    cumulative probability numbers
    select True for UN probability projections
    
    Returns: DataFrame with data for each years on rows
    with columns Population, Sccenario, Years"""

    ddata = pd.DataFrame(indata.loc[indata.IPCCRegion==region])

    if "Variant" in ddata.columns:
        ddata = ddata.drop("Variant", axis=1)

    columns = ddata.Scenario.to_list()

    wt = ddata.transpose()

    wt = wt.reset_index()

    wtt = wt[3:]
    
    wtt.columns = ["year"] + columns
    
    wnew = pd.DataFrame()
    for c, col in enumerate(columns):
        data = pd.DataFrame(wtt[wtt.columns[0]])
        data = data.rename(columns={data.columns[0]: "Year"})
        data["Population"] = wtt[wtt.columns[c+1]]
        data["Scenario"] = wtt.columns[c+1]
        wnew = pd.concat((wnew, data), axis=0)

    if rename:
        change={"Lower 80": "20", "Lower 95": "5", "Median": "50", "Upper 80": "80", "Upper 95": "95"}
        for ch in change.keys():
            wnew["Scenario"] = wnew["Scenario"].replace(ch, change[ch])
                    
    return (wnew)

def transformUNminmax(indata: pd.DataFrame, region: str, rename: bool, remove: list):

    """Transforms UN data in vertical series
    for scenarios with max and min population in 2100
    indata: dataframe of UN data where data for each year is a new column
    region: name of a region selected
    rename: if True, raw labels would be changes into corresponding cumulative probability numbers
    select True for UN probability projections
    remove: list of scenarios to remove as not proper scenarios
    
    Returns: DataFrame with """

    sel_series = [] #list to append the scenrios fulfilling requirements
    undata = transformUN(indata, region, rename)
    undata = undata.loc[~undata.Scenario.isin(remove)]
    max_2100 = pd.DataFrame(undata.loc[undata.Year==2100]["Population"]).max()
    sel_series.append(list(set(undata.loc[undata.Population==max_2100.values[0]]["Scenario"]))[0])
    min_2100 = pd.DataFrame(undata.loc[undata.Year==2100]["Population"]).min()
    sel_series.append(list(set(undata.loc[undata.Population==min_2100.values[0]]["Scenario"]))[0])
    undata = pd.DataFrame(undata.loc[undata.Scenario.isin(sel_series)])
    return undata, sel_series

def transformAR(indata: pd.DataFrame, region: str, dataset: str, threshold: tuple, years: list,
                variable: str, renamevariable: str):

    """Transforms indata from assessment reports
    (ARs) from having years in columns to having years in rows
    indata: dataframe of AR data where data for each year is a new column
    region: name of a region selected
    dataset: label to rename the series (e.g. AR6)
    threshold: ranges used to filter out the data using quantiles
    years: list of years to represent

    Returns: DataFrame of AR data with columns renamevariable (i.e. Population or GDP), Region, Series, Year, Unit, string Year
    """
    ar = pd.DataFrame(indata.loc[indata.Variable == variable])
    ared = pd.DataFrame(ar.loc[ar.Region == region])
    arnew = pd.DataFrame()
    for year in years:
        data = pd.DataFrame(np.vstack((ared[str(year)], ared["Unit"])).transpose(), columns = [renamevariable, "Unit"])
        data["Year"] = year
        data["sYear"] = str(year)
        low = data[renamevariable].quantile(threshold[0])
        high = data[renamevariable].quantile(threshold[1])
        data = pd.DataFrame(data.loc[data[renamevariable] >= low])
        data = pd.DataFrame(data.loc[data[renamevariable] < high])
        data["Series"] = dataset
        arnew = pd.concat((arnew,data))
    return arnew

def transformSSP(indata, region, years, variable):

    """Transforms Shared Socio-economic Pathways (SSP)
    data from years in horizontal series to years in vertical series
    indata: DataFrame with SSP population, following IPCC region conventions
    region: selected IPCC region
    years: selected years
    variable: Population

    Returns: DataFrame with columns sYears, Population, Model, Scenario
    """
    syears = [str(y) for y in years]

    if "Model" in indata.columns:
        columns = ["Model"] + ["Scenario"] + ["IPCCRegion"] + syears

        indata = indata.groupby(["Model", "Scenario","IPCCRegion"])[syears].sum().reset_index()

        wout = pd.DataFrame()
        models = list(set(indata.Model))
        scenarios = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5", "Historical Reference"]
        scenarios = [sc for sc in scenarios if sc in indata.Scenario.unique()]
        for model in models:
            for scenario in scenarios:
                wt = pd.DataFrame(indata.loc[(indata.IPCCRegion == region) 
                                & (indata.Model == model) 
                                & (indata.Scenario==scenario)])
                
                wt = wt[columns]
                wt.columns = ["Model", "Scenario", "IPCCRegion"] + syears
                wtt = wt.transpose()
                wts =  pd.DataFrame(wtt.loc[wtt.index.isin(syears)])
                wts.columns = [variable]
                wts["Model"] = model
                wts["Scenario"] = scenario
                wts["Year"] = years
                wout = pd.concat((wout, wts))
        wout = wout.reset_index()
        wout = wout.drop(columns=["index"])
        wout = wout[["Year", variable, "Model", "Scenario"]]
    else:
        columns = ["Scenario"] + ["IPCCRegion"] + syears

        indata = indata.groupby(["Scenario","IPCCRegion"])[syears].sum().reset_index()

        wout = pd.DataFrame()

        scenarios = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5", "Historical Reference"]
        scenarios = [sc for sc in scenarios if sc in indata.Scenario.unique()]

        for scenario in scenarios:
            wt = pd.DataFrame(indata.loc[(indata.IPCCRegion == region) 
                            & (indata.Scenario==scenario)])
            
            wt = wt[columns]
            wt.columns = ["Scenario", "IPCCRegion"] + syears
            wtt = wt.transpose()
            wts =  pd.DataFrame(wtt.loc[wtt.index.isin(syears)])
            wts.columns = [variable]
            wts["Scenario"] = scenario
            wts["Year"] = years
            wout = pd.concat((wout, wts))
        wout = wout.reset_index()
        wout = wout.drop(columns=["index"])
        wout = wout[["Year", variable, "Scenario"]]
    return (wout)

def readSSP(years: list):

    """Read Shared Socioeconomic Pathays data from folder data\SSP
    Receives:
    - years: list of years 
    Returns:
    SSPpop: A dataframe with SSP population
    SSPgdp: A dataframe with SSP GDP,
    SSPgroups: A dataframe with SSP population, grouped by MODEL and SCENARIO
    SSPgdpgroups: A dataframe with SSP GDP, grouped by MODEL and SCENARIO
    codes: dictionary with ISO code and country names
    scenarios: dictionary scenario names and variants
    """

    codefile  = "codes_and_country_names.csv" 
    sspfile = "SspDb_country_data_2013-06-12.csv"
    folder = r'data/SSP'
    incodes = pd.read_csv(os.path.join(folder, codefile))
    SSP = pd.read_csv(os.path.join(folder, sspfile))

    SSP["Country"] = SSP["REGION"]
    columns = SSP.columns[:5].to_list() +["Country"] + [str(y) for y in years]
    SSP = SSP[columns]
    regions = list(set(SSP["REGION"]))
    incodes.columns = ["ISO", "Country"]

    keys=list(incodes.ISO)
    values=list(incodes.Country)
    codes = {k:values[keys.index(k)] for k in keys}

    UNreg  =       ["Burundi",
                    "Comoros",
                    "Djibouti",
                    "Eritrea",
                    "Ethiopia",
                    "Kenya",
                    "Madagascar",
                    "Malawi",
                    "Mauritius",
                    "Mayotte",
                    "Mozambique",
                    "Réunion",
                    "Rwanda",
                    "Seychelles",
                    "Somalia",
                    "South Sudan",
                    "Uganda",
                    "United Republic of Tanzania",
                    "Zambia",
                    "Zimbabwe",
                    "Angola",
                    "Cameroon",
                    "Central African Republic",
                    "Chad",
                    "Congo",
                    "Democratic Republic of the Congo",
                    "Equatorial Guinea",
                    "Gabon",
                    "Sao Tome and Principe",
                    "Algeria",
                    "Egypt",
                    "Libya",
                    "Morocco",
                    "Sudan",
                    "Tunisia",
                    "Western Sahara",
                    "Botswana",
                    "Eswatini",
                    "Lesotho",
                    "Namibia",
                    "South Africa",
                    "Benin",
                    "Burkina Faso",
                    "Cabo Verde",
                    "Côte d'Ivoire",
                    "Gambia",
                    "Ghana",
                    "Guinea",
                    "Guinea-Bissau",
                    "Liberia",
                    "Mali",
                    "Mauritania",
                    "Niger",
                    "Nigeria",
                    "Saint Helena",
                    "Senegal",
                    "Sierra Leone",
                    "Togo",
                    "Kazakhstan",
                    "Kyrgyzstan",
                    "Tajikistan",
                    "Turkmenistan",
                    "Uzbekistan",
                    "China",
                    "China, Hong Kong SAR",
                    "China, Macao SAR",
                    "China, Taiwan Province of China",
                    "Dem. People's Republic of Korea",
                    "Japan",
                    "Mongolia",
                    "Republic of Korea",
                    "Afghanistan",
                    "Bangladesh",
                    "Bhutan",
                    "India",
                    "Iran (Islamic Republic of)",
                    "Maldives",
                    "Nepal",
                    "Pakistan",
                    "Sri Lanka",
                    "Brunei Darussalam",
                    "Cambodia",
                    "Indonesia",
                    "Lao People's Democratic Republic",
                    "Malaysia",
                    "Myanmar",
                    "Philippines",
                    "Singapore",
                    "Thailand",
                    "Timor-Leste",
                    "Viet Nam",
                    "Armenia",
                    "Azerbaijan",
                    "Bahrain",
                    "Cyprus",
                    "Georgia",
                    "Iraq",
                    "Israel",
                    "Jordan",
                    "Kuwait",
                    "Lebanon",
                    "Oman",
                    "Qatar",
                    "Saudi Arabia",
                    "State of Palestine",
                    "Syrian Arab Republic",
                    "Türkiye",
                    "United Arab Emirates",
                    "Yemen",
                    "Belarus",
                    "Bulgaria",
                    "Czechia",
                    "Hungary",
                    "Poland",
                    "Republic of Moldova",
                    "Romania",
                    "Russian Federation",
                    "Slovakia",
                    "Ukraine",
                    "Denmark",
                    "Estonia",
                    "Faroe Islands",
                    "Finland",
                    "Guernsey",
                    "Iceland",
                    "Ireland",
                    "Isle of Man",
                    "Jersey",
                    "Latvia",
                    "Lithuania",
                    "Norway",
                    "Sweden",
                    "United Kingdom",
                    "Albania",
                    "Andorra",
                    "Bosnia and Herzegovina",
                    "Croatia",
                    "Gibraltar",
                    "Greece",
                    "Holy See",
                    "Italy",
                    "Kosovo (under UNSC res. 1244)",
                    "Malta",
                    "Montenegro",
                    "North Macedonia",
                    "Portugal",
                    "San Marino",
                    "Serbia",
                    "Slovenia",
                    "Spain",
                    "Austria",
                    "Belgium",
                    "France",
                    "Germany",
                    "Liechtenstein",
                    "Luxembourg",
                    "Monaco",
                    "Netherlands",
                    "Switzerland",
                    "Anguilla",
                    "Antigua and Barbuda",
                    "Aruba",
                    "Bahamas",
                    "Barbados",
                    "Bonaire, Sint Eustatius and Saba",
                    "British Virgin Islands",
                    "Cayman Islands",
                    "Cuba",
                    "Curaçao",
                    "Dominica",
                    "Dominican Republic",
                    "Grenada",
                    "Guadeloupe",
                    "Haiti",
                    "Jamaica",
                    "Martinique",
                    "Montserrat",
                    "Puerto Rico",
                    "Saint Barthélemy",
                    "Saint Kitts and Nevis",
                    "Saint Lucia",
                    "Saint Martin (French part)",
                    "Saint Vincent and the Grenadines",
                    "Sint Maarten (Dutch part)",
                    "Trinidad and Tobago",
                    "Turks and Caicos Islands",
                    "United States Virgin Islands",
                    "Belize",
                    "Costa Rica",
                    "El Salvador",
                    "Guatemala",
                    "Honduras",
                    "Mexico",
                    "Nicaragua",
                    "Panama",
                    "Argentina",
                    "Bolivia (Plurinational State of)",
                    "Brazil",
                    "Chile",
                    "Colombia",
                    "Ecuador",
                    "Falkland Islands (Malvinas)",
                    "French Guiana",
                    "Guyana",
                    "Paraguay",
                    "Peru",
                    "Suriname",
                    "Uruguay",
                    "Venezuela (Bolivarian Republic of)",
                    "Bermuda",
                    "Canada",
                    "Greenland",
                    "Saint Pierre and Miquelon",
                    "United States of America",
                    "Australia",
                    "New Zealand",
                    "Fiji",
                    "New Caledonia",
                    "Papua New Guinea",
                    "Solomon Islands",
                    "Vanuatu",
                    "Guam",
                    "Kiribati",
                    "Marshall Islands",
                    "Micronesia (Fed. States of)",
                    "Nauru",
                    "Northern Mariana Islands",
                    "Palau",
                    "American Samoa",
                    "Cook Islands",
                    "French Polynesia",
                    "Niue",
                    "Samoa",
                    "Tokelau",
                    "Tonga",
                    "Tuvalu",
                    "Wallis and Futuna Islands",
                    ]


    checked = [name for name in list(codes.values()) if name not in UNreg]

    if len(checked) > 0:
        print (checked)
        print ("These countries are not mapped ", checked)


    scenarios = {"SSP3_v9_130115"	:	"SSP3"	,
                "SSP1_v9_130219"	:	"SSP1"	,
                "SSP2_v9_130219"	:	"SSP2"	,
                "SSP3_v9_130219"	:	"SSP3"	,
                "SSP4_v9_130219"	:	"SSP4"	,
                "SSP5_v9_130219"	:	"SSP5"	,
                "SSP1_v9_130325"	:	"SSP1"	,
                "SSP2_v9_130325"	:	"SSP2"	,
                "SSP3_v9_130325"	:	"SSP3"	,
                "SSP4_v9_130325"	:	"SSP4"	,
                "SSP5_v9_130325"	:	"SSP5"	,
                "SSP1_v9_130424"	:	"SSP1"	,
                "SSP2_v9_130424"	:	"SSP2"	,
                "SSP3_v9_130424"	:	"SSP3"	,
                "SSP4_v9_130424"	:	"SSP4"	,
                "SSP5_v9_130424"	:	"SSP5"	,
                "SSP5_v9_130115"	:	"SSP5"	,
                "SSP1_v9_130115"	:	"SSP1"	,
                "SSP2_v9_130115"	:	"SSP2"	,
                "SSP4_v9_130115"	:	"SSP4"	,
                "SSP4d_v9_130115"	:	"SSP4"	}

    # SSPpop: renaming scenarios
    SSPpop = pd.DataFrame( SSP.loc[SSP.VARIABLE == "Population"] )
    for o in scenarios.keys():
        SSPpop["SCENARIO"]  = SSPpop["SCENARIO"].replace(o, scenarios[o])
        SSPpop["SCENARIO"]  = SSPpop["SCENARIO"].replace(o, scenarios[o])
    SSPpop["REGION"] = SSPpop["REGION"].apply(lambda x: codes[x])

    # SSPgdp: renaming scenarios
    SSPgdp  = pd.DataFrame( SSP.loc[SSP.VARIABLE == "GDP|PPP"] )
    for o in scenarios.keys():
        SSPgdp["SCENARIO"]  = SSPgdp["SCENARIO"].replace(o, scenarios[o])
        SSPgdp["SCENARIO"]  = SSPgdp["SCENARIO"].replace(o, scenarios[o])
    SSPgdp["REGION"] = SSPgdp["REGION"].apply(lambda x: codes[x])

    SSPgroups = pd.DataFrame(SSPpop.groupby(["MODEL","SCENARIO"]).sum(numeric_only=True).reset_index())
    SSPgdpgroups  = pd.DataFrame(SSPgdp.groupby(["MODEL","SCENARIO"]).sum(numeric_only=True).reset_index())
    remove = "PIK GDP-32"
    SSPgroups = pd.DataFrame(SSPgroups.loc[SSPgroups.MODEL != remove])
    SSPgdpgroups = pd.DataFrame(SSPgdpgroups.loc[SSPgdpgroups.MODEL != remove])

    SSPgroups["IPCCRegion"] = "WORLD"
    SSPgdpgroups["IPCCRegion"] = "WORLD"
    SSPgroups = SSPgroups.rename(columns={"MODEL": "Model", "SCENARIO": "Scenario"})
    return (SSPpop, SSPgdp, SSPgroups, SSPgdpgroups, codes, scenarios)

def createsids():
    """Returns a dictionary with small island developing"""
    UNreg = ["Antigua and Barbuda",
            "Bahamas",
            "Barbados",
            "Belize",
            "Cabo Verde",
            "Comoros",
            "Cook Islands",
            "Cuba",
            "Dominica",
            "Dominican Republic",
            "Fiji",
            "Grenada",
            "Guinea-Bissau",
            "Guyana",
            "Haiti",
            "Jamaica",
            "Kiribati",
            "Maldives",
            "Marshall Islands",
            "Mauritius",
            "Micronesia (Fed. States of)",
            "Nauru",
            "Niue",
            "Palau",
            "Papua New Guinea",
            "Saint Kitts and Nevis",
            "Saint Lucia",
            "Saint Vincent and the Grenadines",
            "Samoa",
            "Sao Tome and Principe",
            "Seychelles",
            "Singapore",
            "Solomon Islands",
            "Suriname",
            "Timor-Leste",
            "Tonga",
            "Trinidad and Tobago",
            "Tuvalu",
            "Vanuatu",]

    return {"SIDs": UNreg}

def createldcs():
    """Returns a dictionary with least developing countries"""
    UNreg = ["Afghanistan",
            "Angola",
            "Bangladesh",
            "Benin",
            "Burkina Faso",
            "Burundi",
            "Cambodia",
            "Central African Republic",
            "Chad",
            "Comoros",
            "Democratic Republic of the Congo",
            "Djibouti",
            "Eritrea",
            "Ethiopia",
            "Gambia",
            "Guinea",
            "Guinea-Bissau",
            "Haiti",
            "Kiribati",
            "Lao People's Democratic Republic",
            "Lesotho",
            "Liberia",
            "Madagascar",
            "Malawi",
            "Mali",
            "Mauritania",
            "Mozambique",
            "Myanmar",
            "Nepal",
            "Niger",
            "Rwanda",
            "Sao Tome and Principe",
            "Senegal",
            "Sierra Leone",
            "Solomon Islands",
            "Somalia",
            "South Sudan",
            "Sudan",
            "Timor-Leste",
            "Togo",
            "Tuvalu",
            "Uganda",
            "United Republic of Tanzania",
            "Yemen",
            "Zambia",]

    return {"LDCs": UNreg}

def createlldcs():
    """Returns a dictionary with landlocked least developing countries""" 
    UNreg = ["Afghanistan",
            "Armenia",
            "Azerbaijan",
            "Bhutan",
            "Botswana",
            "Burkina Faso",
            "Burundi",
            "Central African Republic",
            "Chad",
            "Eswatini",
            "Ethiopia",
            "Kazakhstan",
            "Kyrgyzstan",
            "Lao People's Democratic Republic",
            "Lesotho",
            "Malawi",
            "Mali",
            "Mongolia",
            "Nepal",
            "Niger",
            "North Macedonia",
            "Paraguay",
            "Bolivia (Plurinational State of)",
            "Republic of Moldova",
            "Rwanda",
            "South Sudan",
            "Tajikistan",
            "Turkmenistan",
            "Uganda",
            "Uzbekistan",
            "Zambia",
            "Zimbabwe",]

    return {"LLDCs": UNreg}


def readSSPnew(years: list, selected_scenarios: list, region_dict: dict):

    """Read Shared Socioeconomic Pathays data from folder data\SSP
    Receives:
    - years: list of years 
    - selected_scenarios: list of chosen scenarios to represent
    - region_dict: dictionary of regions 
    Returns:
    SSPnew: A dataframe with SSP population into world, R5 regions
    """

    folder = 'data/SSP'
    filename = 'SSPv3.csv'
    SSPvnew = pd.read_csv(os.path.join(folder, filename))

    syears = [str(y) for y in years]
    SSPvnew = pd.DataFrame(SSPvnew[SSPvnew.Scenario.isin(selected_scenarios)])

    str_columns = ["Model", "Scenario", "Region", "Unit"]
    keep_columns = str_columns + syears
    SSPvnew = SSPvnew[keep_columns]

    for r in region_dict.keys():
        SSPvnew["Region"] = SSPvnew["Region"].replace(r, region_dict[r])

    selected_regions = list(region_dict.values())

    SSPvnew = pd.DataFrame(SSPvnew[SSPvnew.Region.isin(selected_regions)].groupby(["Model","Region", "Scenario"]).sum([years])).reset_index()

    SSPvnew = SSPvnew.rename(columns={"Region": "IPCCRegion"})
        
    return SSPvnew


def counts (data: pd.DataFrame, region: str):

    """Returns number of population scenarios for each data input 
    and selected region in 2050 and 2100
    data: IPCC database with each year in a single column
    region: selected region

    Returns: dataout: array with shape (2,1) with number of scenarios in
    year 2050 and in year 2100"""

    datavar = data.loc[((data.Variable == "Population") & (data.Region == region))]
    datavar1 = datavar["2050"][datavar["2050"] > 0]
    vals2050 = len(datavar1)
    datavar2 = datavar["2100"][datavar["2100"] > 0]
    vals2100 = len(datavar2)
    name = list(set(data.Report))[0]
    dataout = pd.DataFrame(np.array([vals2050, vals2100]).reshape(2,1), 
            columns=["Scenario Number"], index=[name, name])
    dataout["Region"]=region
    dataout["Year"]=np.array([2050, 2100]).reshape(2,1)
    return dataout

def data_error(truedata: pd.DataFrame, 
               indata: pd.DataFrame, 
               year: float, 
               threshold: float,
               region: str, 
               dataset: str,
               scaler: int,
               untype: str):

    """Gives error estimates on a regional scale assuming UN mean as true data"""
    """Estimate percent error dividing RMSE by true value"""

    """
    truedata: UN population data with yearly data by columns
    indata: AR population
    year: selected year to estimate error
    threshold: tuple with quantiles for keeping interquartile range
    region: selected region
    dataset: name of dataset
    scaler: scaler used for data
    untype: type of data (UN or SSP)
    
    Returns: mean absolute error, mean square error, 
    ratioed root mean squared error"""

    y_pred = pd.DataFrame(indata.loc[indata.Year==year])["Population"].values

    if untype == "UN":
        y_new = transformUN(truedata, region, False)
    else:
        y_new = transformSSP(truedata, region, [year], "Population")
        y_new = y_new.rename(columns={y_new.columns[0]: "Year"})
        y_new["Year"] = year

    y_new = pd.DataFrame(y_new.loc[(y_new.Year == year)])["Population"].values

    # transforms UN data into millions (when equal 1) or billions (when equal 1000)
    y_new *= 1/scaler

    # calculate error on the basis of UN mean and length of AR data
    n = len(y_pred)

    y_true = np.repeat(np.mean(y_new), n)

    MAE = np.sum(np.abs(y_true - y_pred))/(n-1)
    MSE = np.sum(np.power((y_true - y_pred),2))/(n-1)
    RMSE = 100 * np.power(MSE, 0.5)/np.mean(y_true)

    return MAE, MSE, RMSE

def trimsample (sample: np.array,
                low: float,
                up: float):
    """Trims samples of data based on a defined percentage cut
    Values below or higher the relative cut are filtered out
    sample: array of data to trim, representing values for a year
    low: relative percentage for cutting lower bounds
    up: relative percentage for cutting higher bounds

    Returns: array without trimmed values"""

    # mask the values
    trimmed = trim(sample, limits=(low, up), inclusive=(True, True), relative=True)
    # masked values substituted with zeros
    trimmed = trimmed.filled(0.0)
    # filter out zeros
    trimmed = trimmed[np.where(trimmed >0.0)]
    return trimmed

def pre_test (sample_0: np.array,
              sample_1: np.array,  
              low_0: float, 
              up_0: float, 
              low_1: float, 
              up_1: float, 
              function: str,
              qvalue=0):

    """Pre-process samples before applying a Welch t-test
    and calculates the function on the data to be used in the test,
    for example a certain percentile or the standard deviation

    sample_0: first sample of population data at a certain year, 1D array
    sample_1: second sample of population data at a certain year, 1D array
    low_0: relative percentage for the lower-bound trimming on first sample
    up_0: relative percentage for the upper-bound trimming on first sample
    low_1: relative percentage for the lower-bound trimming on second sample
    up_1: relative percentage for the upper-bound trimming on second sample
    function: statistics to calculate on the sample, 
    accepted values are: mean ("mean"), standard deviation ("std"), and percentile ("percentile")
    qvalue: value of the calculated quantile, default to 0

    Returns: 
    v1: calculated statistics on sample 1
    s1: variance of sample 1 
    n1: number of elements in sample 1
    v2: calculated statistics on sample 2
    s2: variance of sample 2
    n2: number of elements in sample 2
    """

    sample1 = trimsample(sample_0, low_0, up_0)
    sample2 = trimsample(sample_1, low_1, up_1)
    sample1 = np.reshape(np.asarray(sample1),-1)
    sample2 = np.reshape(np.asarray(sample2),-1)
    if function=="mean":
        v1 = np.mean(sample1)
        v2 = np.mean(sample2)
    if function=="std":
        v1 = np.std(sample1)
        v2 = np.std(sample2)
    if function=="percentile":
        v1 = np.quantile(sample1, qvalue)
        v2 = np.quantile(sample2, qvalue)

    s1 = np.var(sample1)
    s2 = np.var(sample2)
    n1 = sample1.shape[0]
    n2 = sample2.shape[0]

    return (v1, s1, n1, v2, s2, n2)

def welch_test (v1: float,
                s1: float, 
                n1: int, 
                v2: float, 
                s2: float, 
                n2: int, 
                alternative: str):

    """Applies Welch t-test for two samples or for a sample and value
    v1: calculated statistics on sample 1
    s1: variance of sample 1 
    n1: number of elements in sample 1
    v2: calculated statistics on sample 2 
    s2: variance of sample 2
    n2: number of elements in sample 2

    Returns:
    welch-test result, the degrees of freedom, and the p-value
    """
    vn1 = v1 / n1
    vn2 = v2 / n2
    denom = np.sqrt(vn1 + vn2)

    if n2 > 1:
        df = np.power((vn1 + vn2),2) / (np.power((vn1),2) / (n1 -1) + np.power((vn2),2) / (n2-1))
    else:
        df = np.power((s1/n1 + s2/n2),2) / (np.power((s1/n1),2) / (n1 -1) )

    d = v1-v2
    with np.errstate(divide='ignore', invalid='ignore'):
        welch_t = np.divide(d, denom)
    if alternative == 'less':
        pval = special.stdtr(df, welch_t)
    elif alternative == 'greater':
        pval = special.stdtr(df, -welch_t)
    elif alternative == 'two-sided':
        pval = special.stdtr(df, -np.abs(welch_t))*2

    return (welch_t, df, pval)

def databdiff(database1: pd.DataFrame,
             name1: str, 
             database2: pd.DataFrame, 
             name2: str,
             variable: str,
             function: str,
             qvalue: float,
             alternative: str,
             low_1: float,
             up_1: float,
             low_2: float,
             up_2: float,
             years: list):
    """Represents differences between database 1 and database 2
    distributing them in percentage of decrease or increase
    database1: data sample 1
    name1: name of sample 1 database
    database2: data sample 2
    name2: name of sample 2 database
    variable: variable to compare
    function: statistics to calculate on the sample,
    qvalue: value of the calculated quantile, default to 0
    alternative: alternative hypothesis, accepted values are: less, greater, and two-sided
    low_1: relative percentage for the lower-bound trimming on first sample
    up_1: relative percentage for the upper-bound trimming on first sample
    low_2: relative percentage for the lower-bound trimming on second sample
    up_2:  relative percentage for the upper-bound trimming on second sample
    years: list of years to compare
    """

    out = pd.DataFrame()

    for year in years:
        sample1 = database1.loc[database1.Year==year][variable]
        sample1 = pd.DataFrame(sample1)

        sample2 = database2.loc[database2.Year==year][variable]
        sample2 = pd.DataFrame(sample2)

        if function=="mean":
            mndict = {variable: np.mean(sample2, axis=0)}
            mn2 = pd.DataFrame.from_dict(mndict, orient="columns").reset_index(drop=True)

        if function=="std":
            mndict = {variable: np.std(sample2, axis=0).values[0]}
            mn2 = pd.DataFrame.from_dict(mndict, orient='index', columns=[variable])

        if function=="percentile":
            mn2 = pd.DataFrame(data=np.array(sample2[variable].quantile(qvalue)).reshape(1,1), index=None, columns=[variable])

        #vv = np.array([-0.99, -0.5, -0.10, -0.01, 0.01, 0.10, 0.50, 0.99])
        vv = np.array([-0.1,-0.01, 0.01, 0.1])

        # we compare the dataset deviations with 
        # a fraction of the calculated statistics
        # to determine the bins

        labels = list([ "medium-to-high decrease",  
                        "low decrease", "nearest", "low increase",
                        "medium-to-high increase"])
        
        bins = mn2.values * vv
        bins = bins[0]
        # differences (left) AR6 value vs the AR5/SR 1.5 (right)
        # -0.5	0.5
        # -0.1	0.9
        # -0.01	0.99
        # 0.01	1.01
        # 0.1	1.1
        # 0.5	1.5
        # mar6 - mar5 <= -100 mar5
        # mar6 <= -99 mar5 
        # database2 multiplier: -0.1 + 1 = 0.9, -0.01 + 1 = 0.99,  + 0.01  + 1 = 1.10,  +0.1 + 1 = 1.1

        v_bins = pd.IntervalIndex.from_tuples([ (100 * bins[0], bins[0]),
                                                (bins[0], bins[1]),
                                                (bins[1], bins[2]),
                                                (bins[2], bins[3]),
                                                (bins[3], 100 * bins[3])])

        arr = sample1 - mn2.values



        arr["value"] = pd.cut(arr.values.flatten(), v_bins, right=True, 
                                labels=labels, retbins=False, 
                                precision=3, include_lowest=False, 
                                duplicates='raise', ordered=True)

        grouped = arr.groupby("value", observed=False).count()
        
        data = pd.DataFrame(grouped.transpose().values, columns=labels)

        v1, s1, n1, v2, s2, n2 = pre_test(sample1, sample2, low_1, up_1, low_2, up_2, function, qvalue)
        
        welch_t, df, pval = welch_test(v1, s1, n1, v2, s2, n2, alternative)

        p_value = np.round(pval,3)

        data["p_value"] = p_value

        data["year"] = year

        out = pd.concat((out, data), axis=0)

    return out

def ext_census(years: list):
    """
    Uploads external datasets for the analysis
    US Census Data in billions of people

    years: years to consider

    Returns external datasets:
    censusg: U.S. Census data for global population (billion)
    """
    folder = r'data/other_pop_data'
    filename1 = "uscensus.xlsx"

    census = pd.read_excel(os.path.join(folder, filename1),"uscensus")
    excluded = ["Annual Growth Rate %",
            "Area (sq km)",
            "Density (per sq km)",
            "Total Fertility Rate",
            "Life Expectancy at Birth",
            "Under-5 Mortality Rate"]
    included = [col for col in census.columns if col not in excluded]
    census = census[included]
    census = census.loc[census.Year.isin(years)]
    censusg = census.groupby(["Year", "IPCCRegion"])["Population"].sum().reset_index()
    censusg["Model"] = "U.S. Census"
    censusg["Series"] = "U.S. Census"
    censusg["Scenario"] = "Median USC"
    #censusg["Type"] = "Determ"

    world = census.groupby(["Year"])["Population"].sum().reset_index()
    world["IPCCRegion"] = "WORLD"
    world["Model"] = "U.S. Census"
    world["Series"] = "U.S. Census"
    world["Scenario"] = "Median USC"
    #world["Type"] = "Determ"
    world = world[censusg.columns]
    world["Population"] = world["Population"] / 1e9

    return world

def ext_wbank(updtcolumns: list, years: list):
        """Extracts World Bank data
        
        Inputs:
        columns: list of columns to order dataframe
        years: list of years to consider
        
        Returns:
        wbankg: pd DataFrame with global population (billion)
        """
        # upload world bank data

        folder = r'data/other_pop_data'
        filename2 = "worldbank.xlsx"
        syears = [str(year) for year in years]
        columns = ["Country Name", "IPCCRegion"]

        newcolumns = columns + syears
        syears = [[str(year) + " " + "[YR" + str(year) + "]"] for year in years]
        syears = [item for sublist in syears for item in sublist]

        columns = ["Country Name", "IPCCRegion"] + syears

        dtypes = [str, str, float, float, float]
        wbank = pd.read_excel(os.path.join(folder, filename2),"worldbank", 
        usecols=columns)
        wbank = wbank.rename(columns=dict(zip(columns,newcolumns)))
        wbank = pd.DataFrame(wbank[newcolumns])
        IPCCRegions = ["R5ASIA", "R5OECD90+EU", "R5OWO", "R5LAM", "R5MAF", "R5REF"]
        wbank = wbank[wbank.IPCCRegion.isin(IPCCRegions)]

        wbankg = pd.DataFrame()
        for y in newcolumns[2:]:
            added = pd.DataFrame(wbank.groupby("IPCCRegion")[y].sum().reset_index())
            added = added.rename(columns={y:"Population1"})
            added["Year"] = int(y)
            wbankg = pd.concat((wbankg,added), axis=0)
        wbankg = wbankg.loc[wbankg.IPCCRegion != "IPCCRegion"]

        world = wbankg.groupby(["Year"])["Population1"].sum().reset_index()
 
        world["IPCCRegion"] = "WORLD"
        world["Model"] = "World Bank"
        world["Type"] = "Determ"
        world["Series"] = "WorldBank"
        world["Scenario"] = "Median WB"
        world["Population"] = world["Population1"] * 1/1e9

        return world[updtcolumns]

def ext_ihme(updtcolumns: list, years: list):
    """Extracts IHME data
    from: 
    https://ghdx.healthdata.org/record/ihme-data/global-population-forecasts-2017-2100

    Inputs:
    columns: list of columns to order dataframe
    years: list of years to extract
    
    Returns:
    ihmeframe: pd DataFrame with global population (billion)
    """
    
    # upload sdg data
    folder = r'data/other_pop_data'
    filename = "IHME.csv"

    datar = pd.read_csv(os.path.join(folder, filename))

    data = datar.groupby(["location_name","year_id", "scenario_name"])[["val", "upper", "lower"]].sum().reset_index()
    data = data.rename(columns={"location_name": "IPCCRegion", "year_id": "Year", "val": "Population", "scenario_name": "Series"})
    data["Model"] = "IHME"
    data["Type"] = "Determ"
    data["Scenario"] = data["Series"]

    ihmeframe = data.loc[data.IPCCRegion == "Global"]
    ihmeframe = ihmeframe.replace({"Global": "WORLD"})
    ihmeframe["Population"] *= 1/1e9
    ihmeframe = ihmeframe.loc[ihmeframe["Year"].isin(years)]
    ihmeframe = ihmeframe[updtcolumns]
    return (ihmeframe)

def ext_RFF(years: list):
    """"
    Extract Resources For the Future (RFF) database
    Receives:
    years: list of years to extract
    Returns:
    pdRFF: pd.DataFrame with percentiles of RFF distribution (billion)
    """
    ### Upload RFF data
    folder=r'data'
    all_data = pd.read_csv(os.path.join(folder,"RFF.csv"))

    ### Comparison between probabilistic projections RFF with UN percentiles

    # Here values are transformed in billions
    all_data = all_data.rename(columns={"Pop": "Population"})

    quantiles = [0.05, 0.2, 0.5, 0.8, 0.95]
    # selected data 
    sdata = pd.concat([pd.DataFrame(all_data[["Population","year"]].loc[all_data.year==y]) for y in years])

    # estimate quantiles per year and collect everything in undata
    pdRFF = pd.DataFrame()
    for y in years:
        pdquant = pd.concat([pd.DataFrame.quantile(pd.DataFrame(sdata[["Population"]].loc[all_data.year==y])/1e6, quantile) for quantile in quantiles] )
        pdquant=pd.concat((pdquant.reset_index(),pd.Series(np.array(quantiles)).reset_index()),axis=1)
        pdquant["Year"] = y
        pdRFF = pd.concat((pdRFF,pdquant), axis=0)
    pdRFF = pdRFF.drop("index", axis=1)
    pdRFF.columns = ["Population", "Series", "Year"]
    pdRFF["Scenario"] = pdRFF["Series"]
    change = {0.05: "5 pRFF", 0.2: "20 pRFF", 0.5: "50 pRFF", 0.8: "80 pRFF", 0.95: "95 pRFF"}
    for ch in change.keys():
        pdRFF["Scenario"] = pdRFF["Scenario"].replace(ch, change[ch])
    pdRFF["Model"] = "RFF"
    return pdRFF
    
def ext_undata(wprob, wdet, columns, remove):
    """Extracts the undata probabilistic
    and the extreme deterministic scenarios
    in vertical format

    Inputs:
    wprob: dataframe with probabilistic projections from UN
    wdet: dataframe with deterministic scenarios from UN
    columns: same as pdRFF columns
    remove: list of scenarios to remove


    Returns:
    undata: dataframe with probabilistic projections from UN with year by row
    undata_ext:  dataframe with extreme deterministic projections
    Values are in billion and reported with each year row by row
    """
    # UN data of a certain revision
    undata = transformUN(wprob, "WORLD", True)
    undata["Model"] = "UN"
    # change = {"5": "5 pUN", "20": "20 pUN", "50": "50 pUN", "80": "80 pUN", "95": "95 pUN"}
    # undata = undata[columns]
    # for ch in change.keys():
    #     undata["Scenario"] = undata["Scenario"].replace(ch, change[ch])
    undata["Series"] = pd.Series(undata["Scenario"])
    # change = {"5": 0.05, "20": 0.2, "50": 0.5, "80": 0.8, "95": 0.95}
    # for ch in change.keys():
    #     undata["Series"] = undata["Series"].replace(ch, change[ch])
    # undata=undata.sort_values(by="Series")
    # undata = undata.drop("Series",axis=1)
    undata["Population"] *= 1/1e3
    undata["Model"]="pUN"

    ### Max/min deterministic scenarios from UN, year
    region="WORLD"
    undata_ext, sel_labels = transformUNminmax(wdet, region, False, remove)
    undata_ext["Population"] *=1/1000
    undata_ext["Model"]="dUN"
    return undata, undata_ext

def maxestimate(SSPUN, undata2022, censusg, wbankg, ihmeframe):
    """Estimates maximum of selected timeseries
    International Database generated by U.S. Census (IDB), WOrld Bank, 
    SSP1, SSP2, SSP3, SSP4, SSP5
    UN percentiles of distribution (95, 50, 25, 5)
    Institution of Health and Metrics Evaluation (IHME) scenarios,
    of faster and  lower growwth of educational atttanment anf health quality
    Receives:
    SSPUN: DataFrame with SSP and extreme deterministic UN
    undata2022: DataFrame with probabilistic UN data
    censusg: DataFrame with IDB data
    wbankg: DataFrame with World Bank data
    ihmeframe: DataFrame with IHME
    """
    datassp1 = pd.DataFrame(SSPUN.loc[ ((SSPUN.Model=="SSP") & (SSPUN.Scenario=="SSP1")) ])
    datassp2 = pd.DataFrame(SSPUN.loc[ ((SSPUN.Model=="SSP") & (SSPUN.Scenario=="SSP2")) ])
    datassp3 = pd.DataFrame(SSPUN.loc[ ((SSPUN.Model=="SSP") & (SSPUN.Scenario=="SSP3")) ])
    datassp4 = pd.DataFrame(SSPUN.loc[ ((SSPUN.Model=="SSP") & (SSPUN.Scenario=="SSP4")) ])
    datassp5 = pd.DataFrame(SSPUN.loc[ ((SSPUN.Model=="SSP") & (SSPUN.Scenario=="SSP5")) ])

    undata95 = pd.DataFrame(undata2022.loc[ (undata2022.Series=="95") ])
    undata50 = pd.DataFrame(undata2022.loc[ (undata2022.Series=="50") ])
    undata25 = pd.DataFrame(undata2022.loc[ (undata2022.Series=="20") ])
    undata5 = pd.DataFrame(undata2022.loc[ (undata2022.Series=="5") ])

    dataun = SSPUN.loc[SSPUN.Model=="dUN"]
    datalo = dataun.loc[dataun.Scenario =="Low variant"]
    datact = dataun.loc[dataun.Scenario == "High variant"]

    ihme = ihmeframe.copy(deep=True)
    ihme = ihme.replace({"Faster Met Need and Education": "Faster", 
                        "Fastest Met Need and Education": "Fastest",
                        "Reference": "Reference",
                        "SDG Met Need and Education": "SDG",
                        "Slower Met Need and Education": "Slower"})

    datafaster = pd.DataFrame(ihme.loc[ (ihme.Scenario=="Faster") ])
    datafastest = pd.DataFrame(ihme.loc[ (ihme.Scenario=="Fastest") ])
    dataref = pd.DataFrame(ihme.loc[ (ihme.Scenario=="Reference") ])
    datasdg = pd.DataFrame(ihme.loc[ (ihme.Scenario=="SDG") ])
    dataslower = pd.DataFrame(ihme.loc[ (ihme.Scenario=="Slower") ])

    data = [censusg, wbankg, datassp1, datassp2, datassp3, datassp4, datassp5, undata95, undata50, undata25, undata5,
    ]

    names = ["IDB", "World Bank", "SSP1", "SSP2", "SSP3", "SSP4", "SSP5", "pUN 95 perc", "pUN 50 perc", "pUN 25 perc", "pUN 5 perc"]
    for d,dd in enumerate(data):
        m = max(dd["Population"])
        arg = pd.DataFrame(dd.loc[dd.Population == m]["Year"]).values[0]
        m = round(m, 3)
        print  (names[d], " has maximum of ", m, " billion inhabitants in year ", arg[0])


    data = [datalo, datact]
    names =["UN low variant", "UN high variance"]

    for d,dd in enumerate(data):
        m = max(dd["Population"])
        arg = pd.DataFrame(dd.loc[dd.Population == m]["Year"]).values[0]
        m = round(m, 3)
        print  (names[d], " has maximum of ", m, " billion inhabitants in year ", arg[0])

    data = [ datafaster, datafastest, dataref, datasdg, dataslower]
    names = ["Faster", "Fastest", "Reference", "SDG", "Lower"]

    for d,dd in enumerate(data):
        m = max(dd["Population"])
        arg = pd.DataFrame(dd.loc[dd.Population == m]["Year"]).values[0]
        m = round(m, 3)
        print  ("Scenario ", names[d], " has maximum of ", m, " billion inhabitants in year ", arg[0])
      
def plot_ars(ars: pd.DataFrame, 
            undata1: pd.DataFrame,
            undata2: pd.DataFrame,
            region: str,
            scenarios1: list,
            label_scenarios1: list,
            scenarios2: list,
            label_scenarios2: list,
            limits: tuple,
            ylabel: str,
            years: list):
    """Plots 1 dataframes in two boxplots (AR)
    and 2 dataframes as overlaid curves
    on each subplot (ie. UN databases and SSPs)
    alongisde subplot with marginals for 2100
    ars: dataframe with AR data
    undata1: dataframe with data for first subplot (UN)
    undata2: dataframe with data for second subplot (SSPs)
    region: region to plot
    scenarios1: list of scenarios to plot in first subplot
    label_scenarios1: list of labels for scenarios in first subplot
    scenarios2: list of scenarios to plot in second subplot
    label_scenarios2: list of labels for scenarios in second subplot
    limits: tuple with limits for y axis
    ylabel: label for y axis"""

    cmap = cm.get_cmap('tab20')
    bar_colors_neg1 = cmap(np.linspace(0, 1, int(np.ceil(len(scenarios1))+1)))
    bar_colors1 = bar_colors_neg1


    cmap = cm.get_cmap('tab20c')
    bar_colors_neg2 = cmap(np.linspace(0, 1, int(np.ceil(len(scenarios2))+1)))
    bar_colors2 = bar_colors_neg2

    ar2100 = pd.DataFrame(ars.loc[ars.Year==2100])

    fig = plt.figure()

    gs = fig.add_gridspec(1, 2)
    fig.set_tight_layout(True)
    a1 = fig.add_subplot(gs[0])

    flierprops = dict(marker='o', markerfacecolor="y", markersize=3,
                    linestyle='none',markeredgecolor='teal')

    ystring = [str(y) for y in years]
    
    for sc, scenario in enumerate(scenarios1):   
        w = pd.DataFrame(undata1.loc[undata1.Scenario==scenario]) 
        w["Year"] = np.linspace(1, 9, 9)
        a1.x = np.linspace(1, 9, 9)
        a1.y = w.Population
        a1.plot(a1.x, a1.y, color=bar_colors1[sc], label= sc)


    ars.boxplot(column="Population", ax= a1,  by="Year", rot=90, 
        grid=False,  flierprops=flierprops)
    xlabels = ["", "2030", "", "2050", "", "2070", "", "2090", " "]
    a1.set_xticklabels(xlabels)
    a1.set_title("UN percentiles")

    plt.ylabel(ylabel)
    a1.set_ylim(limits)
    plt.legend(labels=label_scenarios1)

    a2 = fig.add_subplot(gs[1])


    for sc, scenario in enumerate(scenarios2):
        w = undata2.loc[undata2.Scenario==scenario].groupby(["Year", "Scenario"])["Population"].mean().reset_index()
        w["Model"] = "SSP"
        w["Year"]  = np.linspace(1, 9, 9)
        a2.x = np.linspace(1, 9, 9)
        a2.y = w.Population
        a2.plot(a2.x, a2.y, color=bar_colors2[sc], label= sc)


    ars.boxplot(column="Population", ax= a2,  by="Year", rot=90, 
        grid=False, flierprops=flierprops)
    a2.set_title("SSPs")
    plt.legend(labels=label_scenarios2)
    a2.set_ylim(limits)

    a2.set_xticklabels(xlabels)
    plt.ylabel(ylabel)
    fig.get_figure().suptitle(region, fontsize=16)

    plt.show()
    return (fig)

def plot_2ars(ars: pd.DataFrame, 
            undata1: pd.DataFrame,
            undata2: pd.DataFrame,
            region: str,
            scenarios1: list,
            label_scenarios1: list,
            scenarios2: list,
            label_scenarios2: list,
            limits: tuple,
            ylabel: str,
            years: list,):
    """Plots 2 dataframes in two boxplots (AR)
    and another dataframe as overlaid curves
    on each subplot (ie. UN databases and SSPs)
    alongisde subplot with marginals for 2100
    ars: dataframe with AR data
    undata1: dataframe with data for first subplot (UN)
    undata2: dataframe with data for second subplot (SSPs)
    region: region to plot
    scenarios1: list of scenarios to plot in first subplot
    label_scenarios1: list of labels for scenarios in first subplot
    scenarios2: list of scenarios to plot in second subplot
    label_scenarios2: list of labels for scenarios in second subplot
    limits: tuple with limits for y axis
    ylabel: label for y axis
    """

    from matplotlib.transforms import Affine2D
    import mpl_toolkits.axisartist.floating_axes as floating_axes
    cmap= cm.get_cmap("tab20b")
    bar_colors_neg1 = cmap(np.linspace(0, 1, int(np.ceil(len(scenarios1))) ))
    bar_colors1 = bar_colors_neg1


    cmap = cm.get_cmap("nipy_spectral")
    bar_colors_neg2 = cmap(np.linspace(0, 1, int(np.ceil(len(scenarios2))) ))
    bar_colors2=bar_colors_neg2 
    # np.vstack((bar_colors_neg2[2:], bar_colors_neg1[3:]))
    

    ar2100 = pd.DataFrame(ars.loc[ars.Year==2100])

    fig = plt.figure()

    gs = fig.add_gridspec(1, 3,)
   
    a1 = fig.add_subplot(gs[0])

    flierprops = dict(marker='o', markerfacecolor="y", markersize=1.5,
                    linestyle='none',markeredgecolor='teal')

    ystring = [str(y) for y in years]
    
    for sc, scenario in enumerate(scenarios1):   
        w = pd.DataFrame(undata1.loc[undata1.Scenario==scenario])  
        w["Year"] = ystring 
        a1.x = np.linspace(1, 9, 9)
        a1.y = w.Population
        a1.plot(a1.x, a1.y, color=bar_colors1[sc], label= sc)


    ars.boxplot(column="Population", ax= a1,  by="Year", rot=90, 
        grid=False,  flierprops=flierprops)
    xlabels = ["", "2030", "", "2050", "", "2070", "", "2090", " "]
    a1.set_xticklabels(xlabels)
    a1.set_title("UN percentiles")
    a1.tick_params(axis="x",labelrotation=45, pad=0.2)
    
    plt.ylabel(ylabel)
    a1.set_ylim(limits)
    plt.legend(labels=label_scenarios1)
    a2 = fig.add_subplot(gs[1])


    for sc, scenario in enumerate(scenarios2):
        w = undata2.loc[undata2.Scenario==scenario].groupby(["Year", "Scenario"])["Population"].mean().reset_index()
        w["Model"] = "SSP"
        w["Year"] = ystring
        a2.x = np.linspace(1, 9, 9)
        a2.y = w.Population
        a2.plot(a2.x, a2.y, color=bar_colors2[sc], label= sc)


    ars.boxplot(column="Population", ax= a2, by="Year", rot=90, 
        grid=False, flierprops=flierprops)
    a2.set_title("SSPs")
    plt.legend(labels=label_scenarios2)
    a2.set_ylim(limits)

    a2.set_xticklabels(xlabels)
    a2.set_yticklabels([])
    a2.tick_params(axis="x",labelrotation=45, pad=0.2)

    a3 = fig.add_subplot(gs[2])

    sns.kdeplot(
        data=pd.DataFrame(ar2100), y="Population", fill=True, ax=a3,

    )

    a3.set_ylabel("")   
    a3.set_yticklabels([])
    a3.set_xticks([0, 0.5, 1.0, 1.5], labels=[" ", "0.5", "1.0", "1.5"])
    a3.tick_params(axis="x",labelrotation=45, pad=7)
    fig.get_figure().suptitle(" ")
    
    plt.title("Year=2100")
    plt.ylim(limits)
    plt.tight_layout()
    plt.subplots_adjust(hspace=.0)
    plt.show()
    return(fig)

def plot_mars(ars: pd.DataFrame, 
            undata1: pd.DataFrame,
            region: str,
            scenarios1: list,
            label_scenarios1: list,
            limits: tuple,
            ylabel: str,
            years: list):
    """Plots 2 dataframes in two boxplots (AR)
    and another dataframe as overlaid curves
    on each subplot (ie. UN databases and SSPs)
    alongisde subplot with marginals for 2100
    ars: dataframe with AR data
    undata1: dataframe with data for first subplot (UN)
    region: region to plot
    scenarios1: list of scenarios to plot in first subplot
    label_scenarios1: list of labels for scenarios in first subplot
    limits: tuple with limits for y axis
    ylabel: label for y axis"""

    cmap = cm.get_cmap('tab20')
    bar_colors_neg1 = cmap(np.linspace(0, 1, int(np.ceil(len(scenarios1))) + 2 ))
    bar_colors1 = bar_colors_neg1

    ar2100 = pd.DataFrame(ars.loc[ars.Year==2100])

    fig = plt.figure()

    gs = fig.add_gridspec(1, 2)
    fig.set_tight_layout(True)
    a1 = fig.add_subplot(gs[0])

    flierprops = dict(marker='o', markerfacecolor="y", markersize=1.5,
                    linestyle='none',markeredgecolor='teal')

    ystring = [str(y) for y in years]
    
    for sc, scenario in enumerate(scenarios1):
        w = undata1.loc[undata1.Scenario==scenario].groupby(["Year", "Scenario"])["Population"].mean().reset_index()
        w["Model"] = "SSP"
        w["Year"] = ystring
        a1.x = np.linspace(1, 9, 9)
        a1.y = w.Population
        a1.plot(a1.x, a1.y, color=bar_colors1[sc], label= sc)


    ars.boxplot(column="Population", ax= a1,  by="Year", rot=90, 
        grid=False,  flierprops=flierprops)
    xlabels = ["", "2030", "", "2050", "", "2070", "", "2090", " "]
    a1.set_xticklabels(xlabels)
    a1.set_title("SSPS")

    plt.ylabel(ylabel)
    a1.set_ylim(limits)
    plt.legend(labels=label_scenarios1)
    
    a2 = fig.add_subplot(gs[1])
    sns.kdeplot(
        data=ar2100, y="Population",  fill=True,
    )
    a2.set_xlabel(ylabel)

    fig.get_figure().suptitle(region, fontsize=16)
    
    plt.title("Year=2100")
    plt.ylim(limits)

    plt.show()
    return(fig)

path_for_figure = os.path.join(os.getcwd(),"figures_population_paper")
osExists = os.path.exists(path_for_figure)

if not osExists:
    os.makedirs(path_for_figure)