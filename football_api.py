import os
# Unset SSLKEYLOGFILE before importing requests to prevent SSL key log permission issues in sandboxed environment
os.environ.pop("SSLKEYLOGFILE", None)

import requests
from datetime import datetime
from dotenv import load_dotenv
from utils import safe_get, convert_to_ist, normalize_team_name

load_dotenv()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

API_KEY = os.getenv("FOOTBALL_API_KEY")
COMPETITION_CODE = os.getenv("FOOTBALL_COMPETITION_CODE", "WC")
COMPETITION_ID = os.getenv("FOOTBALL_COMPETITION_ID", "2000")
BASE_URL = "https://api.football-data.org/v4"
TIMEOUT = 15  # seconds

HEADERS = {
    "X-Auth-Token": API_KEY if API_KEY else ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Normalization
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def normalize_match(raw):
    """Converts football-data.org match object to internal schema.
    
    Input fields from API:
    - raw["id"] → fixture_id
    - raw["status"] → map to status and status_short
    - raw["homeTeam"]["name"] → home_team.name
    - raw["homeTeam"]["id"] → home_team.id
    - raw["homeTeam"]["crest"] → home_team.flag
    - raw["awayTeam"]["name"] → away_team.name
    - raw["awayTeam"]["id"] → away_team.id
    - raw["awayTeam"]["crest"] → away_team.flag
    - raw["score"]["fullTime"]["home"] → score.home (default 0)
    - raw["score"]["fullTime"]["away"] → score.away (default 0)
    - raw["venue"] → venue (may be None, default "Venue TBC")
    - raw["utcDate"] → kickoff_utc, convert to IST for kickoff_ist and kickoff_ist_display
    - raw["group"] → group (strip "GROUP_" prefix, e.g. "GROUP_A" → "Group A")
    - raw["stage"] → round (format nicely, e.g. "GROUP_STAGE" → "Group Stage")
    - raw["matchday"] → add to round as "Matchday X"
    
    Output must match this exact schema:
    {
      "fixture_id": int,
      "status": "scheduled" or "live" or "completed",
      "status_short": "NS" or "1H" or "HT" or "2H" or "FT" etc,
      "status_display": str,
      "home_team": {"id": int, "name": str, "flag": str},
      "away_team": {"id": int, "name": str, "flag": str},
      "score": {"home": int, "away": int},
      "venue": str,
      "kickoff_utc": str,
      "kickoff_ist": str,
      "kickoff_ist_display": str,
      "round": str,
      "group": str,
      "win_probability": None,
      "importance_score": 50,
      "events": []
    }
    
    Use safe_get from utils.py for all field access.
    Use convert_to_ist from utils.py for time conversion.
    win_probability is always None.
    importance_score is always 50 as default.
    """
    fixture_id = int(safe_get(raw, ["id"], 0))
    raw_status = safe_get(raw, ["status"], "")
    
    # Map status
    if raw_status in ("TIMED", "SCHEDULED"):
        status = "scheduled"
    elif raw_status in ("IN_PLAY", "PAUSED"):
        status = "live"
    elif raw_status == "FINISHED":
        status = "completed"
    elif raw_status == "POSTPONED":
        status = "postponed"
    elif raw_status == "CANCELLED":
        status = "cancelled"
    else:
        status = "scheduled"
        
    # Map status_short
    if raw_status == "IN_PLAY":
        status_short = "1H"
    elif raw_status == "PAUSED":
        status_short = "HT"
    elif raw_status == "FINISHED":
        status_short = "FT"
    elif raw_status in ("TIMED", "SCHEDULED"):
        status_short = "NS"
    elif raw_status == "POSTPONED":
        status_short = "PST"
    elif raw_status == "CANCELLED":
        status_short = "CANC"
    else:
        status_short = "NS"
        
    # Extract Team Names & Logos/Crests
    home_name = normalize_team_name(safe_get(raw, ["homeTeam", "name"], "TBD"))
    home_id = safe_get(raw, ["homeTeam", "id"])
    home_flag = safe_get(raw, ["homeTeam", "crest"], "")
    home_tla = safe_get(raw, ["homeTeam", "tla"], "")
    
    away_name = normalize_team_name(safe_get(raw, ["awayTeam", "name"], "TBD"))
    away_id = safe_get(raw, ["awayTeam", "id"])
    away_flag = safe_get(raw, ["awayTeam", "crest"], "")
    away_tla = safe_get(raw, ["awayTeam", "tla"], "")
    
    # Extract Scores
    home_score = safe_get(raw, ["score", "fullTime", "home"])
    away_score = safe_get(raw, ["score", "fullTime", "away"])
    home_score = home_score if home_score is not None else 0
    away_score = away_score if away_score is not None else 0
    
    # Extract Venue
    venue = safe_get(raw, ["venue"])
    if not venue:
        venue = "Venue TBC"
        
    # Date/Time extraction and conversion to IST
    kickoff_utc = safe_get(raw, ["utcDate"], "")
    ist_info = convert_to_ist(kickoff_utc)
    kickoff_ist_display = ist_info.get("display", "Time TBC")
    ist_dt = ist_info.get("datetime")
    kickoff_ist = ist_dt.isoformat() if ist_dt else ""
    
    # Map status_display
    if status == "live":
        minute = safe_get(raw, ["minute"])
        if minute:
            status_display = f"{minute}'"
        else:
            status_display = "Half Time" if status_short == "HT" else "Live"
    elif status == "completed":
        status_display = "Full Time"
    elif status == "postponed":
        status_display = "Postponed"
    elif status == "cancelled":
        status_display = "Cancelled"
    else:
        status_display = kickoff_ist_display
        
    # Extract Group
    raw_group = safe_get(raw, ["group"])
    group = ""
    if raw_group:
        cleaned_group = raw_group.replace("GROUP_", "").replace("_", " ").strip()
        if len(cleaned_group) == 1:
            group = f"Group {cleaned_group}"
        else:
            group = cleaned_group.title()
            
    # Extract Round/Stage
    raw_stage = safe_get(raw, ["stage"])
    round_name = ""
    if raw_stage:
        round_name = raw_stage.replace("_", " ").title()
        
    matchday = safe_get(raw, ["matchday"])
    if matchday:
        if round_name:
            round_name = f"{round_name} - Matchday {matchday}"
        else:
            round_name = f"Matchday {matchday}"
            
    return {
        "fixture_id": fixture_id,
        "status": status,
        "status_short": status_short,
        "status_display": status_display,
        "home_team": {"id": home_id, "name": home_name, "flag": home_flag, "tla": home_tla},
        "away_team": {"id": away_id, "name": away_name, "flag": away_flag, "tla": away_tla},
        "score": {"home": home_score, "away": away_score},
        "venue": venue,
        "kickoff_utc": kickoff_utc,
        "kickoff_ist": kickoff_ist,
        "kickoff_ist_display": kickoff_ist_display,
        "round": round_name,
        "group": group,
        "win_probability": None,
        "importance_score": 50,
        "events": []
    }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Endpoints
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_all_matches():
    """GET /competitions/{COMPETITION_CODE}/matches
    Returns all matches. Used as base for filtering.
    """
    try:
        url = f"{BASE_URL}/competitions/{COMPETITION_CODE}/matches"
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            matches = safe_get(data, ["matches"], [])
            return [normalize_match(m) for m in matches]
    except Exception:
        pass
    return None


def get_live_matches():
    """Filter get_all_matches() where status == "live"
    Returns list of normalized matches or [] if none.
    """
    endpoint = "live_matches"
    import data_store
    import fallback_data

    # 1. Rate Limit check
    if data_store.is_api_limit_reached():
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached
        return fallback_data.DEMO_LIVE

    # 2. Fresh Cache check
    if data_store.is_cache_fresh(endpoint):
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached

    # 3. Call API
    try:
        all_matches = get_all_matches()
        if all_matches is not None:
            live_matches = [m for m in all_matches if m.get("status") == "live"]
            data_store.save_cache(endpoint, live_matches)
            data_store.increment_api_counter()
            return live_matches
    except Exception:
        pass

    # 4. API fails -> stale cache or fallback
    cached = data_store.load_cache(endpoint)
    if cached is not None:
        return cached
    return fallback_data.DEMO_LIVE


def get_today_matches():
    """Filter get_all_matches() where kickoff date in IST == today's date in IST
    Returns list of normalized matches.
    """
    endpoint = "today_matches"
    import data_store
    import fallback_data

    # 1. Rate Limit check
    if data_store.is_api_limit_reached():
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached
        return fallback_data.DEMO_MATCHES

    # 2. Fresh Cache check
    if data_store.is_cache_fresh(endpoint):
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached

    # 3. Call API
    try:
        all_matches = get_all_matches()
        if all_matches is not None:
            from utils import IST
            today_ist = datetime.now(IST).strftime("%Y-%m-%d")
            today_matches = [m for m in all_matches if m.get("kickoff_ist", "")[:10] == today_ist]
            data_store.save_cache(endpoint, today_matches)
            data_store.increment_api_counter()
            return today_matches
    except Exception:
        pass

    # 4. API fails -> stale cache or fallback
    cached = data_store.load_cache(endpoint)
    if cached is not None:
        return cached
    return fallback_data.DEMO_MATCHES


def get_upcoming_matches():
    """Filter get_all_matches() where status == "scheduled"
    Sort by kickoff_utc ascending. Return first 10.
    """
    endpoint = "upcoming_matches"
    import data_store
    import fallback_data

    # 1. Rate Limit check
    if data_store.is_api_limit_reached():
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached
        return fallback_data.DEMO_UPCOMING

    # 2. Fresh Cache check
    if data_store.is_cache_fresh(endpoint):
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached

    # 3. Call API
    try:
        all_matches = get_all_matches()
        if all_matches is not None:
            upcoming = [m for m in all_matches if m.get("status") == "scheduled"]
            upcoming = sorted(upcoming, key=lambda x: x.get("kickoff_utc", ""))
            result = upcoming[:10]
            data_store.save_cache(endpoint, result)
            data_store.increment_api_counter()
            return result
    except Exception:
        pass

    # 4. API fails -> stale cache or fallback
    cached = data_store.load_cache(endpoint)
    if cached is not None:
        return cached
    return fallback_data.DEMO_UPCOMING


def get_completed_matches():
    """Filter get_all_matches() where status == "completed"
    Sort by kickoff_utc descending. Return first 10.
    """
    endpoint = "completed_matches"
    import data_store
    import fallback_data

    # 1. Rate Limit check
    if data_store.is_api_limit_reached():
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached
        return fallback_data.DEMO_COMPLETED

    # 2. Fresh Cache check
    if data_store.is_cache_fresh(endpoint):
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached

    # 3. Call API
    try:
        all_matches = get_all_matches()
        if all_matches is not None:
            completed = [m for m in all_matches if m.get("status") == "completed"]
            completed = sorted(completed, key=lambda x: x.get("kickoff_utc", ""), reverse=True)
            result = completed[:10]
            
            num_fetched = 0
            for match in result:
                fixture_id = match.get("fixture_id")
                if not fixture_id:
                    continue
                    
                cache_key = f"match_detail_{fixture_id}"
                
                if data_store.is_cache_fresh(cache_key):
                    cached_detail = data_store.load_cache(cache_key)
                    if cached_detail is not None:
                        match["events"] = cached_detail
                        continue
                        
                if num_fetched >= 5:
                    match["events"] = []
                    continue
                    
                try:
                    url = f"{BASE_URL}/matches/{fixture_id}"
                    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                    if resp.status_code == 200:
                        data = resp.json()
                        goals_data = safe_get(data, ["match", "goals"], [])
                        if not isinstance(goals_data, list):
                            goals_data = []
                            
                        events = []
                        for g in goals_data:
                            minute = safe_get(g, ["minute"])
                            if minute is None:
                                minute = 0
                            else:
                                minute = int(minute)
                                
                            scorer = safe_get(g, ["scorer", "name"], "Unknown")
                            team = safe_get(g, ["team", "name"], "Unknown")
                            gtype_raw = safe_get(g, ["type"], "REGULAR")
                            
                            if gtype_raw == "OWN_GOAL":
                                gtype = "own_goal"
                            elif gtype_raw == "PENALTY":
                                gtype = "penalty"
                            else:
                                gtype = "goal"
                                
                            events.append({
                                "minute": minute,
                                "scorer": scorer,
                                "team": team,
                                "type": gtype
                            })
                            
                        events = sorted(events, key=lambda x: x.get("minute", 0))
                        match["events"] = events
                        
                        data_store.save_cache(cache_key, events)
                        data_store.increment_api_counter()
                        num_fetched += 1
                    else:
                        match["events"] = []
                except Exception:
                    match["events"] = []
            
            data_store.save_cache(endpoint, result)
            data_store.increment_api_counter()
            return result
    except Exception:
        pass

    # 4. API fails -> stale cache or fallback
    cached = data_store.load_cache(endpoint)
    if cached is not None:
        return cached
    return fallback_data.DEMO_COMPLETED


def get_standings():
    """GET /competitions/{COMPETITION_CODE}/standings
    Normalize standings per team and group by group name.
    """
    endpoint = "standings"
    import data_store
    import fallback_data

    # 1. Rate Limit check
    if data_store.is_api_limit_reached():
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached
        return fallback_data.DEMO_STANDINGS

    # 2. Fresh Cache check
    if data_store.is_cache_fresh(endpoint):
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached

    # 3. Call API
    try:
        url = f"{BASE_URL}/competitions/{COMPETITION_CODE}/standings"
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            standings_list = safe_get(data, ["standings"], [])
            
            group_standings = {f"Group {ch}": [] for ch in "ABCDEFGHIJKL"}
            for item in standings_list:
                raw_group = safe_get(item, ["group"])
                if not raw_group:
                    continue
                cleaned_group = raw_group.replace("GROUP_", "").replace("_", " ").strip()
                if len(cleaned_group) == 1:
                    group_name = f"Group {cleaned_group}"
                else:
                    group_name = cleaned_group.title()
                    
                table = safe_get(item, ["table"], [])
                group_teams = []
                for entry in table:
                    team_id = safe_get(entry, ["team", "id"])
                    team_name = normalize_team_name(safe_get(entry, ["team", "name"], "TBD"))
                    team_crest = safe_get(entry, ["team", "crest"], "")
                    
                    rank = safe_get(entry, ["position"], 0)
                    played = safe_get(entry, ["playedGames"], 0)
                    won = safe_get(entry, ["won"], 0)
                    drawn = safe_get(entry, ["draw"], 0)
                    lost = safe_get(entry, ["lost"], 0)
                    goals_for = safe_get(entry, ["goalsFor"], 0)
                    goals_against = safe_get(entry, ["goalsAgainst"], 0)
                    goal_difference = safe_get(entry, ["goalDifference"], 0)
                    points = safe_get(entry, ["points"], 0)
                    form = safe_get(entry, ["form"], "")
                    if form is None:
                        form = ""
                        
                    group_teams.append({
                        "team": {"id": team_id, "name": team_name, "flag": team_crest},
                        "group": group_name,
                        "rank": rank,
                        "played": played,
                        "won": won,
                        "drawn": drawn,
                        "lost": lost,
                        "goals_for": goals_for,
                        "goals_against": goals_against,
                        "goal_difference": goal_difference,
                        "points": points,
                        "form": form,
                        "qualification_status": "pending"
                    })
                # Sort by rank
                group_teams = sorted(group_teams, key=lambda x: x.get("rank", 99))
                group_standings[group_name] = group_teams
                
            data_store.save_cache(endpoint, group_standings)
            data_store.increment_api_counter()
            return group_standings
    except Exception:
        pass

    # 4. API fails -> stale cache or fallback
    cached = data_store.load_cache(endpoint)
    if cached is not None:
        return cached
    return fallback_data.DEMO_STANDINGS


def get_top_scorers():
    """GET /competitions/{COMPETITION_CODE}/scorers
    Normalize scorers and sort by goals descending.
    """
    endpoint = "top_scorers"
    import data_store
    import fallback_data

    # 1. Rate Limit check
    if data_store.is_api_limit_reached():
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached
        return fallback_data.DEMO_SCORERS

    # 2. Fresh Cache check
    if data_store.is_cache_fresh(endpoint):
        cached = data_store.load_cache(endpoint)
        if cached is not None:
            return cached

    # 3. Call API
    try:
        url = f"{BASE_URL}/competitions/{COMPETITION_CODE}/scorers"
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            scorers_list = safe_get(data, ["scorers"], [])
            
            normalized_scorers = []
            for entry in scorers_list:
                player_id = safe_get(entry, ["player", "id"])
                player_name = safe_get(entry, ["player", "name"], "Unknown Player")
                
                team_name = normalize_team_name(safe_get(entry, ["team", "name"], "TBD"))
                team_crest = safe_get(entry, ["team", "crest"], "")
                
                goals = safe_get(entry, ["goals"], 0)
                assists = safe_get(entry, ["assists"], 0)
                assists = assists if assists is not None else 0
                
                played_matches = safe_get(entry, ["playedMatches"], 0)
                played_matches = played_matches if played_matches is not None else 0
                
                normalized_scorers.append({
                    "player": {"id": player_id, "name": player_name, "photo": ""},
                    "team": {"name": team_name, "flag": team_crest},
                    "goals": goals,
                    "assists": assists,
                    "matches_played": played_matches,
                    "hype_score": 50
                })
                
            normalized_scorers = sorted(normalized_scorers, key=lambda x: x.get("goals", 0), reverse=True)
            data_store.save_cache(endpoint, normalized_scorers)
            data_store.increment_api_counter()
            return normalized_scorers
    except Exception:
        pass

    # 4. API fails -> stale cache or fallback
    cached = data_store.load_cache(endpoint)
    if cached is not None:
        return cached
    return fallback_data.DEMO_SCORERS


def get_match_events(fixture_id):
    """GET /fixtures/events?fixture={fixture_id} (Not used in v4 for now, returns empty list)"""
    return []
