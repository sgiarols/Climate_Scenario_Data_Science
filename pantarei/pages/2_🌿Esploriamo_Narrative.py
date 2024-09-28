import numpy as np
import os
import pandas as pd
import streamlit as st

dirfolder = os.getcwd()
if "pantarei" not in dirfolder:
    dirfolder = os.path.join(dirfolder, "pantarei")

st.title("Focus sulla dimensione sociale")

st.write("La narrativa socioeconomica dietro lo scenario climatico")

folder = "data/"
folder = os.path.join(dirfolder, folder)

# Metadata have been edited correcting the Sustainable IMP which was wrongly assinged to SSP2
file = "SSPs.png"

file = os.path.join(folder, file)
st.image(file)

st.write("Narrative demografiche e clima")

file = "SSP_UN_chart_global.png"
file = os.path.join(folder, file)
st.image(file)
st.write("Giarola et al. npj climate action (2024)")


st.write("Emissioni, mitigazione, ed giustizia climatica")
folder = "data/"
folder = os.path.join(dirfolder, folder)

# Metadata have been edited correcting the Sustainable IMP which was wrongly assinged to SSP2
file = "GDP_Emissions.png"

file = os.path.join(folder, file)
st.image(file)
st.write("O'Neil et al. npj climate action (2024)")