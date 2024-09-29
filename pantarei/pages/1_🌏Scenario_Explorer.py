import numpy as np
import os
import pandas as pd
import streamlit as st

dirfolder = os.getcwd()

path = os.path.abspath(dirfolder)

if "pantarei" not in path:
    dirfolder = os.path.join(path, "pantarei")

st.title("Focus on emissions")
def readdata (selected_var, syears):

    file = os.path.join(dirfolder, "pages/data/AR6_Scenarios_Database_World_v1.1.csv")

    strings = ["Model",	"Scenario",	"Region",	"Variable",	"Unit"]

    selected_col = strings + syears
    data = pd.read_csv(file)[selected_col]

    my_data = pd.DataFrame(data[data.Variable.isin(selected_var)])
    return my_data


def add_policy(chart_data: pd. DataFrame):
    # part 2 meta added
    folder = "pages/data/"
    folder = os.path.join(dirfolder, folder)

    # Metadata have been edited correcting the Sustainable IMP which was wrongly assinged to SSP2
    file = "AR6_meta.csv"

    file = os.path.join(folder, file)
    metadata = pd.read_csv(file, encoding='unicode_escape')
    policy= metadata["Policy_category"]
    policy = list(policy.fillna("Unknown"))
    scens = list(metadata["Scenario"])

    not_scens = [sc for sc in list(set(chart_data.Scenario)) if sc not in scens]
    not_scenspol = ["Unknown" for i in range(len(not_scens))]

    scens = scens + not_scens
    policy = policy + not_scenspol

    dict_policy = dict(zip(scens,policy))

    chart_data["Policy"] = chart_data["Scenario"].apply(lambda x: dict_policy[x])

    return chart_data

def add_category(chart_data: pd. DataFrame):
    folder = "pages/data"
    folder = os.path.join(dirfolder, folder)

    # Metadata have been edited correcting the Sustainable IMP which was wrongly assinged to SSP2
    file = "AR6_meta.csv"

    file = os.path.join(folder, file)
    metadata = pd.read_csv(file, encoding='unicode_escape')
    policy= metadata["Category_subset"]
    policy = list(policy.fillna("Unknown"))
    scens = list(metadata["Scenario"])

    not_scens = [sc for sc in list(set(chart_data.Scenario)) if sc not in scens]
    not_scenspol = ["Unknown" for i in range(len(not_scens))]

    scens = scens + not_scens
    policy = policy + not_scenspol

    dict_policy = dict(zip(scens,policy))

    chart_data["Category"] = chart_data["Scenario"].apply(lambda x: dict_policy[x])
    category = list(chart_data.Category.unique())
    new_category = ["C1", "C5", "C3", "C4", "C7", "C8", "C6", "C3", "C1", "C2", "no climate asessment", "Unknown"]
    dict_category = dict(zip(category, new_category))
    chart_data["Category"] = chart_data["Category"].apply(lambda x: dict_category[x])

    return chart_data

def select_variable(my_data: pd.DataFrame, selection: str, years: list, syears: list):
    # select variable
    chart_data = pd.DataFrame(my_data.loc[my_data.Variable==selection])
    new_cols = ["S" + str(c) for c in range(len(chart_data))]
    chart_data["String"] = new_cols

    chart_data = add_policy(chart_data)
    chart_data = add_category(chart_data)

    selected_col = ["String"] + strings + ["Policy"] + ["Category"] + syears
    chart_data = chart_data[selected_col]

    chart_data = chart_data.rename(columns=dict(zip(syears, years)))

    chart_data = chart_data.drop(["Model", "Region"], axis=1)
    return chart_data


def re_order(chart_data: pd.DataFrame):
    # estimate sum over columns
    chart_data['Sum']=chart_data[years].sum(axis=1)

    allmin = pd.DataFrame()
    allmax = pd.DataFrame()
    for category in chart_data.Category.unique():
        data = pd.DataFrame(chart_data.loc[chart_data.Category == category])
        data = data.sort_values(by="Sum", ascending=True)
        allmin = pd.concat((allmin,pd.DataFrame(data.iloc[0]).transpose()), axis=0)
        data = data.sort_values(by="Sum", ascending=False)
        allmax = pd.concat((allmax,pd.DataFrame(data.iloc[0]).transpose()),axis=0)
    return (allmin, allmax)

# config
baseyear = 2010
endyear = 2110
years = np.arange(baseyear, endyear, step=10)
syears = [str(y) for y in years]

selected_var = [
                "Emissions|CO2",
                ]
selected_var_name = [
                "CO2 Emissions",             
                ]

strings = ["Model",	"Scenario",	"Region",	"Variable",	"Unit"]
# config
output = readdata(selected_var, syears)

# change units
output[syears]*= 1/1000
output["Unit"] = "Gt CO2/yr"


st.write("A scenario shows how emissions can evolve")

label = "Emissions of CO2 has different categories (values in Gt CO2 / yr)"

selection = "CO2 Emissions"

# Part 1
chart_data = select_variable(output, selected_var[selected_var_name.index(selection)], years, syears)

chart_data1 = chart_data.transpose()
chart_data1.columns = chart_data1.loc[chart_data1.index=="String"].values[0]
chart_data1 = chart_data1.iloc[6:,:]
st.area_chart(chart_data1)


# Part 2
st.write("Maybe the chart is too confusing for the high number of scenarios")

chart_data2 = re_order(chart_data)[0]

chart_data2min = pd.DataFrame(chart_data2[years]).transpose()
chart_data2min.columns = chart_data2["Category"]
st.write("Let's see the trends for the minimum values")

st.line_chart(chart_data2min)

st.write("Let's see the trends for the maximum values")
chart_data2 = re_order(chart_data)[1]

chart_data2max = pd.DataFrame(chart_data2[years]).transpose()
chart_data2max.columns = chart_data2["Category"]

st.line_chart(chart_data2max)

st.write("Policies influence emissions differently")

# Here we change the 
st.title("The use of fuels effects emissions")

select_variable_fuel = ["Final Energy|Electricity",
                        "Final Energy|Gases",
                        "Final Energy|Liquids",
                        "Final Energy|Solids|Coal",]

display_variable = ["electricity", "gaseous fuels", "liquid fuels", "solid fuels"]

my_fuel = readdata (select_variable_fuel, syears)


select_mit = list(chart_data2.Category.unique())
st.write("Policies can be more or less stringent")
mit_sel = st.selectbox("Choose a climate ambition", select_mit, index=0)

chart_data_mit = chart_data.loc[chart_data.Category == mit_sel]
chart_data_mit1 = chart_data_mit.transpose()
chart_data_mit1.columns = chart_data_mit1.loc[chart_data_mit1.index=="String"].values[0]
length = int(len(chart_data_mit1)-1)
chart_data_mit1 = chart_data_mit1.iloc[6:length,:]


st.area_chart(chart_data_mit1)

# #filter by mitigation

chart_fuel = readdata(select_variable_fuel, syears)
chart_fuel = add_category(chart_fuel)
chart_fuel = add_policy(chart_fuel)
chart_fuel1 = pd.DataFrame(chart_fuel.loc[chart_fuel.Category==mit_sel])
max_scenarios = [i+1 for i in range(10000)]
scen_sel = st.selectbox("Limit the number of scenarios to represent ", max_scenarios, index=10)

for i in range(len(select_variable_fuel)):
    st.write("This is the energy trend in EJ /yr as ", display_variable[i])

    chart_fuel2 = pd.DataFrame(chart_fuel1.loc[chart_fuel1.Variable==select_variable_fuel[i]])

    new_cols = ["S" + str(c) for c in range(len(chart_fuel2))]

    scen_sel = min(scen_sel, len(new_cols))

    chart_fuel2["String"] = new_cols

    chart_fuel2 = add_policy(chart_fuel2)

    chart_fuel2 = add_category(chart_fuel2)

    selected_col = ["String"] + strings + ["Policy"] + ["Category"] + syears

    chart_fuel2 = chart_fuel2[selected_col]
    chart_fuel3 = chart_fuel2.transpose()
    chart_fuel3.columns = chart_fuel3.loc[chart_fuel3.index=="String"].values[0]
    chart_fuel3 = chart_fuel3.iloc[8:,:scen_sel]

    st.area_chart(chart_fuel3)



