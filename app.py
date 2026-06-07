import os
os.environ.pop("SSLKEYLOGFILE", None)

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from dotenv import load_dotenv
import pytz
from datetime import datetime

from components import create_header, create_match_cards, create_matches_table, create_standings_section, create_empty_state
from data_store import (
    get_smart_match_cards,
    get_today_matches,
    get_live_matches,
    get_upcoming_matches,
    get_completed_matches,
    get_standings
)

load_dotenv()

# Helper function for IST update time
def get_current_ist_time():
    """Return current IST time formatted as 'Updated HH:MM IST'."""
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    return now.strftime("Updated %H:%M IST")

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

server = app.server

# Initial layout construction
app.layout = html.Div(
    style={
        "backgroundColor": "#0A0E1A",
        "minHeight": "100vh",
        "color": "#F8FAFC",
    },
    children=[
        # Interval timers for auto-refresh
        dcc.Interval(id="live-interval", interval=60*1000, n_intervals=0),
        dcc.Interval(id="standard-interval", interval=10*60*1000, n_intervals=0),

        # Header Wrapper
        html.Div(
            [
                # Container for Demo Mode Banner
                html.Div(
                    id="demo-mode-banner",
                    children=html.Div(
                        "⚠ Demo Mode — Live data unavailable. Showing sample data.",
                        style={
                            "backgroundColor": "#D97706",
                            "color": "#FFFFFF",
                            "textAlign": "center",
                            "padding": "8px 16px",
                            "fontWeight": "bold",
                            "fontSize": "14px",
                            "width": "100%",
                        }
                    )
                ),
                
                # Header main content
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H1(
                                        "CupPulse 2026",
                                        style={
                                            "color": "#F8FAFC",
                                            "fontWeight": "bold",
                                            "fontSize": "28px",
                                            "margin": 0
                                        }
                                    ),
                                    html.P(
                                        "Real-Time FIFA World Cup Intelligence Dashboard",
                                        style={
                                            "color": "#94A3B8",
                                            "fontSize": "14px",
                                            "margin": 0,
                                            "marginTop": "4px"
                                        }
                                    )
                                ],
                                xs=12, md=8,
                                style={"textAlign": "left"}
                            ),
                            dbc.Col(
                                html.Div(
                                    id="header-last-updated",
                                    children=get_current_ist_time(),
                                    style={
                                        "color": "#94A3B8",
                                        "fontSize": "13px",
                                        "fontWeight": "500",
                                        "height": "100%",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "flex-end"
                                    }
                                ),
                                xs=12, md=4,
                                className="mt-2 mt-md-0"
                            )
                        ],
                        align="center",
                        className="w-100 m-0"
                    ),
                    style={
                        "backgroundColor": "#0F172A",
                        "borderBottom": "1px solid #1E293B",
                        "padding": "20px 24px"
                    }
                )
            ]
        ),
        
        # Main Dashboard Container
        dbc.Container(
            [
                # Featured Matches Section
                html.Div(
                    [
                        html.H2(
                            "Featured Matches", 
                            style={
                                "color": "#F8FAFC", 
                                "marginBottom": "20px", 
                                "fontWeight": "bold", 
                                "fontSize": "22px"
                            }
                        ),
                        html.Div(
                            id="match-cards-container",
                            children=create_match_cards(get_smart_match_cards())
                        )
                    ],
                    style={"marginTop": "30px", "marginBottom": "40px"}
                ),
                
                # Live Scores Table Section
                html.Div(
                    id="live-scores-section",
                    children=create_matches_table(get_live_matches(), "Live Matches") if get_live_matches() else html.Div(
                        [
                            html.H3("Live Matches", style={"color": "#F8FAFC", "marginBottom": "16px", "fontWeight": "bold", "fontSize": "20px"}),
                            create_empty_state("No live matches at the moment.")
                        ]
                    ),
                    style={"marginBottom": "30px"}
                ),
                
                # Today, Upcoming, and Completed Matches Tables
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    id="today-matches-table",
                                    children=create_matches_table(get_today_matches(), "Today's Matches")
                                ),
                                html.Div(
                                    id="upcoming-matches-table",
                                    children=create_matches_table(get_upcoming_matches(), "Upcoming Matches")
                                ),
                                html.Div(
                                    id="completed-matches-table",
                                    children=create_matches_table(get_completed_matches(), "Completed Matches")
                                ),
                            ],
                            xs=12
                        )
                    ]
                ),
                
                # Group Standings Section
                html.Div(
                    [
                        html.H2(
                            "Group Standings", 
                            style={
                                "color": "#F8FAFC", 
                                "marginBottom": "20px", 
                                "fontWeight": "bold", 
                                "fontSize": "22px"
                            }
                        ),
                        html.Div(
                            id="standings-section",
                            children=create_standings_section(get_standings())
                        )
                    ],
                    style={"marginTop": "40px", "paddingBottom": "50px"}
                )
            ],
            fluid=True,
            style={"maxWidth": "1400px", "padding": "0 24px"}
        )
    ]
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Callbacks
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Callback 1: Live Interval Refresh (every 60 seconds)
@app.callback(
    [
        Output("match-cards-container", "children"),
        Output("live-scores-section", "children"),
        Output("header-last-updated", "children"),
        Output("demo-mode-banner", "children"),
    ],
    [Input("live-interval", "n_intervals")]
)
def refresh_live_data(n_intervals):
    """Update featured matches, live matches list, header timestamp, and demo banner."""
    # 1. Match Cards
    smart_cards = create_match_cards(get_smart_match_cards())
    
    # 2. Live Scores Section
    live_matches = get_live_matches()
    if live_matches:
        live_section = create_matches_table(live_matches, "Live Matches")
    else:
        live_section = html.Div(
            [
                html.H3("Live Matches", style={"color": "#F8FAFC", "marginBottom": "16px", "fontWeight": "bold", "fontSize": "20px"}),
                create_empty_state("No live matches at the moment.")
            ]
        )
        
    # 3. Header Timestamp
    timestamp = get_current_ist_time()
    
    # 4. Demo Mode Banner
    demo_banner = html.Div(
        "⚠ Demo Mode — Live data unavailable. Showing sample data.",
        style={
            "backgroundColor": "#D97706",
            "color": "#FFFFFF",
            "textAlign": "center",
            "padding": "8px 16px",
            "fontWeight": "bold",
            "fontSize": "14px",
            "width": "100%",
        }
    )
    
    return smart_cards, live_section, timestamp, demo_banner


# Callback 2: Standard Interval Refresh (every 10 minutes)
@app.callback(
    [
        Output("today-matches-table", "children"),
        Output("upcoming-matches-table", "children"),
        Output("completed-matches-table", "children"),
        Output("standings-section", "children"),
    ],
    [Input("standard-interval", "n_intervals")]
)
def refresh_standard_data(n_intervals):
    """Update general tables (Today's, Upcoming, Completed) and Group Standings."""
    today = create_matches_table(get_today_matches(), "Today's Matches")
    upcoming = create_matches_table(get_upcoming_matches(), "Upcoming Matches")
    completed = create_matches_table(get_completed_matches(), "Completed Matches")
    standings = create_standings_section(get_standings())
    return today, upcoming, completed, standings


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8050)
