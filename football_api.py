"""
Football API client for the FIFA World Cup 2026 Dashboard.
Wraps the API-Football v3 endpoints on RapidAPI.
Every function is wrapped in try/except and returns None on failure.
"""

import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

API_KEY = os.getenv("FOOTBALL_API_KEY")
LEAGUE_ID = os.getenv("FOOTBALL_LEAGUE_ID", "1")
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
TIMEOUT = 5  # seconds

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Internal helper
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _api_get(endpoint, params=None):
    """Fire a GET request and return the JSON response list.

    Returns ``None`` on any failure (network error, timeout, bad key,
    non-200 status, missing ``response`` key, etc.).
    """
    if not API_KEY:
        return None
    try:
        url = f"{BASE_URL}/{endpoint}"
        resp = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
        if resp.status_code != 200:
            return None
        data = resp.json()
        return data.get("response")
    except (requests.RequestException, ValueError, KeyError):
        return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Public API functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_live_matches():
    """GET /fixtures?live=all

    Returns a list of live fixture dicts or ``None``.
    """
    try:
        return _api_get("fixtures", params={"live": "all"})
    except Exception:
        return None


def get_today_matches():
    """GET /fixtures?date={today YYYY-MM-DD}

    Returns a list of today's fixture dicts or ``None``.
    """
    try:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return _api_get("fixtures", params={"date": today})
    except Exception:
        return None


def get_upcoming_matches():
    """GET /fixtures?league={LEAGUE_ID}&season=2026&next=10

    Returns a list of the next 10 fixture dicts or ``None``.
    """
    try:
        return _api_get(
            "fixtures",
            params={"league": LEAGUE_ID, "season": "2026", "next": "10"},
        )
    except Exception:
        return None


def get_completed_matches():
    """GET /fixtures?league={LEAGUE_ID}&season=2026&last=10

    Returns a list of the last 10 fixture dicts or ``None``.
    """
    try:
        return _api_get(
            "fixtures",
            params={"league": LEAGUE_ID, "season": "2026", "last": "10"},
        )
    except Exception:
        return None


def get_standings():
    """GET /standings?league={LEAGUE_ID}&season=2026

    Returns the standings response list or ``None``.
    """
    try:
        return _api_get(
            "standings",
            params={"league": LEAGUE_ID, "season": "2026"},
        )
    except Exception:
        return None


def get_top_scorers():
    """GET /players/topscorers?league={LEAGUE_ID}&season=2026

    Returns the top-scorers response list or ``None``.
    """
    try:
        return _api_get(
            "players/topscorers",
            params={"league": LEAGUE_ID, "season": "2026"},
        )
    except Exception:
        return None


def get_match_events(fixture_id):
    """GET /fixtures/events?fixture={fixture_id}

    Parameters
    ----------
    fixture_id : int
        The fixture ID to fetch events for.

    Returns the events response list or ``None``.
    """
    try:
        return _api_get(
            "fixtures/events",
            params={"fixture": str(fixture_id)},
        )
    except Exception:
        return None
