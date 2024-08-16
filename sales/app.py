# How to Build, Deploy & Share a Python app!
from pathlib import Path
import pandas as pd

import plotly.express as px
from shiny import reactive
from shiny.express import render,input, ui
from shinywidgets import render_plotly

ui.page_opts(title="Sales Dashboard - Video 1 of 5", fillable=True)

ui.input_numeric("n", "Number of Items", 5, min=0, max=20)

@reactive.calc  #when you do not have many time to code, each time you can use this
def dat():
    infile = Path(__file__).parent / "data/sales.csv"
    df = pd.read_csv(infile)
    df['order_date'] = pd.to_datetime(df['order_date']) #we modify the df, adding new column Month, if you wanna modify the df use copy not original, otherwise it will cause to other places
    df['month'] = df['order_date'].dt.month_name()
    return df #it returns the cashed value

@render_plotly
def plot1():
    df = dat()
    top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()
    return px.bar(top_sales, x='product', y='quantity_ordered')


@render_plotly
def sales_over_time():
    df = dat()
    sales = df.groupby(['city', 'month'])['quantity_ordered'].sum().reset_index()
    print(sales)

with ui.card():
    ui.card_header("Sample Sales Data")
    @render.data_frame
    def sample_sales_data():
        return dat().head(100)



    #@render.data_frame
    #def data():
    #    return dat()