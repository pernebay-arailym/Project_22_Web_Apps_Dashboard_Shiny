# How to Build, Deploy & Share a Python app!
from pathlib import Path
import pandas as pd

import plotly.express as px
from shiny import reactive
from shiny.express import render,input, ui
from shinywidgets import render_plotly

ui.page_opts(title="Sales Dashboard - Video 1 of 5", fillable=True)

ui.input_numeric("n", "Number of Items", 5, min=0, max=20)

@reactive.calc
def dat():
    infile = Path(__file__).parent / "data/sales.csv"
    return pd.read_csv(infile)

@render_plotly
def plot1():
    df = dat()
    top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()
    return px.bar(top_sales, x='product', y='quantity_ordered')


@render_plotly
def sales_over_time():
    df = dat()
    print(df)

with ui.card():
    ui.card_header("Sample Sales Data")
    @render.data_frame
    def sample_sales_data():
        return dat().head(100)



    #@render.data_frame
    #def data():
    #    return dat()