# How to Build, Deploy & Share a Python app!
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly

ui.page_opts(title="Sales Dashboard - Video 1 of 5", fillable=True)
with ui.layout_columns():

    @render_plotly
    def plot1():
        return px.histogram(px.data.tips(), y="tip")

    @render_plotly
    def plot2():
        return px.histogram(px.data.tips(), y="total_bill") 
