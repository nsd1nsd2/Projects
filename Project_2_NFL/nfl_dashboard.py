"""
Name: Roshan Peri/Freddy Elyas 
File: nfl_dashboard.py 
Purpose: Backend code for the dashboard
"""

import panel as pn
import sys 
import matplotlib.pyplot as plt 
#sys.path.append(r'Classwork\Sankey\Sankey_Code')
sys.path.append('Classwork/Sankey/Sankey_Code')

from nflapi import NFLAPI
nfl = NFLAPI()
# Loads javascript dependencies and configures Panel (required)
pn.extension()
#data = nfl.load_nfl(r'Homework\Homework_3\Data\nfl-team-statistics.csv')
data = nfl.load_nfl('Homework/Homework_3/Data/nfl-team-statistics.csv')

# WIDGET DECLARATIONS

# Search Widgets
team = pn.widgets.Select(name='Team',options=nfl.get_team(), value= 'PHI')
year = pn.widgets.IntRangeSlider(name = 'Year', start = 1999, end = 2022, value = (2000,2010), step = 1)
fig_width = pn.widgets.IntSlider(name='Figure Width', start=1, end=20, value=10)
fig_height = pn.widgets.IntSlider(name='Figure Height', start=1, end=10, value=5)
all_team = pn.widgets.Checkbox(name = "Show all Teams", value = False)
color_picker = pn.widgets.ColorPicker(name = "Plot Colors", value = '#99ef78')
stat = pn.widgets.Select(
    name='Statistic',
    options=[
        'offense_total',
        'defensive_total',
        'points_scored',
        'points_allowed',
        'wins'
    ],
    value='offense_total'
)
#Data Widgets 
nfl_df = pn.pane.DataFrame(data)


# Plotting widgets




# CALLBACK FUNCTIONS
"""
Creating callback funtions for each of the aspects of the dashboard 
"""
def get_team(team, year,check):
    team_df = nfl.filtered_df(team, year, check)
    return pn.pane.DataFrame(team_df)
def offensive(team, year, fig_width, fig_height, stat, color):
    plot = nfl.barplot(team, year, fig_width, fig_height, stat,color)
    return pn.pane.Matplotlib(plot)
def trend_plot(team, year, fig_width, fig_height, stat, color):
    trend_plot = nfl.trend(team, year, fig_width, fig_height, stat, color )
    return pn.pane.Matplotlib(trend_plot)
# CALLBACK BINDINGS (Connecting widgets to callback functions)

team_data = pn.bind(get_team, team, year,all_team)
offensive_plot = pn.bind(offensive, team, year, fig_width, fig_height, stat, color_picker)
trends = pn.bind(trend_plot,team, year, fig_width, fig_height, stat, color_picker)
# DASHBOARD WIDGET CONTAINERS ("CARDS")
card_width = 320

search_card = pn.Card(
    pn.Column(
        # Widget 1
        team,
        # Widget 2
        year,
        # Widget 3
        stat,
        all_team
        
    ),
    title="Search", width=card_width, collapsed=False
)


plot_card = pn.Card(
    pn.Column(
        # Widget 1
        fig_width,
        fig_height, 
        color_picker
        # Widget 2
        # Widget 3
    ),

    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="Interactive NFL Data",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme = "dark",
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Dataset", team_data),  # Replace None with callback binding
            ("Bar Plot", offensive_plot),  # Replace None with callback binding
            ("Trend Plot", trends),
            active=1  # Which tab is active by default?
        )

    ],
    header_background='blue'

).servable()

layout.show()
