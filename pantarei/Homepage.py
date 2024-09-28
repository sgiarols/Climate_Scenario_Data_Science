import numpy as np
import os
import pandas as pd
import streamlit as st

dirfolder = os.getcwd()
dirfolder = os.path.join(dirfolder, "/pantarei")
st.image(os.path.join(dirfolder, "MSCA_logo.png"))

st.title("PANTA REI: Perspectives on mitigation and adaptation of climate change")

st.write("Welcome! We will see how mitigation and adaptation are in the modelling.")


