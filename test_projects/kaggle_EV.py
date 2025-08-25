# kaggle was only needed to download the dataset; uncomment to download
# import kagglehub

# Download latest version
# path = kagglehub.dataset_download("patricklford/global-ev-sales-2010-2024")


from pathlib import Path # to use relative paths

import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px

currentDir = Path(__file__).parent
file_path = currentDir.parent / "Data Sets" / "IEA Global EV Data 2024.csv"

df = pd.read_csv("../Data Sets/IEA Global EV Data 2024.csv")

# Initialize graphic No. 1 (Percentage of EV Sales Worldwide)
worldwidePercentage = df[
    (df["region"] == 'World') & 
    (df["mode"] == "Cars") &
    (df["parameter"] == "EV sales share") &
    (df["unit"] == "percent")
]
predictedCurrent = worldwidePercentage[
    (worldwidePercentage["category"].str.contains("Projection")) &
    (worldwidePercentage["year"] < 2023)
].index
worldwidePercentage = worldwidePercentage.drop(predictedCurrent)

fig1 = px.line(worldwidePercentage, x='year', y='value', color='category',line_dash="category")

# Initialize graphic No. 2 ()
groupedByRegion = df[
    (df["year"] < 2024) & 
    (df["mode"] == "Cars") &
    (df["parameter"] == "EV sales share") &
    (df["unit"] == "percent") & 
    ((df["region"] == "Europe") | (df["region"] == "North America") | (df["region"] == "Asia") | (df["region"] == "Australia") | (df["region"] == "South America") |
     (df["region"] == "Rest of the World"))
]
fig2 = px.bar(groupedByRegion, x='year', y='value', color='region', barmode='group')

# Initialize the Dash app
app = Dash()

app.layout = html.Div([
    html.H2("Global EV Sales (2010-2023)"),
    html.Div("This is a simple dashboard visualizing the rise in global sales of electric vehicles (EVs) from 2010 to 2023."),
    html.Div([
        dash_table.DataTable(
            data=df.to_dict('records'),
            page_size=12,
            style_table={'overflowX': 'auto'}
        ),
        dash_table.DataTable(
            data=groupedByRegion.to_dict('records'),
            page_size=6,
            style_table={'overflowX': 'auto'}
        ),
        html.P("The following graph shows the percentage of EV sales worldwide from 2010 to 2024. Furthermore, it shows predictions up until 2035 in two variants, " \
        "one scenario for the case that all pledged climate targets are fully met (APS) and one scenario using current policies (STEPS), thus resulting in a more conservative projection."),
        dcc.Graph(figure=fig1)
    ]),
    html.Div([
            html.Div("The next graphic gives a more detailled perspective on the sales of EVs, grouped by region. Using the slider, you can explore the data year by year.",
                     style={'display': 'inline-block'}),
            dcc.Graph(figure=fig2, style={'display': 'inline-block'})
    ])
])

app.run()