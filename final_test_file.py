"""
Name: Roshan Peri, Justian Liao, Kevin Ohgami
File: final_test_file.py
Purpose: Create all the bar graphs and line graphs necessary for the final article
"""
#import statements
import matplotlib.pyplot as plt 
import statistics as sta
import calendar
import seaborn as sns 
months = []
#appends the months of the year to be used later in the program
for i in range(1,13):
        months.append(calendar.month_name[i])

def read_file_yearly(filename):
    """
    Purpose: Reads the data file according to which 
    year is inputted, adds it to a dictionary with the 
    being the country and the value being a list of all 
    emissions recorded for the 12 months. 
    It then proceeds to return the resulting dictionary
    """
    year_emission = {
        
    }
    #opens the file 
    file = open(filename, 'r')
    line = file.readline().strip()
    #reads through the file 
    for line in file: 
        val = line.split(',')
        country = val[2].lower().capitalize()
        emission = val[4]
        #adds the assigned values to a dictonary
        if country not in year_emission:
            year_emission[country] = []
        if emission not in country:
            year_emission[country].append(float(emission))
    #sifts through the dictionary and removes countries that don't have data for 12 months 
    for key in list(year_emission.keys()):
        if len(year_emission[key]) != 12:
            del year_emission[key]
    emission = year_emission
    return year_emission

def visual_yearly(year):
    """
    Purpose: Takes whatever year data the user inputs 
    and creates a bar graph of the yearly average of the 
    emissios and plots them all next to each other to see
    how each country compares to the other. It then proceeds
    to print out the corresponding bar graph. 
    """
    year_emission = {

    }
    country = []
    average = []
    #assigns the local dictionary the data 
    year_emission = read_file_yearly(year)
    #appends the country and then appends the average of all the months and adds to list 
    for key, value in year_emission.items():
        country.append(key)
        average.append(sta.mean(value))
    plt.figure(figsize=(12,6), dpi=200)
    #plots figure
    sns.barplot(x = country, y = average, palette='magma')
    #adds the data points on the graph
    for i in range(len(country)):
        plt.text(i,average[i],round(average[i]), ha='center', va='bottom',fontsize=5)
    plt.ylabel("Average emission in pounds")
    plt.xlabel("Countries")
    if year == "2020.csv":
        plt.title("Yearly Average of CO2 Emission in 2020" )
    if year == "2021.csv":
        plt.title("Yearly Average of CO2 Emission in 2021" )
    if year == "2022.csv":
        plt.title("Yearly Average of CO2 Emission in 2022" )
    if year == "2023.csv":
        plt.title("Yearly Average of CO2 Emission in 2023" )
    plt.yscale('log')
    plt.xticks(rotation = 90)
    plt.savefig(year + '.png', bbox_inches = 'tight')
    plt.show()
    
def visual_monthly(year, country):
    """
    Purpose: Creates a bargraph of an in-depth 
    look at the yearly breakdown for any country that 
    the user specifies in the parameters along with 
    any year that the user specifies. The data is processed from
    the read_file_yearly and is used in this function. It then 
    prints the corresponding bar graph. For the parameters,
    it takes in the year which user wants to use along with the country
    they would like to collect data from.
    """
    month_emission = {

    }
    
    month_emission = read_file_yearly(year)
    plt.figure(figsize=(12,6),dpi=200)
    sns.barplot(x=months,y=month_emission[country], palette= 'rocket')
    #labels each of the data points 
    for i in range(len(month_emission[country])):
        plt.text(i,month_emission[country][i], round(month_emission[country][i]), ha='center', va='bottom',fontsize = 8)
    if year == "2020.csv":
        plt.title(country.lower().capitalize()+"'s 2020 Average CO2 Usage Per Month")
    if year == "2021.csv":
        plt.title(country.lower().capitalize()+"'s 2021 Average CO2 Usage Per Month")
    if year == '2022.csv':
        plt.title(country.lower().capitalize()+"'s 2022 Average CO2 Usage Per Month")
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel("Amount in tons")
    plt.xticks(fontsize = 8)
    plt.xlabel("Months")
    plt.savefig(country + year +'.png')
    plt.show()

def plot_style(year,season,country):
    """
    Purpose: General plotting style points so 
    user does not need to repeat the same lines 
    of code multiple times. Takes in the year,season,country
    to help name the grapshs
    """
    
    plt.xlabel("Months")
    if year == "2020.csv" and season == "winter":
        plt.title(country + "'s 2020 Winter Seasonal CO2 Emissions")
    if year == "2020.csv" and season == "spring":
        plt.title(country + "'s 2020 Spring Seasonal CO2 Emissions")
    if year == "2020.csv" and season == "summer":
        plt.title(country + "'s 2020 Summer Seasonal CO2 Emissions")
    if year == "2020.csv" and season == "winter":
        plt.title(country + "'s 2020 Winter Seasonal CO2 Emissions")
    
    if year == "2021.csv" and season == "winter":
        plt.title(country + "'s 2021 Winter Seasonal CO2 Emissions")
    if year == "2021.csv" and season == "spring":
        plt.title(country + "'s 2021 Spring Seasonal CO2 Emissions")
    if year == "2021.csv" and season == "summer":
        plt.title(country + "'s 2021 Summer Seasonal CO2 Emissions")
    if year == "2021.csv" and season == "fall":
        plt.title(country + "'s 2021 Fall Seasonal CO2 Emissions")
    
    if year == "2022.csv" and season == "winter":
        plt.title(country + "'s 2022 Winter Seasonal CO2 Emissions")
    if year == "2022.csv" and season == "spring":
        plt.title(country + "'s 2022 Spring Seasonal CO2 Emissions")
    if year == "2022.csv" and season == "summer":
        plt.title(country + "'s 2022 Summer Seasonal CO2 Emissions")
    if year == "2022.csv" and season == "fall":
        plt.title(country + "'s 2022 Fall Seasonal CO2 Emissions")
    
    if year == "2023.csv" and season == "winter":
        plt.title(country + "'s 2023 Winter Seasonal CO2 Emissions")
    if year == "2023.csv" and season == "spring":
        plt.title(country + "'s 2023 Spring Seasonal CO2 Emissions")
    if year == "2023.csv" and season == "summer":
        plt.title(country + "'s 2023 Summer Seasonal CO2 Emissions")
    if year == "2023.csv" and season == "fall":
        plt.title(country + "'s 2023 Fall Seasonal CO2 Emissions")
    plt.ylabel("Average Amount Burned in Tonnes", size = 10)
    plt.ticklabel_format(style='plain', axis='y')
    plt.savefig(country + season + year + '.png')
    plt.show()

def visual_seasonal(year,season,country):
    """
    Purpose: Creates a bar graph of emissions on a seasonal basis 
    for any country in any year. User inputs what year, season and country 
    they would like and a graph that shows the seasonal breakdown is produced 
    and returned. 
    """
    seasonal_emission = {

    }
    #labeling the seasons 
    seasonal_winter = ['December', 'January','February']
    seasonal_spring = ['March', 'April','May']
    seasonal_summer = ['June', 'July', 'August']
    seasonal_fall = ['September', 'October','November']
    seasonal_emission = read_file_yearly(year)
    #parameters to correctly graph based on parameters inputed 
    if season == "winter":
        plt.figure(figsize=(10,6),dpi=200)
        sns.barplot(x=seasonal_winter, y=seasonal_emission[country][0:3], palette="mako")
        plot_style(year,season,country)
    if season == "spring":
        plt.figure(figsize=(10,6),dpi=200)
        sns.barplot(x=seasonal_spring, y=seasonal_emission[country][3:6], palette='crest')
        plot_style(year,season,country)
    if season == "summer":
        plt.figure(figsize=(10,6),dpi=200)
        sns.barplot(x=seasonal_summer, y=seasonal_emission[country][6:9], palette='magma')
        plot_style(year,season,country)
    if season == 'fall':
        plt.figure(figsize=(10,6),dpi=200)
        sns.barplot(x=seasonal_fall, y=seasonal_emission[country][9:12],palette='flare')
        plot_style(year,season,country)

def line_graph(year1,year2,year3,country):
    """
    Purpose: creates a line graph with data from 
    all three years for a monthly breakdown as well.
    Takes in the years the user would like to see and 
    a specific country and a line graph is outputted 
    with the x-axis being the months and the points being 
    each of the emissions produced from that month. 
    """
    #setting dictionaries for all the data for each year 
    line_month1 = {

    }
    line_month2 = {

    }
    line_month3 = {

    }
    line_month1 = read_file_yearly(year1)
    line_month2 = read_file_yearly(year2)
    line_month3 = read_file_yearly(year3)
    #plotting/general plotting techniques 
    plt.figure(figsize=(12,6), dpi=200)
    sns.lineplot(x=months,y=line_month1[country], label = '2020')
    sns.lineplot(x=months,y=line_month2[country], label = '2021')
    sns.lineplot(x=months,y=line_month3[country], label = '2022')
    plt.xlabel('Months')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Emissions Emitted in Tons')
    plt.title(country+"'s Monthly CO2 Emissions Per Year")
    plt.grid()
    plt.legend()
    plt.savefig(country + " Yearly_Breakdown.png")
    plt.show()
def main():
    visual_seasonal('2022.csv','winter','United kingdom')
    visual_seasonal('2022.csv','summer','United kingdom')
    line_graph('2020.csv','2021.csv','2022.csv','Germany')
    line_graph('2020.csv','2021.csv','2022.csv','Albania')
    line_graph('2020.csv','2021.csv','2022.csv','France')
    visual_yearly("2020.csv")
    visual_yearly("2021.csv")
    visual_yearly("2022.csv")
    visual_monthly('2021.csv', "Albania")
    visual_monthly('2021.csv', "Germany")
    visual_monthly('2021.csv', "France")
main()