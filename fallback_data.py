"""
Fallback / demo data for the FIFA World Cup 2026 Dashboard.
Used when the live API is unavailable or during development.

World Cup 2026 format:
  - 48 teams, 12 groups (A–L), 4 teams per group
  - Top 2 from each group + 8 best third-place teams → Round of 32
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Individual match objects
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_MATCH_LIVE = {
    "fixture_id": 1001,
    "status": "live",
    "status_short": "2H",
    "status_display": "74'",
    "home_team": {
        "id": 26,
        "name": "Argentina",
        "flag": "https://media.api-sports.io/flags/ar.svg",
    },
    "away_team": {
        "id": 2,
        "name": "France",
        "flag": "https://media.api-sports.io/flags/fr.svg",
    },
    "score": {"home": 2, "away": 1},
    "venue": "MetLife Stadium, East Rutherford",
    "kickoff_utc": "2026-06-21T18:00:00Z",
    "kickoff_ist": "2026-06-21T23:30:00+05:30",
    "kickoff_ist_display": "23:30 IST",
    "round": "Group Stage - Round 1",
    "group": "Group C",
    "win_probability": None,
    "importance_score": 9,
    "events": [],
}

_MATCH_SCHEDULED_1 = {
    "fixture_id": 1002,
    "status": "scheduled",
    "status_short": "NS",
    "status_display": "23:30 IST",
    "home_team": {
        "id": 6,
        "name": "Brazil",
        "flag": "https://media.api-sports.io/flags/br.svg",
    },
    "away_team": {
        "id": 25,
        "name": "Germany",
        "flag": "https://media.api-sports.io/flags/de.svg",
    },
    "score": {"home": 0, "away": 0},
    "venue": "AT&T Stadium, Arlington",
    "kickoff_utc": "2026-06-22T18:00:00Z",
    "kickoff_ist": "2026-06-22T23:30:00+05:30",
    "kickoff_ist_display": "23:30 IST",
    "round": "Group Stage - Round 1",
    "group": "Group D",
    "win_probability": None,
    "importance_score": 10,
    "events": [],
}

_MATCH_SCHEDULED_2 = {
    "fixture_id": 1003,
    "status": "scheduled",
    "status_short": "NS",
    "status_display": "02:30 IST",
    "home_team": {
        "id": 9,
        "name": "Spain",
        "flag": "https://media.api-sports.io/flags/es.svg",
    },
    "away_team": {
        "id": 27,
        "name": "Portugal",
        "flag": "https://media.api-sports.io/flags/pt.svg",
    },
    "score": {"home": 0, "away": 0},
    "venue": "SoFi Stadium, Inglewood",
    "kickoff_utc": "2026-06-22T21:00:00Z",
    "kickoff_ist": "2026-06-23T02:30:00+05:30",
    "kickoff_ist_display": "02:30 IST",
    "round": "Group Stage - Round 1",
    "group": "Group E",
    "win_probability": None,
    "importance_score": 9,
    "events": [],
}

_MATCH_COMPLETED_1 = {
    "fixture_id": 1004,
    "status": "completed",
    "status_short": "FT",
    "status_display": "Full Time",
    "home_team": {
        "id": 10,
        "name": "England",
        "flag": "https://media.api-sports.io/flags/gb.svg",
    },
    "away_team": {
        "id": 2384,
        "name": "USA",
        "flag": "https://media.api-sports.io/flags/us.svg",
    },
    "score": {"home": 1, "away": 0},
    "venue": "Estadio Azteca, Mexico City",
    "kickoff_utc": "2026-06-20T15:00:00Z",
    "kickoff_ist": "2026-06-20T20:30:00+05:30",
    "kickoff_ist_display": "20:30 IST",
    "round": "Group Stage - Round 1",
    "group": "Group B",
    "win_probability": None,
    "importance_score": 8,
    "events": [],
}

_MATCH_COMPLETED_2 = {
    "fixture_id": 1005,
    "status": "completed",
    "status_short": "FT",
    "status_display": "Full Time",
    "home_team": {
        "id": 12,
        "name": "Japan",
        "flag": "https://media.api-sports.io/flags/jp.svg",
    },
    "away_team": {
        "id": 3,
        "name": "Croatia",
        "flag": "https://media.api-sports.io/flags/hr.svg",
    },
    "score": {"home": 2, "away": 1},
    "venue": "BMO Field, Toronto",
    "kickoff_utc": "2026-06-20T18:00:00Z",
    "kickoff_ist": "2026-06-20T23:30:00+05:30",
    "kickoff_ist_display": "23:30 IST",
    "round": "Group Stage - Round 1",
    "group": "Group F",
    "win_probability": None,
    "importance_score": 7,
    "events": [],
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Aggregated match lists
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEMO_MATCHES = [
    _MATCH_LIVE,
    _MATCH_SCHEDULED_1,
    _MATCH_SCHEDULED_2,
    _MATCH_COMPLETED_1,
    _MATCH_COMPLETED_2,
]

DEMO_LIVE = [_MATCH_LIVE]

DEMO_UPCOMING = [_MATCH_SCHEDULED_1, _MATCH_SCHEDULED_2]

DEMO_COMPLETED = [_MATCH_COMPLETED_1, _MATCH_COMPLETED_2]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Group Standings  (Groups A & B populated; C–L empty)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEMO_STANDINGS = {
    "Group A": [
        {
            "team": {
                "id": 16,
                "name": "Mexico",
                "flag": "https://media.api-sports.io/flags/mx.svg",
            },
            "group": "Group A",
            "rank": 1,
            "played": 2,
            "won": 2,
            "drawn": 0,
            "lost": 0,
            "goals_for": 4,
            "goals_against": 1,
            "goal_difference": 3,
            "points": 6,
            "form": "WW",
            "qualification_status": "qualified",
        },
        {
            "team": {
                "id": 31,
                "name": "Morocco",
                "flag": "https://media.api-sports.io/flags/ma.svg",
            },
            "group": "Group A",
            "rank": 2,
            "played": 2,
            "won": 1,
            "drawn": 1,
            "lost": 0,
            "goals_for": 3,
            "goals_against": 1,
            "goal_difference": 2,
            "points": 4,
            "form": "WD",
            "qualification_status": "pending",
        },
        {
            "team": {
                "id": 1500,
                "name": "Canada",
                "flag": "https://media.api-sports.io/flags/ca.svg",
            },
            "group": "Group A",
            "rank": 3,
            "played": 2,
            "won": 0,
            "drawn": 1,
            "lost": 1,
            "goals_for": 1,
            "goals_against": 2,
            "goal_difference": -1,
            "points": 1,
            "form": "DL",
            "qualification_status": "in_danger",
        },
        {
            "team": {
                "id": 2382,
                "name": "Ecuador",
                "flag": "https://media.api-sports.io/flags/ec.svg",
            },
            "group": "Group A",
            "rank": 4,
            "played": 2,
            "won": 0,
            "drawn": 0,
            "lost": 2,
            "goals_for": 0,
            "goals_against": 4,
            "goal_difference": -4,
            "points": 0,
            "form": "LL",
            "qualification_status": "eliminated",
        },
    ],
    "Group B": [
        {
            "team": {
                "id": 10,
                "name": "England",
                "flag": "https://media.api-sports.io/flags/gb.svg",
            },
            "group": "Group B",
            "rank": 1,
            "played": 1,
            "won": 1,
            "drawn": 0,
            "lost": 0,
            "goals_for": 1,
            "goals_against": 0,
            "goal_difference": 1,
            "points": 3,
            "form": "W",
            "qualification_status": "pending",
        },
        {
            "team": {
                "id": 13,
                "name": "Senegal",
                "flag": "https://media.api-sports.io/flags/sn.svg",
            },
            "group": "Group B",
            "rank": 2,
            "played": 1,
            "won": 1,
            "drawn": 0,
            "lost": 0,
            "goals_for": 2,
            "goals_against": 1,
            "goal_difference": 1,
            "points": 3,
            "form": "W",
            "qualification_status": "pending",
        },
        {
            "team": {
                "id": 17,
                "name": "South Korea",
                "flag": "https://media.api-sports.io/flags/kr.svg",
            },
            "group": "Group B",
            "rank": 3,
            "played": 1,
            "won": 0,
            "drawn": 0,
            "lost": 1,
            "goals_for": 1,
            "goals_against": 2,
            "goal_difference": -1,
            "points": 0,
            "form": "L",
            "qualification_status": "must_win",
        },
        {
            "team": {
                "id": 2384,
                "name": "USA",
                "flag": "https://media.api-sports.io/flags/us.svg",
            },
            "group": "Group B",
            "rank": 4,
            "played": 1,
            "won": 0,
            "drawn": 0,
            "lost": 1,
            "goals_for": 0,
            "goals_against": 1,
            "goal_difference": -1,
            "points": 0,
            "form": "L",
            "qualification_status": "must_win",
        },
    ],
    "Group C": [],
    "Group D": [],
    "Group E": [],
    "Group F": [],
    "Group G": [],
    "Group H": [],
    "Group I": [],
    "Group J": [],
    "Group K": [],
    "Group L": [],
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Top Scorers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEMO_SCORERS = [
    {
        "player": {
            "id": 278,
            "name": "Kylian Mbappé",
            "photo": "https://media.api-sports.io/football/players/278.png",
        },
        "team": {
            "id": 2,
            "name": "France",
            "flag": "https://media.api-sports.io/flags/fr.svg",
        },
        "goals": 3,
        "assists": 1,
    },
    {
        "player": {
            "id": 154,
            "name": "Lionel Messi",
            "photo": "https://media.api-sports.io/football/players/154.png",
        },
        "team": {
            "id": 26,
            "name": "Argentina",
            "flag": "https://media.api-sports.io/flags/ar.svg",
        },
        "goals": 2,
        "assists": 2,
    },
    {
        "player": {
            "id": 1100,
            "name": "Jude Bellingham",
            "photo": "https://media.api-sports.io/football/players/1100.png",
        },
        "team": {
            "id": 10,
            "name": "England",
            "flag": "https://media.api-sports.io/flags/gb.svg",
        },
        "goals": 2,
        "assists": 1,
    },
    {
        "player": {
            "id": 306,
            "name": "Vinícius Júnior",
            "photo": "https://media.api-sports.io/football/players/306.png",
        },
        "team": {
            "id": 6,
            "name": "Brazil",
            "flag": "https://media.api-sports.io/flags/br.svg",
        },
        "goals": 2,
        "assists": 0,
    },
    {
        "player": {
            "id": 521,
            "name": "Pedri",
            "photo": "https://media.api-sports.io/football/players/521.png",
        },
        "team": {
            "id": 9,
            "name": "Spain",
            "flag": "https://media.api-sports.io/flags/es.svg",
        },
        "goals": 1,
        "assists": 3,
    },
]
