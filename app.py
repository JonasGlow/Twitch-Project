# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Usable?

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('data/Top100Combined.csv')

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h")
)

# Get summary data
def getSummary():
    # Get unique number of streamers
    streamers = df['user_id'].nunique()

    # Get average number of viewers
    viewers = df['viewer_count'].mean().round(0)

    # Get average number of followers
    followers = df['follower_count'].mean().round(0)

    return streamers, viewers, followers

# Make top 20 streamers table
def makeTopStreamersTable():
    return 0

# Make timeseries graph over the summed viewercount over the timeslots
def makeSumViewersGraph():

    fig = px.line(df, x='timestamp', y="GOOG")
    return fig

# Make timeseries graph of the top streams over the time period
def makeTimeSeriesTopStreams():
    # fig = px.line(df, x="date", y=df.columns, hover_data={"date": "|%B %d, %Y"}, title='Development of the Top 10 Streamers over the Time Period')
    return 0
# VIELLEICHT ALS RANKING VERLAUF ALSO STREAMER NAMEN REIN UND RAUS

# Graph 3
def makeLanguageDistribution():
    fig = px.pie(df, values='user_id', names='language', title='Language Distribution')
    return fig

# Graph 4
def makeFollowerGraph():
    fig = px.bar(df, x='follower_count', y='user_name', title='Most Followers')
    return fig

# Graph 5
def make_graph5():
    return 0

# Graph 6
def make_graph6():
    return 0

# Graph 7
def make_graph7():
    return 0

# Graph 8
def make_graph8():
    return 0


# Create app layout
app.layout = html.Div(
    [
    # Header-start    
    html.Div(
        [
            html.H3(
                "Top 100 Streams on Twitch from the 22-08-2020",
                style={'margin-bottom': '0px', 'margin-top': '25px', 'text-align': 'center'},
            ),
            html.H6(
                "Data Overview", style={'margin-top': '0px', 'text-align': 'center'}
            ),
        ]    
    ),


    # Section-start (Block with summary)
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [html.H6(getSummary()[0]), html.P("Number of Streamers")],
                        id='streamers',
                        className="pretty_container columns",
                    ),
                    html.Div(
                        [html.H6(getSummary()[1]), html.P("Average Viewer Count")],
                        id='viewers',
                        className="pretty_container columns",
                    ),
                    html.Div(
                        [html.H6(getSummary()[2]), html.P("Average Follower Count")],
                        id='followers',
                        className="pretty_container columns",
                    ),
                ],
                className="row flex-display",
            ),
        ]
    ),
    # Section-end

    # Table (Vielleicht nicht table sondern was anderes?)
    html.Div(
        [
            html.Div(
                [   
                   html.Div(
                        [html.H6(id=""), html.P("Top 20 Streamers Table")],
                        className="pretty_container columns",
                    ),
                ],
                className="row flex-display",
            ),
        ]
    ),
    # Section-end

    # Sum of Viewercount of the timeslots
    html.Div(
        [
            html.Div(
                [   
                    html.Div(
                        [dcc.Graph(id="main-graph", figure = makeSumViewersGraph())],
                        className="pretty_container columns",
                    ),
                ],
                className="row flex-display",
            ),
        ]
    ),
    # Section-end

    # Development top 10 streams over the timeslots
    html.Div(
        [
            html.Div(
                [   
                    html.Div(
                        [dcc.Graph(id="main-graph", figure = makeTimeSeriesTopStreams())],
                        className="pretty_container columns",
                    ),
                ],
                className="row flex-display",
            ),
        ]
    ),
    # Section-end

    # Section-start 
    html.Div(
        [
            html.Div(
                [   
                    # Languages distribution TODO FIX POPUP
                    html.Div(
                        [dcc.Graph(id="", figure = makeLanguageDistribution())],
                        className="pretty_container columns",
                    ),
                    # Followercount distribution
                    html.Div(
                        [dcc.Graph(id="", figure = makeFollowerGraph())],
                        className="pretty_container columns",
                    ),
                ],
                className="row flex-display",
            ),
        ]
    ),
    # Section-end



    # Section-start (Clip-Data)
    html.Div(
        [
            html.Div(
                [   
                    # Graph 1
                    html.Div(
                        [dcc.Graph(id="", figure = makeTimeSeriesTopStreams())],
                        className="pretty_container columns",
                    ),
                    # Graph 1
                    html.Div(
                        [dcc.Graph(id="", figure = makeTimeSeriesTopStreams())],
                        className="pretty_container columns",
                    ),
                ],
                className="row flex-display",
            ),
        ]
    ),
    # Section-end


    # Section-start (Video-Data)
    html.Div(
        [
            html.Div(
                [   
                    # Graph 1
                    html.Div(
                        [dcc.Graph(id="", figure = makeTimeSeriesTopStreams())],
                        className="pretty_container columns",
                    ),
                    # Graph 1
                    html.Div(
                        [dcc.Graph(id="", figure = makeTimeSeriesTopStreams())],
                        className="pretty_container columns",
                    ),
                ],
                className="row flex-display",
            ),
        ]
    ),
    # Section-end

    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)
