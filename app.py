# How to Build, Deploy & Share a Python app!
from pathlib import Path
import pandas as pd

import plotly.express as px
from shiny import reactive
from shiny.express import render,input, ui
from shinywidgets import render_plotly

ui.page_opts(title="Sales Dashboard - Video 1 of 5", fillable=True)

@reactive.calc
def dat():
    infile = Path(__file__).parent / "data/sales.csv"
    return pd.read_csv(infile)

with ui.layout_columns():

    @render_plotly
    def plot1():
        return px.histogram(px.data.tips(), y="tip")

    @render_plotly
    def plot2():
        return px.histogram(px.data.tips(), y="total_bill") 
