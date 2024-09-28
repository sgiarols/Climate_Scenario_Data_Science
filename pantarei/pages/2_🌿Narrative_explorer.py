import numpy as np
import os
import pandas as pd
import streamlit as st

dirfolder = os.getcwd()

st.title("Focus on social dimension in scenarios")

st.write("Scenarios are based on a socio-economic narrative")
st.write("The most used framework in climate-economic scenarios uses the Shared Socioeconomic Pathways")
folder = "pages/data/"
folder = os.path.join(dirfolder, folder)

# Metadata have been edited correcting the Sustainable IMP which was wrongly assinged to SSP2
file = "SSPs.png"

file = os.path.join(folder, file)
st.image(file)
url = "https://doi.org/10.1038/s44168-024-00152-y"
st.markdown("Source: [link](%s)" % url)

st.title("Demographic narratives in scenarios")

file = "SSP_UN_chart_global.png"
file = os.path.join(folder, file)
st.image(file)
url = "https://doi.org/10.1038/s44168-024-00152-y"
st.markdown("Source: [link](%s)" % url)


st.title("Emissions, mitigation, and climate justice")
folder = "pages/data/"
folder = os.path.join(dirfolder, folder)

# Metadata have been edited correcting the Sustainable IMP which was wrongly assinged to SSP2
file = "GDP_Emissions.png"

file = os.path.join(folder, file)
st.image(file)
url = "https://ourworldindata.org/"
st.markdown("Source: [link](%s)" % url)