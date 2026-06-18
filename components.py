import dash_bootstrap_components as dbc
from dash import html, dcc

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. create_header
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_demo_banner():
    """Returns the demo mode banner component."""
    return html.Div(
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

def create_header(last_updated="Updated --:-- IST", demo_mode=False):
    """Create the header area with CupPulse title, subtitle, update time, and optional demo banner."""
    banner = None
    if demo_mode:
        banner = create_demo_banner()
        
    header_content = html.Div(
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
                        last_updated,
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
    
    if banner:
        return html.Div([banner, header_content])
    return header_content


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. create_match_card
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_match_card(match):
    """Create a premium, dark-themed match card representing a single match."""
    if not match:
        return html.Div()
        
    status = match.get("status", "scheduled")
    status_display = match.get("status_display", "")
    kickoff_ist_display = match.get("kickoff_ist_display", "")
    venue = match.get("venue", "")
    group = match.get("group", "")
    round_name = match.get("round", "")
    
    home_team = match.get("home_team", {}) or {}
    away_team = match.get("away_team", {}) or {}
    home_name = home_team.get("name", "TBD")
    home_flag = home_team.get("flag", "")
    away_name = away_team.get("name", "TBD")
    away_flag = away_team.get("flag", "")
    
    score = match.get("score", {}) or {}
    home_score = score.get("home")
    away_score = score.get("away")
    
    card_style = {
        "backgroundColor": "#121824",
        "borderRadius": "12px",
        "padding": "16px",
        "border": "1px solid #1E293B",
        "transition": "all 0.3s ease",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.2)",
    }
    
    if status == "live":
        card_style["border"] = "2px solid #10B981"
        card_style["boxShadow"] = "0 0 15px rgba(16, 185, 129, 0.2)"
    elif status == "completed":
        card_style["opacity"] = "0.75"
        card_style["backgroundColor"] = "#0E131F"
        
    header_parts = []
    if group:
        header_parts.append(group)
    if round_name:
        header_parts.append(round_name)
    header_text = " • ".join(header_parts)
    
    header_div = html.Div(
        header_text,
        style={
            "fontSize": "11px",
            "color": "#94A3B8",
            "textTransform": "uppercase",
            "letterSpacing": "1px",
            "marginBottom": "12px",
            "textAlign": "center"
        }
    )
    
    badge_container = []
    if status == "live":
        badge_container.append(
            dbc.Badge(
                "● LIVE",
                color="success",
                className="mb-2",
                style={
                    "backgroundColor": "#10B981",
                    "color": "white",
                    "fontWeight": "bold",
                    "padding": "4px 8px",
                    "borderRadius": "4px",
                    "fontSize": "10px"
                }
            )
        )
        
    if status == "scheduled":
        score_display = "vs"
    else:
        score_display = f"{home_score if home_score is not None else 0} - {away_score if away_score is not None else 0}"
        
    teams_row = dbc.Row(
        [
            # Home Team
            dbc.Col(
                html.Div(
                    [
                        html.Img(
                            src=home_flag, 
                            style={
                                "width": "40px", 
                                "height": "26px", 
                                "objectFit": "cover", 
                                "borderRadius": "4px",
                                "boxShadow": "0 2px 4px rgba(0,0,0,0.3)"
                            }
                        ) if home_flag else html.Div(style={"width": "40px", "height": "26px", "backgroundColor": "#2D3748", "borderRadius": "4px"}),
                        html.Div(
                            home_name, 
                            style={
                                "color": "#F8FAFC", 
                                "fontWeight": "bold", 
                                "fontSize": "13px", 
                                "marginTop": "6px",
                                "textOverflow": "ellipsis",
                                "overflow": "hidden",
                                "whiteSpace": "nowrap"
                            }
                        )
                    ],
                    style={"textAlign": "center"}
                ),
                width=4,
                className="d-flex flex-column align-items-center justify-content-center"
            ),
            
            # Score/vs & Status display
            dbc.Col(
                html.Div(
                    [
                        html.Div(badge_container, style={"display": "flex", "justifyContent": "center"}),
                        html.Div(
                            score_display,
                            style={
                                "color": "#F8FAFC",
                                "fontSize": "22px",
                                "fontWeight": "800",
                                "letterSpacing": "1px",
                                "lineHeight": "1.2"
                            }
                        ),
                        html.Div(
                            status_display,
                            style={
                                "color": "#10B981" if status == "live" else "#94A3B8",
                                "fontSize": "12px",
                                "fontWeight": "600",
                                "marginTop": "4px"
                            }
                        )
                    ],
                    style={"textAlign": "center"}
                ),
                width=4,
                className="d-flex flex-column align-items-center justify-content-center"
            ),
            
            # Away Team
            dbc.Col(
                html.Div(
                    [
                        html.Img(
                            src=away_flag, 
                            style={
                                "width": "40px", 
                                "height": "26px", 
                                "objectFit": "cover", 
                                "borderRadius": "4px",
                                "boxShadow": "0 2px 4px rgba(0,0,0,0.3)"
                            }
                        ) if away_flag else html.Div(style={"width": "40px", "height": "26px", "backgroundColor": "#2D3748", "borderRadius": "4px"}),
                        html.Div(
                            away_name, 
                            style={
                                "color": "#F8FAFC", 
                                "fontWeight": "bold", 
                                "fontSize": "13px", 
                                "marginTop": "6px",
                                "textOverflow": "ellipsis",
                                "overflow": "hidden",
                                "whiteSpace": "nowrap"
                            }
                        )
                    ],
                    style={"textAlign": "center"}
                ),
                width=4,
                className="d-flex flex-column align-items-center justify-content-center"
            ),
        ],
        className="align-items-center justify-content-center my-2"
    )
    
    info_div = html.Div(
        [
            html.Div(
                [
                    html.Span("Kickoff: ", style={"color": "#64748B", "fontSize": "11px"}),
                    html.Span(kickoff_ist_display, style={"color": "#94A3B8", "fontSize": "11px", "fontWeight": "500"})
                ],
                style={"marginBottom": "2px"}
            ) if kickoff_ist_display else None,
            html.Div(
                venue,
                style={
                    "color": "#64748B",
                    "fontSize": "11px",
                    "textOverflow": "ellipsis",
                    "overflow": "hidden",
                    "whiteSpace": "nowrap"
                }
            ) if venue else None
        ],
        style={"marginTop": "12px", "textAlign": "center", "borderTop": "1px solid #1E293B", "paddingTop": "10px"}
    )
    
    card_content = [header_div, teams_row, info_div]
    
    win_prob = match.get("win_probability")
    if win_prob is not None:
        if isinstance(win_prob, dict):
            home_p = win_prob.get("home", 0)
            draw_p = win_prob.get("draw", 0)
            away_p = win_prob.get("away", 0)
            win_prob_elem = html.Div(
                [
                    html.Div("Win Probability", style={"fontSize": "10px", "color": "#64748B", "textAlign": "center", "marginBottom": "6px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                    dbc.Progress(
                        [
                            dbc.Progress(value=home_p, color="primary", bar=True, label=f"{home_p}%" if home_p > 15 else ""),
                            dbc.Progress(value=draw_p, color="secondary", bar=True, label=f"{draw_p}%" if draw_p > 15 else ""),
                            dbc.Progress(value=away_p, color="success", bar=True, label=f"{away_p}%" if away_p > 15 else ""),
                        ],
                        style={"height": "16px", "fontSize": "9px", "borderRadius": "4px", "backgroundColor": "#1E293B"}
                    )
                ],
                style={"marginTop": "12px", "borderTop": "1px solid #1E293B", "paddingTop": "10px"}
            )
        else:
            win_prob_elem = html.Div(
                [
                    html.Span("Win Probability: ", style={"color": "#64748B", "fontSize": "11px"}),
                    html.Span(str(win_prob), style={"color": "#F8FAFC", "fontWeight": "bold", "fontSize": "11px"})
                ],
                style={"marginTop": "12px", "textAlign": "center", "borderTop": "1px solid #1E293B", "paddingTop": "10px"}
            )
        card_content.append(win_prob_elem)
        
    return html.Div(card_content, style=card_style, className="h-100")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. create_match_cards
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_match_cards(matches):
    """Create a responsive grid of match cards."""
    if not matches:
        return create_empty_state("No matches available.")
        
    cols = []
    for match in matches:
        cols.append(
            dbc.Col(
                create_match_card(match),
                xs=12, sm=6, md=6, lg=4, xl=3,
                className="mb-4 d-flex align-items-stretch"
            )
        )
    return dbc.Row(cols, className="g-4")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  4. create_matches_table
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_matches_table(matches, title):
    """Create a dark-themed table display of list of matches."""
    if not matches:
        return html.Div(
            [
                html.H3(title, style={"color": "#F8FAFC", "marginBottom": "16px", "fontWeight": "bold", "fontSize": "20px"}),
                create_empty_state("No match data available.")
            ]
        )
        
    table_headers = [
        html.Th("Time", style={"textAlign": "center", "width": "120px"}),
        html.Th("Match", style={"textAlign": "center"}),
        html.Th("Group/Round", style={"textAlign": "center"}),
        html.Th("Venue", style={"textAlign": "center"}),
        html.Th("Status", style={"textAlign": "center", "width": "120px"}),
    ]
    
    table_rows = []
    for m in matches:
        status = m.get("status", "scheduled")
        status_display = m.get("status_display", "")
        kickoff_ist_display = m.get("kickoff_ist_display", "")
        venue = m.get("venue", "")
        group = m.get("group", "")
        round_name = m.get("round", "")
        
        home = m.get("home_team", {}) or {}
        away = m.get("away_team", {}) or {}
        home_name = home.get("name", "TBD")
        home_flag = home.get("flag", "")
        away_name = away.get("name", "TBD")
        away_flag = away.get("flag", "")
        
        score = m.get("score", {}) or {}
        home_score = score.get("home")
        away_score = score.get("away")
        
        if status == "scheduled":
            score_text = "vs"
        else:
            score_text = f"{home_score if home_score is not None else 0} - {away_score if away_score is not None else 0}"
            
        match_col = html.Div(
            [
                # Home team
                html.Div(
                    [
                        html.Span(home_name, style={"marginRight": "8px", "fontWeight": "600", "color": "#F8FAFC"}),
                        html.Img(src=home_flag, style={"width": "24px", "height": "16px", "objectFit": "cover", "borderRadius": "2px"}) if home_flag else None,
                    ],
                    style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end", "flex": "1", "textAlign": "right"}
                ),
                # Score / vs divider
                html.Div(
                    score_text,
                    style={
                        "fontWeight": "bold", 
                        "color": "#10B981" if status == "live" else "#F8FAFC",
                        "margin": "0 16px",
                        "minWidth": "60px",
                        "textAlign": "center",
                        "fontSize": "15px"
                    }
                ),
                # Away team
                html.Div(
                    [
                        html.Img(src=away_flag, style={"width": "24px", "height": "16px", "objectFit": "cover", "borderRadius": "2px"}) if away_flag else None,
                        html.Span(away_name, style={"marginLeft": "8px", "fontWeight": "600", "color": "#F8FAFC"}),
                    ],
                    style={"display": "flex", "alignItems": "center", "justifyContent": "flex-start", "flex": "1", "textAlign": "left"}
                )
            ],
            style={"display": "flex", "alignItems": "center", "justifyContent": "center", "width": "100%"}
        )
        
        if status == "live":
            status_elem = dbc.Badge(
                status_display or "LIVE",
                color="success",
                style={"backgroundColor": "#10B981", "color": "white", "fontWeight": "bold", "padding": "4px 8px"}
            )
        elif status == "completed":
            status_elem = html.Span(status_display or "FT", style={"color": "#64748B", "fontSize": "13px"})
        else:
            status_elem = html.Span(status_display or "Scheduled", style={"color": "#94A3B8", "fontSize": "13px"})
            
        group_round_text = f"{group} - {round_name}" if group and round_name else (group or round_name or "")
        
        row_style = {"verticalAlign": "middle"}
        if status == "completed":
            row_style["opacity"] = "0.75"
            
        table_rows.append(
            html.Tr(
                [
                    html.Td(kickoff_ist_display or "TBD", style={"textAlign": "center", "color": "#94A3B8"}),
                    html.Td(match_col),
                    html.Td(group_round_text, style={"textAlign": "center", "color": "#94A3B8"}),
                    html.Td(venue or "TBD", style={"textAlign": "center", "color": "#64748B", "fontSize": "13px"}),
                    html.Td(status_elem, style={"textAlign": "center"}),
                ],
                style=row_style
            )
        )
        
    table = dbc.Table(
        [
            html.Thead(html.Tr(table_headers), style={"backgroundColor": "#1E293B"}),
            html.Tbody(table_rows)
        ],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        color="dark",
        style={
            "backgroundColor": "#121824",
            "borderColor": "#1E293B",
            "color": "#F8FAFC",
            "borderRadius": "8px",
            "overflow": "hidden"
        }
    )
    
    return html.Div(
        [
            html.H3(title, style={"color": "#F8FAFC", "marginBottom": "16px", "fontWeight": "bold", "fontSize": "20px"}),
            table
        ],
        style={"marginBottom": "30px"}
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  5. create_standings_section
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_STATUS_COLORS = {
    "qualified": "success",
    "pending": "secondary",
    "in_danger": "warning",
    "must_win": "danger",
    "eliminated": "dark"
}

_STATUS_LABELS = {
    "qualified": "Qualified",
    "pending": "Pending",
    "in_danger": "In Danger",
    "must_win": "Must Win",
    "eliminated": "Eliminated"
}

def create_group_table(group_name, group_data):
    """Create a dark table for a single group standings."""
    if not group_data:
        return html.Div(
            [
                html.H4(group_name, style={"color": "#F8FAFC", "fontWeight": "bold", "fontSize": "16px", "marginBottom": "10px"}),
                html.Div(
                    "Standings not yet available",
                    style={
                        "backgroundColor": "#121824",
                        "border": "1px dashed #2D3748",
                        "borderRadius": "8px",
                        "padding": "20px",
                        "color": "#64748B",
                        "textAlign": "center",
                        "fontSize": "13px"
                    }
                )
            ],
            style={"marginBottom": "24px"}
        )
        
    headers = [
        html.Th("Rank", style={"textAlign": "center", "width": "50px"}),
        html.Th("Team"),
        html.Th("P", style={"textAlign": "center"}),
        html.Th("W", style={"textAlign": "center"}),
        html.Th("D", style={"textAlign": "center"}),
        html.Th("L", style={"textAlign": "center"}),
        html.Th("GF", style={"textAlign": "center"}),
        html.Th("GA", style={"textAlign": "center"}),
        html.Th("GD", style={"textAlign": "center"}),
        html.Th("Pts", style={"textAlign": "center", "fontWeight": "bold"}),
        html.Th("Status", style={"textAlign": "center", "width": "100px"}),
    ]
    
    rows = []
    sorted_data = sorted(group_data, key=lambda x: x.get("rank", 99))
    
    for entry in sorted_data:
        rank = entry.get("rank", "-")
        team = entry.get("team", {}) or {}
        team_name = team.get("name", "TBD")
        team_flag = team.get("flag", "")
        
        played = entry.get("played", 0)
        won = entry.get("won", 0)
        drawn = entry.get("drawn", 0)
        lost = entry.get("lost", 0)
        goals_for = entry.get("goals_for", 0)
        goals_against = entry.get("goals_against", 0)
        goal_difference = entry.get("goal_difference", 0)
        points = entry.get("points", 0)
        qual_status = entry.get("qualification_status", "")
        
        status_badge = None
        if qual_status:
            badge_color = _STATUS_COLORS.get(qual_status, "secondary")
            badge_label = _STATUS_LABELS.get(qual_status, qual_status.capitalize())
            
            custom_badge_style = {"fontSize": "10px", "padding": "3px 6px"}
            if qual_status == "qualified":
                custom_badge_style["backgroundColor"] = "#10B981"
            elif qual_status == "must_win":
                custom_badge_style["backgroundColor"] = "#EF4444"
            elif qual_status == "in_danger":
                custom_badge_style["backgroundColor"] = "#F59E0B"
            elif qual_status == "eliminated":
                custom_badge_style["backgroundColor"] = "#4B5563"
            else:
                custom_badge_style["backgroundColor"] = "#374151"
                
            status_badge = dbc.Badge(
                badge_label,
                color=badge_color,
                style=custom_badge_style
            )
        else:
            status_badge = html.Span("-", style={"color": "#64748B"})
            
        gd_text = f"+{goal_difference}" if goal_difference > 0 else str(goal_difference)
        gd_color = "#10B981" if goal_difference > 0 else ("#EF4444" if goal_difference < 0 else "#94A3B8")
        
        rows.append(
            html.Tr(
                [
                    html.Td(rank, style={"textAlign": "center", "fontWeight": "bold", "color": "#94A3B8"}),
                    html.Td(
                        html.Div(
                            [
                                html.Img(src=team_flag, style={"width": "20px", "height": "14px", "marginRight": "8px", "borderRadius": "2px", "objectFit": "cover"}) if team_flag else None,
                                html.Span(team_name, style={"fontWeight": "600", "color": "#F8FAFC"})
                            ],
                            style={"display": "flex", "alignItems": "center"}
                        )
                    ),
                    html.Td(played, style={"textAlign": "center", "color": "#E2E8F0"}),
                    html.Td(won, style={"textAlign": "center", "color": "#E2E8F0"}),
                    html.Td(drawn, style={"textAlign": "center", "color": "#E2E8F0"}),
                    html.Td(lost, style={"textAlign": "center", "color": "#E2E8F0"}),
                    html.Td(goals_for, style={"textAlign": "center", "color": "#94A3B8", "fontSize": "12px"}),
                    html.Td(goals_against, style={"textAlign": "center", "color": "#94A3B8", "fontSize": "12px"}),
                    html.Td(gd_text, style={"textAlign": "center", "color": gd_color, "fontSize": "12px", "fontWeight": "500"}),
                    html.Td(points, style={"textAlign": "center", "fontWeight": "bold", "color": "#F8FAFC"}),
                    html.Td(status_badge, style={"textAlign": "center"}),
                ],
                style={"verticalAlign": "middle"}
            )
        )
        
    table = dbc.Table(
        [
            html.Thead(html.Tr(headers), style={"backgroundColor": "#1E293B"}),
            html.Tbody(rows)
        ],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        color="dark",
        style={
            "backgroundColor": "#121824",
            "borderColor": "#1E293B",
            "color": "#F8FAFC",
            "borderRadius": "8px",
            "overflow": "hidden",
            "fontSize": "13px"
        }
    )
    
    return html.Div(
        [
            html.H4(group_name, style={"color": "#F8FAFC", "fontWeight": "bold", "fontSize": "16px", "marginBottom": "10px"}),
            table
        ],
        style={"marginBottom": "24px"}
    )

def create_standings_section(standings):
    """Create a structured, side-by-side layout for groups A through L."""
    if not standings:
        standings = {}
        
    group_keys = [f"Group {ch}" for ch in "ABCDEFGHIJKL"]
    cols = []
    
    for group_name in group_keys:
        group_data = standings.get(group_name, [])
        cols.append(
            dbc.Col(
                create_group_table(group_name, group_data),
                xs=12, xl=6,
                className="mb-4"
            )
        )
        
    return dbc.Row(cols, className="g-4")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  6. create_top_scorers_section
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_RANK_MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}
_RANK_COLORS = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}

def create_top_scorers_section(scorers):
    """Create a premium dark-themed Top Scorers / Golden Boot leaderboard."""
    if not scorers:
        return create_empty_state("Top scorer data not yet available.")

    headers = [
        html.Th("Rank", style={"textAlign": "center", "width": "60px"}),
        html.Th("Player"),
        html.Th("Team", style={"textAlign": "center"}),
        html.Th("MP", style={"textAlign": "center", "width": "50px"}),
        html.Th("Goals", style={"textAlign": "center", "width": "70px"}),
        html.Th("Assists", style={"textAlign": "center", "width": "70px"}),
    ]

    rows = []
    for idx, scorer in enumerate(scorers, start=1):
        player = scorer.get("player", {}) or {}
        player_name = player.get("name", "Unknown")

        team = scorer.get("team", {}) or {}
        team_name = team.get("name", "")
        team_flag = team.get("flag", "")

        goals = scorer.get("goals", 0)
        assists = scorer.get("assists", 0)
        matches_played = scorer.get("matches_played", "-")

        # Rank display with medal for top 3
        medal = _RANK_MEDALS.get(idx, "")
        rank_color = _RANK_COLORS.get(idx, "#94A3B8")
        rank_display = html.Span(
            f"{medal} {idx}" if medal else str(idx),
            style={"fontWeight": "bold", "color": rank_color, "fontSize": "14px"}
        )

        # Player name styling — bold gold for #1
        player_style = {
            "fontWeight": "700" if idx <= 3 else "600",
            "color": rank_color if idx <= 3 else "#F8FAFC",
            "fontSize": "14px",
        }

        # Team cell with flag
        team_cell = html.Div(
            [
                html.Img(
                    src=team_flag,
                    style={
                        "width": "20px", "height": "14px",
                        "objectFit": "cover", "borderRadius": "2px",
                        "marginRight": "8px"
                    }
                ) if team_flag else None,
                html.Span(team_name, style={"color": "#94A3B8", "fontSize": "13px"})
            ],
            style={"display": "flex", "alignItems": "center", "justifyContent": "center"}
        )

        # Goals with accent color
        goals_cell = html.Span(
            str(goals),
            style={
                "fontWeight": "bold",
                "color": "#10B981" if goals >= 3 else "#F8FAFC",
                "fontSize": "15px"
            }
        )

        row_style = {"verticalAlign": "middle"}
        if idx <= 3:
            row_style["backgroundColor"] = "rgba(255, 215, 0, 0.03)" if idx == 1 else (
                "rgba(192, 192, 192, 0.03)" if idx == 2 else "rgba(205, 127, 50, 0.03)"
            )

        rows.append(
            html.Tr(
                [
                    html.Td(rank_display, style={"textAlign": "center"}),
                    html.Td(
                        html.Span(player_name, style=player_style)
                    ),
                    html.Td(team_cell),
                    html.Td(
                        str(matches_played),
                        style={"textAlign": "center", "color": "#64748B", "fontSize": "13px"}
                    ),
                    html.Td(goals_cell, style={"textAlign": "center"}),
                    html.Td(
                        str(assists),
                        style={"textAlign": "center", "color": "#94A3B8", "fontSize": "13px"}
                    ),
                ],
                style=row_style
            )
        )

    table = dbc.Table(
        [
            html.Thead(html.Tr(headers), style={"backgroundColor": "#1E293B"}),
            html.Tbody(rows)
        ],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        color="dark",
        style={
            "backgroundColor": "#121824",
            "borderColor": "#1E293B",
            "color": "#F8FAFC",
            "borderRadius": "8px",
            "overflow": "hidden",
            "fontSize": "13px"
        }
    )

    return html.Div(
        [
            html.Div(
                [
                    html.Span("⚽", style={"fontSize": "20px", "marginRight": "10px"}),
                    html.Span("Golden Boot Race", style={
                        "fontSize": "16px", "fontWeight": "bold", "color": "#FFD700",
                        "letterSpacing": "0.5px"
                    })
                ],
                style={"display": "flex", "alignItems": "center", "marginBottom": "16px"}
            ),
            table
        ]
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  7. create_empty_state
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_empty_state(message):
    """Create a beautiful dark empty state panel with a customizable message."""
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        "ℹ", 
                        style={
                            "fontSize": "32px", 
                            "color": "#64748B", 
                            "marginBottom": "12px"
                        }
                    ),
                    html.P(
                        message,
                        style={
                            "color": "#94A3B8",
                            "fontSize": "14px",
                            "margin": 0
                        }
                    )
                ],
                style={
                    "textAlign": "center",
                    "padding": "30px 20px",
                    "backgroundColor": "#121824",
                    "border": "1px dashed #2D3748",
                    "borderRadius": "8px"
                }
            )
        ],
        className="my-3"
    )
