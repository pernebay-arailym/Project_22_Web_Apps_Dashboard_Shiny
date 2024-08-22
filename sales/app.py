# How to Build, Deploy & Share a Python app!
from pathlib import Path
import pandas as pd
import numpy as np 
import seaborn as sns 
import calendar

import altair as alt

import folium
from folium.plugins import HeatMap

import matplotlib.pyplot as plt

import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly, render_altair, render_widget

ui.tags.style(
    """
    .header-container {
        display: flex;
        align-items: center;
        padding: 10px;
        height: 60px; /* Added missing semicolon */
    }

    .header-container img {
        width: 40px; /* Adjusted width for better visibility */
        margin-right: 1px; /* Space between the image and the title */
    }

    .title-container h2 {
        color: white;
        margin: 0;
        font-size: 38px; /* Adjust the size if needed */
    }

    body {
        background-color: slategray;
    }

    .modebar{
        display: none;
    }
        """
)

# Define a function to apply common styling
def apply_plotly_style(fig, yaxis_title):
    fig.update_layout(
        xaxis_title='',  # Remove x-axis label
        yaxis_title=yaxis_title,  # Update y-axis label
        plot_bgcolor='white',  # Remove background color
        paper_bgcolor='white',  # Remove paper background color
        coloraxis_showscale=False,
        xaxis=dict(
            showgrid=False,  # Remove gridlines from x-axis
            zeroline=False    # Remove zero line
        ),
        yaxis=dict(
            showgrid=False,  # Remove gridlines from y-axis
            zeroline=False   # Remove zero line
        ),
    )
    return fig

ui.page_opts(window_title="Sales Dashboard - Video 3 of 5", fillable=False)

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

with ui.tags.div(class_="header-container"):
    
    with ui.tags.div(class_="header-container"):
        @render.image  
        def image():
            here = Path(__file__).parent
            img = {"src": here / "/Users/pernebayarailym/Documents/Portfolio Projects AP/Python Projects/Project_22_Web_Apps_Dashboard_Shiny/sales/shiny-logo.png", "width": "100px"}  
            return img
        
    with ui.tags.div(class_="title-container"):
        ui.h2("Electronics Sales Performance Analysis Dashboard")


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
            
        @render_altair 
        def sales_over_time():
            df = dat()

            sales = df.groupby(['city', 'month'])['quantity_ordered'].sum().reset_index()
            sales_by_city = sales[sales['city'] == input.city()]  # filter to city

            # Define month names for ordering
            month_orders = calendar.month_name[1:]

            # Define the darkest color for text (darker than slategray)
            dark_slategray = '#2F4F4F'

            # Create the Altair chart
            chart = alt.Chart(sales_by_city).mark_bar().encode(
                x=alt.X('month:O', title='Month', sort=month_orders),
                y=alt.Y('quantity_ordered:Q', title='Quantity Ordered'),
                color=alt.value('#1f77b4')  # Replace with your color
            ).properties(
                title=f"Sales over Time -- {input.city()}"
            ).configure_axis(
                grid=False,  # Remove gridlines
                tickSize=0,  # Remove tick marks
                labelFontSize=12,
                labelColor=dark_slategray,  # Set font color darker than slategray
                titleFontSize=14,
                titleColor=dark_slategray  # Set title font color to match labels
            ).configure_title(
                fontSize=16,
                font='Arial',
                anchor='middle',
                color=dark_slategray  # Set chart title font color
            )

            return chart

with ui.layout_column_wrap(width=1/2):
    with ui.navset_card_underline(id="tab", footer= ui.input_numeric("n", "Number of Items", 5, min=0, max=20)):  
        with ui.nav_panel("Top Sellers"):

            @render_plotly
            def plot_top_sellers():
                df = dat()
                top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()

                # Create the bar chart with Plotly Express
                fig = px.bar(top_sales, x='product', y='quantity_ordered', color='quantity_ordered',
                             color_continuous_scale=px.colors.sequential.Blues)  # Use the Blues color spectrum
                               # You can specify a title if desired

                # Apply standardized styling
                fig = apply_plotly_style(fig, "Quantity Ordered")

                return fig

        with ui.nav_panel("Top Sellers Value ($)"):

            @render_plotly
            def plot_top_sellers_value():
                df = dat()
                top_sales = df.groupby('product')['value'].sum().nlargest(input.n()).reset_index()
                # Create the bar chart with Plotly Express
                fig = px.bar(top_sales, x='product', y='value', color='value',
                             color_continuous_scale=px.colors.sequential.Blues)  # Use the Blues color spectrum
                               # You can specify a title if desired

                # Apply standardized styling
                fig = apply_plotly_style(fig, "Total Sales ($)")
                return fig

        with ui.nav_panel("Lowest Sellers"):
            @render_plotly
            def plot_lowest_sellers():
                df = dat()
                top_sales = df.groupby('product')['quantity_ordered'].sum().nsmallest(input.n()).reset_index()
                fig = px.bar(top_sales, x='product', y='quantity ordered', color='quantity_ordered',
                             color_continuous_scale='Reds')  # Use the Blues color spectrum
                               # You can specify a title if desired

                # Apply standardized styling
                fig = apply_plotly_style(fig, "Quantity Ordered")
                #fig.update_traces(marker_color=color())
                return fig

        with ui.nav_panel("Lowest Sellers Value ($)"):
            @render_plotly
            def plot_lowest_sellers_value():
                df = dat()
                top_sales = df.groupby('product')['value'].sum().nsmallest(input.n()).reset_index()
                fig = px.bar(top_sales, x='product', y='value', color='value',
                             color_continuous_scale='Reds')  # Use the Blues color spectrum )  # You can specify a title if desired

                # Apply standardized styling
                fig = apply_plotly_style(fig, "Total Sales ($)")
                #fig.update_traces(marker_color=color())
                return fig

    with ui.card():
        ui.card_header("Sales by Time of Day Heatmap")
        @render.plot
        def plot_sales_by_time():
            df = dat()
            sales_by_hour = df['hour'].value_counts().reindex(np.arange(0, 24), fill_value=0)
            
            heatmap_data = sales_by_hour.values.reshape(24,1)
            sns.heatmap(heatmap_data,
                        annot=True,
                        fmt="d",
                        cmap="coolwarm",
                        cbar=False,
                        xticklabels=[],
                        yticklabels=[f"{i}:00" for i in range(24)])
            
            plt.title("Number of Orders by Hour of Day")
            plt.xlabel("Hour of Day")
            plt.ylabel("Order Count")

with ui.card():
    ui.card_header("Sales by Location Map")
    @render.ui  #has render html
    def plot_us_heatmap():
        df = dat()

        heatmap_data = df[['lat', 'long', 'quantity_ordered']].values
       
        map = folium.Map(location=[32.96, -96.83], zoom_start=4)
        HeatMap(heatmap_data).add_to(map)
        
        return map

with ui.card():
    ui.card_header("Sample Sales Data")
    
    @render.data_frame
    def sample_sales_data():
        return render.DataTable(dat().head(100), selection_mode="row", filters=True)