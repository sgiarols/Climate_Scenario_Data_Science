import numpy as np
import os

import pandas as pd
import streamlit as st

dirfolder = os.getcwd()

path = os.path.abspath(dirfolder)

if "pantarei" not in path:
    dirfolder = os.path.join(path, "pantarei")

st.write(dirfolder)

st.image(os.path.join(dirfolder, "MSCA_logo.png"))

st.title("PANTA REI: Perspectives on mitigation and adaptation of climate change")

st.write("Welcome! We will see how mitigation and adaptation are in the modelling.")



