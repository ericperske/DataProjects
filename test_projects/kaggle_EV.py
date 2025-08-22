# kaggle was only needed to download the dataset; uncomment to download
# import kagglehub

# Download latest version
# path = kagglehub.dataset_download("patricklford/global-ev-sales-2010-2024")
import os
print("Arbeitsverzeichnis:", os.getcwd())
print("Existiert Datei?", os.path.exists("../Data Sets/IEA Global EV Data 2024.csv"))

from pathlib import Path # to use relative paths

import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

currentDir = Path(__file__).parent
file_path = currentDir.parent / "Data Sets" / "IEA Global EV Data 2024.csv"

df = pd.read_csv("../Data Sets/IEA Global EV Data 2024.csv")

# Initialize the Dash app
app = Dash()

app.layout = html.Div([
    html.H2("Global EV Sales (2010-2024)"),
    html.Div("This is a simple dashboard visualizing the rise in global sales of electric vehicles (EVs) from 2010 to 2024."),
])