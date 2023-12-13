# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 16:59:06 2023

@author: prasanna_udara
"""
# Import pandas and matplot library packages
import pandas as pd
import matplotlib.pyplot as plt


def read_data(filename):
    '''
    Function to read the dataframe "filename" and return the two clean
    dataframes where one with year as columns and another with countries as
    columns.
    '''

    # Selected Indicator list
    indicator_lst = [
        "Cereal yield (kg per hectare)",
        "Average precipitation in depth (mm per year)",
        "Agricultural irrigated land (% of total agricultural land)",
        "Agricultural land (% of land area)",
        "Arable land (% of land area)",
        "Forest area (% of land area)"]

    # Selected countries list
    country_lst = ["Australia", "Spain", "India", "Pakistan", "Afghanistan",
                   "Azerbaijan", "Jordan", "Kyrgyz Republic", "Romania",
                   "Slovenia"]

    # Read the csv file as dataframe and skip 4 rows
    df = pd.read_csv(filename, skiprows=4)

    # Select the desired indicators and country names from the original data
    sub_df = df[df["Indicator Name"].isin(indicator_lst) &
                df["Country Name"].isin(country_lst)]

    # Drop the country code and Indicator code
    sub_df.drop(["Country Code", "Indicator Code"], axis=1, inplace=True)

    # Drop Nan values from the desired indicator values
    sub_df.dropna(axis=1, inplace=True)

    # Set the index with Country Name and Indicator Name
    year_df = sub_df.set_index(['Country Name', 'Indicator Name'])

    # Create the dataframe having Country Name as column
    country_df = year_df.stack().unstack("Country Name")

    # Returns the two dataframes, one column with country name and another with
    # year
    return year_df, country_df


def cereal_prepcipitation_plot(df):
    '''
    Function defined to illustrate barplots to compare the Average
    precipitation and Cereal Yield for ten selected countries with four
    different years using the four sub plots.
    '''
    # Data for plotting
    sel_lst = ['Cereal yield (kg per hectare)',
               'Average precipitation in depth (mm per year)']
    df_sub = df.loc[(df.index.get_level_values(
        'Indicator Name').isin(sel_lst)), :]

    year_2005 = df_sub["2005"].unstack()
    year_2010 = df_sub["2010"].unstack()
    year_2015 = df_sub["2015"].unstack()
    year_2020 = df_sub["2020"].unstack()

    # Creating subplots
    fig, ax = plt.subplots(2, 2, figsize=(15, 8))

    # Plotting on the second subplot (ax1)
    ax1 = plt.subplot(2, 2, 1)
    year_2005.plot(kind="bar", ax=ax1)
    ax1.set_title("Year 2005")
    ax1.legend()

    # Plotting on the second subplot (ax2)
    ax2 = plt.subplot(2, 2, 2)
    year_2010.plot(kind="bar", ax=ax2)
    ax2.set_title("Year 2010")
    ax2.legend()

    # Plotting on the second subplot (ax3)
    ax3 = plt.subplot(2, 2, 3)
    year_2015.plot(kind="bar", ax=ax3)
    ax3.set_title("Year 2015")
    ax3.legend()

    # Plotting on the second subplot (ax4)
    ax4 = plt.subplot(2, 2, 4)
    year_2020.plot(kind="bar", ax=ax4)
    ax4.set_title("Year 2020")
    ax4.legend()

    # Display the title
    fig.suptitle("Average Precipitation vs Cereal Yield")

    # Display as compact format
    plt.tight_layout()

    # Save the figure
    plt.savefig("cereal.png")

    # Display the graph
    plt.show()


def irrigated_land_plot(df):
    '''
    Function defined to illustrate lineplot using dataframe. With the dataset,
    a lineplot between agricultural irrigated land of ten different countries
    for the past 2 decades is drawn.
    '''
    # Data for plotting
    agr_irr_land = df.loc[(df.index.get_level_values('Indicator Name').isin(
        ["Agricultural irrigated land (% of total agricultural land)"])), :]
    agr_irr_land = agr_irr_land.droplevel("Indicator Name")

    # Calling the plot function to display line plot
    agr_irr_land.T.plot(kind="line")

    # Display the title
    plt.title("Agricultural irrigated land (% of total agricultural land)")

    # Display legend
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Save the figure
    plt.savefig("irrigated_land.png")

    # Display the plot
    plt.show()


def agricultural_land_plot(df):
    '''
    Function defined to illustrate lineplot using dataframe. With the dataset,
    a lineplot between agricultural land of ten different countries for the
    past 2 decades is drawn.
    '''
    # Data for plotting
    agr_irr_land = df.loc[(df.index.get_level_values(
        'Indicator Name').isin(["Agricultural land (% of land area)"])), :]
    agr_irr_land = agr_irr_land.droplevel("Indicator Name")

    # Calling the plot function to display line plot
    agr_irr_land.T.plot(kind="line")

    # Display the title
    plt.title("Agricultural land (% of land area)")

    # Display legend
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Save the figure
    plt.savefig("agricultural_land.png")

    # Display the plot
    plt.show()


def correlation_plot(df, country_name, color_map):
    '''
    Function to create a correlation matrix using the dataframe and a
    country name. It takes the data from the dataframe and draws a heatmap
    representing the inter depencies of indicator names with each other.
    '''
    # Data for plotting
    country_data = df.loc[country_name]
    corr_matrix = country_data.T.corr().fillna(0)

    # Intialization of the figure
    plt.figure(figsize=(6, 6))

    # Calling the imshow function to display plot
    plt.imshow(corr_matrix)

    # Setting the color map
    plt.set_cmap(color_map)

    # Display the color bar
    plt.colorbar()

    # Display text on the matrix
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            plt.text(
                j, i, f"{corr_matrix.iloc[i, j]:.2f}", ha='center', va='center'
                , color='black')

    # Display the title
    plt.title(country_name)

    # Defining the x and y ticks
    plt.xticks(range(len(corr_matrix)), corr_matrix.columns, rotation=90)
    plt.yticks(range(len(corr_matrix)), corr_matrix.columns)

    # Save the figure
    plt.savefig(f"correlation {country_name} .png")

    # Display the plot
    plt.show()


def statistical_method(df, country_name):
    '''
    Function takes a dataframe and country name as arguments
    and gives out some statistical anaylsis (Mean, Standard Deviation...etc) on
    the data with respective to the countries. It also show the dataframe
    describe method which gives out information regarding the data such as
    count, min, max, mean..etc.
    '''
    # Data for plotting
    country_data = df.loc[:, country_name].unstack()
    print(country_data.T.describe())

    # Getting mean and standard deviation from the data
    country_data["Mean"] = country_data.mean(axis=1)
    country_data["Standard Deviation"] = country_data.std(axis=1)

    # Intialization of the figure
    plt.figure(figsize=(6, 3))

    # Calling the plot function to display lineplot
    plt.plot(country_data.index, country_data["Mean"], label="Mean")
    plt.plot(country_data.index, country_data["Standard Deviation"],
             label="Standard Deviation")

    # Define the plot title
    plt.title("Statistical Methods for Country - " + country_name)

    # Axes labelling
    plt.xlabel("Indicator Name")

    # Mention ticks
    plt.xticks(rotation=90)

    # Display grid
    plt.grid()

    # Display legend
    plt.legend()

    # Save the figure
    plt.savefig("statistical.png")

    # Display plot
    plt.show()


def main():
    # Calling read_data function with filename
    year_df, country_df = read_data("API_19_DS2_en_csv_v2_5998250.csv")

    # Calling cereal_precipitation_plot function with year column dataframe
    cereal_prepcipitation_plot(year_df)

    # Calling iririgated_land_plot function with year column dataframe
    irrigated_land_plot(year_df)

    # Calling agricultural_land_plot function with year column dataframe
    agricultural_land_plot(year_df)

    # Calling correlation_plot function with year column dataframe, country
    # name and color map
    correlation_plot(year_df, "India", "Wistia")
    correlation_plot(year_df, "Australia", "tab20b")

    # Calling statistical method function with country column dataframe and
    # country name
    statistical_method(country_df, "India")


if __name__ == "__main__":
    # Calling main program
    main()
