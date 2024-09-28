import numpy as np
import os
import pandas as pd
import streamlit as st

dirfolder = os.getcwd()
if "pantarei" not in dirfolder:
    dirfolder = os.path.join(dirfolder, "pantarei")

st.image(os.path.join(dirfolder, "data/MSCA_logo.png"))

st.title("PANTA REI: Prospettive di AdattameNTo sociAle nell'eRa del cambiamEnto climatico")

st.write("Benvenuti. Vedremo come adattamento e mitigazione entrino nella modellazione climatica")


