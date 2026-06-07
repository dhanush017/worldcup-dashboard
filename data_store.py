"""
Data-store layer for the FIFA World Cup 2026 Dashboard.
Manages the cache → API → fallback pipeline and tracks daily API usage.
"""

import json
import os
os.environ.pop("SSLKEYLOGFILE", None)
from datetime import datetime, timezone

from dotenv import load_dotenv

import fallback_data
import football_api

load_dotenv()

USE_REAL_API = False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Paths
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CACHE_FILE = os.path.join(DATA_DIR, "cache.json")
API_USAGE_FILE = os.path.join(DATA_DIR, "api_usage.json")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TTL configuration (seconds)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TTL = {
    "live_matches": 60,
    "today_matches": 300,
    "upcoming_matches": 900,
    "completed_matches": 900,
    "standings": 900,
    "top_scorers": 900,
    "match_events": 60,
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Endpoint → API function mapping
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_API_FUNCTIONS = {
    "live_matches": football_api.get_live_matches,
    "today_matches": football_api.get_today_matches,
    "upcoming_matches": football_api.get_upcoming_matches,
    "completed_matches": football_api.get_completed_matches,
    "standings": football_api.get_standings,
    "top_scorers": football_api.get_top_scorers,
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Endpoint → fallback data mapping
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_FALLBACK_DATA = {
    "live_matches": fallback_data.DEMO_LIVE,
    "today_matches": fallback_data.DEMO_MATCHES,
    "upcoming_matches": fallback_data.DEMO_UPCOMING,
    "completed_matches": fallback_data.DEMO_COMPLETED,
    "standings": fallback_data.DEMO_STANDINGS,
    "top_scorers": fallback_data.DEMO_SCORERS,
    "match_events": [],
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Cache helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _read_json(filepath):
    """Read and return parsed JSON from *filepath*, or ``{}`` on error."""
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _write_json(filepath, data):
    """Atomically write *data* as JSON to *filepath*."""
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False, default=str)
    except OSError:
        pass


def is_cache_fresh(endpoint):
    """Return ``True`` if ``cache.json`` has data for *endpoint* within TTL."""
    cache = _read_json(CACHE_FILE)
    entry = cache.get(endpoint)
    if not entry:
        return False

    fetched_at = entry.get("fetched_at_utc")
    if not fetched_at:
        return False

    try:
        fetched_dt = datetime.fromisoformat(fetched_at.replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - fetched_dt).total_seconds()
        return age < TTL.get(endpoint, 900)
    except (ValueError, TypeError):
        return False


def save_cache(endpoint, data):
    """Save *data* under *endpoint* in ``data/cache.json`` with a timestamp."""
    cache = _read_json(CACHE_FILE)
    cache[endpoint] = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }
    _write_json(CACHE_FILE, cache)


def load_cache(endpoint):
    """Load cached data for *endpoint*. Returns ``None`` if absent."""
    cache = _read_json(CACHE_FILE)
    entry = cache.get(endpoint)
    if entry and "data" in entry:
        return entry["data"]
    return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  API usage tracking
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def increment_api_counter():
    """Increment today's API-call count in ``data/api_usage.json``.

    Resets to 0 if the stored date differs from today. Saves the file
    and returns the new count as an ``int``.
    """
    usage = _read_json(API_USAGE_FILE)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if usage.get("date") != today:
        usage = {"date": today, "count": 0}

    usage["count"] = usage.get("count", 0) + 1
    _write_json(API_USAGE_FILE, usage)
    return usage["count"]


def is_api_limit_reached():
    """Return ``True`` if today's API count in ``api_usage.json`` ≥ 95."""
    usage = _read_json(API_USAGE_FILE)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if usage.get("date") != today:
        return False

    return usage.get("count", 0) >= 95


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Main entry point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_data(endpoint):
    """Fetch data for *endpoint* through the cache → API → fallback pipeline.

    1. If cached data is fresh (within TTL), return it immediately.
    2. If the daily API limit is reached, skip the API and use cache or fallback.
    3. Otherwise call the API, cache the result, and return it.
    4. On API failure, fall back to stale cache or demo data.

    Parameters
    ----------
    endpoint : str
        One of ``'live_matches'``, ``'today_matches'``,
        ``'upcoming_matches'``, ``'completed_matches'``,
        ``'standings'``, ``'top_scorers'``, ``'match_events'``.

    Returns
    -------
    list | dict
        Normalized data for the requested endpoint.
    """
    if not USE_REAL_API:
        return _FALLBACK_DATA.get(endpoint, [])

    # 1 — Fresh cache?
    if is_cache_fresh(endpoint):
        cached = load_cache(endpoint)
        if cached is not None:
            return cached

    # 2 — API limit reached? → use stale cache or fallback
    if is_api_limit_reached():
        cached = load_cache(endpoint)
        if cached is not None:
            return cached
        return _FALLBACK_DATA.get(endpoint, [])

    # 3 — Call the API
    api_fn = _API_FUNCTIONS.get(endpoint)
    if api_fn:
        increment_api_counter()
        api_data = api_fn()
        if api_data is not None:
            save_cache(endpoint, api_data)
            return api_data

    # 4 — API failed → stale cache or fallback
    cached = load_cache(endpoint)
    if cached is not None:
        return cached

    return _FALLBACK_DATA.get(endpoint, [])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Wrapper Functions & Smart Match Cards
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_live_matches():
    """Get live matches list."""
    return get_data("live_matches")


def get_today_matches():
    """Get today's matches list."""
    return get_data("today_matches")


def get_upcoming_matches():
    """Get upcoming matches list."""
    return get_data("upcoming_matches")


def get_completed_matches():
    """Get completed matches list."""
    return get_data("completed_matches")


def get_standings():
    """Get standings dict."""
    return get_data("standings")


def get_smart_match_cards():
    """Returns exactly 3 match cards using this priority:
    1. If live matches exist: 1 live + 2 upcoming
    2. If no live but upcoming exist: 2 upcoming + 1 completed
    3. If no upcoming: 3 completed
    4. If all empty: return fallback_data.DEMO_MATCHES[:3]
    Never returns more or fewer than 3 matches."""
    live = get_live_matches() or []
    upcoming = get_upcoming_matches() or []
    completed = get_completed_matches() or []
    
    selected = []
    
    # 1. If live matches exist: 1 live + 2 upcoming
    if len(live) > 0:
        selected.append(live[0])
        selected.extend(upcoming[:2])
        if len(selected) < 3:
            # fill from remaining live
            selected.extend(live[1:])
        if len(selected) < 3:
            # fill from completed
            selected.extend(completed)
            
    # 2. If no live but upcoming exist: 2 upcoming + 1 completed
    elif len(upcoming) > 0:
        selected.extend(upcoming[:2])
        selected.extend(completed[:1])
        if len(selected) < 3:
            # fill from remaining upcoming
            selected.extend(upcoming[2:])
        if len(selected) < 3:
            # fill from live
            selected.extend(live)
            
    # 3. If no upcoming: 3 completed
    else:
        selected.extend(completed[:3])
        if len(selected) < 3:
            # fill from live
            selected.extend(live)
            
    selected = selected[:3]
    
    # 4. If all empty / less than 3: return fallback_data.DEMO_MATCHES[:3]
    if len(selected) < 3:
        return fallback_data.DEMO_MATCHES[:3]
        
    return selected
