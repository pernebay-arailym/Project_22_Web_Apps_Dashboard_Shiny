# How to Build, Deploy & Share a Python app!
from pathlib import Path
import pandas as pd
import numpy as np 
import calendar

import matplotlib.pyplot as plt

import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly

ui.page_opts(title="Sales Dashboard - Video 3 of 5", fillable=False)

#ui.input_checkbox("bar_color", "Make Bars Red?", False)  

#@reactive.calc
#def color():
#    return "red" if input.bar_color() else "blue"

@reactive.calc  #when you do not have many time to code, each time you can use this
def dat():
    infile = Path(__file__).parent / "data/sales.csv"
    df = pd.read_csv(infile)
    df['order_date'] = pd.to_datetime(df['order_date']) #we modify the df, adding new column Month, if you wanna modify the df use copy not original, otherwise it will cause to other places
    df['month'] = df['order_date'].dt.month_name()
    df['hour'] = df['order_date'].dt.hour
    df['value'] = df['quantity_ordered']*df['price_each']
    return df #it returns the cashed value

with ui.card():  
    ui.card_header("Sales by City 2023")

    with ui.layout_sidebar():  
        with ui.sidebar(bg="#f8f8f8", open='open'):  
            ui.input_selectize(  
                "city",  
                "Selec t a City:",  
                ['Dallas (TX)', 'Boston (MA)', 'Los Angeles (CA)', 'San Francisco (CA)', 'Seattle (WA)', 'Atlanta (GA)', 'New York City (NY)', 'Portland (OR)', 'Austin (TX)', 'Portland (ME)'],  
        multiple=False,
        selected='Boston (MA)'  
        )    
            
    @render_plotly 
    def sales_over_time():
        df = dat()
        print(list(df.city.unique()))
        sales = df.groupby(['city', 'month'])['quantity_ordered'].sum().reset_index()
        sales_by_city = sales[sales['city'] == input.city()]   #filter to cities
        month_orders = calendar.month_name[1:]
        fig = px.bar(sales_by_city, x='month', y='quantity_ordered', title=f"Sales over Time -- {input.city()}", category_orders={'month': month_orders})
        #fig.update_traces(marker_color=color())
        return fig  

with ui.layout_column_wrap(width=1/2):
    with ui.navset_card_underline(id="tab", footer= ui.input_numeric("n", "Number of Items", 5, min=0, max=20)):  
        with ui.nav_panel("Top Sellers"):

            @render_plotly
            def plot_top_sellers():
                df = dat()
                top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()
                fig = px.bar(top_sales, x='product', y='quantity_ordered')
                #fig.update_traces(marker_color=color())
                return fig

        with ui.nav_panel("Top Sellers Value ($)"):

            @render_plotly
            def plot_top_sellers_value():
                df = dat()
                top_sales = df.groupby('product')['value'].sum().nlargest(input.n()).reset_index()
                fig = px.bar(top_sales, x='product', y='value')
                #fig.update_traces(marker_color=color())
                return fig

        with ui.nav_panel("Lowest Sellers"):
            @render_plotly
            def plot_lowest_sellers():
                df = dat()
                top_sales = df.groupby('product')['quantity_ordered'].sum().nsmallest(input.n()).reset_index()
                fig = px.bar(top_sales, x='product', y='quantity_ordered')
                #fig.update_traces(marker_color=color())
                return fig

        with ui.nav_panel("Lowest Sellers Value ($)"):
            @render_plotly
            def plot_lowest_sellers_value():
                df = dat()
                top_sales = df.groupby('product')['value'].sum().nsmallest(input.n()).reset_index()
                fig = px.bar(top_sales, x='product', y='value')
                #fig.update_traces(marker_color=color())
                return fig

    with ui.card():
        ui.card_header("Sales by Time of Day Heatmap")
        @render.plot
        def plot_sales_by_time():
            df = dat()
            sales_by_hour = df['hour'].value_counts().reset_index()
            print(sales_by_hour)
            plt.bar(x=sales_by_hour['hour'], height=sales_by_hour['count'])
            plt.xticks(np.arange(0, 24))

with ui.card():
    ui.card_header("Sales by Location Map")
    "Contecnt Here"

with ui.card():
    ui.card_header("Sample Sales Data")
    
    @render.data_frame
    def sample_sales_data():
        return dat().head(100)