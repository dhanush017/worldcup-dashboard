"""
Utility helpers for the FIFA World Cup 2026 Dashboard.
Safe data access, timezone conversion, status formatting,
team-name normalization, and match-importance scoring.
"""

from datetime import datetime, timedelta, timezone

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  IST timezone (UTC +05:30)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IST = timezone(timedelta(hours=5, minutes=30))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Team-name normalization map
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_TEAM_NAME_MAP = {
    "Korea Republic": "South Korea",
    "Korea DPR": "North Korea",
    "IR Iran": "Iran",
    "Türkiye": "Turkey",
    "Turkiye": "Turkey",
    "Côte d'Ivoire": "Ivory Coast",
    "Cote D'Ivoire": "Ivory Coast",
    "United States": "USA",
    "Czech Republic": "Czechia",
    "Chinese Taipei": "Taiwan",
    "Bosnia and Herzegovina": "Bosnia & Herzegovina",
    "Trinidad and Tobago": "Trinidad & Tobago",
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  safe_get
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def safe_get(obj, keys, default=None):
    """Safely traverse a nested dict.

    Example::

        safe_get(match, ['home_team', 'name'], 'TBD')

    Never raises ``KeyError`` or ``TypeError``.
    """
    current = obj
    for key in keys:
        try:
            current = current[key]
        except (KeyError, TypeError, IndexError):
            return default
    return current


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  convert_to_ist
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def convert_to_ist(utc_string):
    """Convert a UTC datetime string to IST.

    Accepts strings like ``'2026-06-21T18:00:00Z'``.

    Returns a dict::

        {'display': '23:30 IST', 'datetime': <datetime>, 'hour': 23}

    Returns ``{'display': 'Time TBC', 'datetime': None, 'hour': 0}``
    if *utc_string* is ``None`` or unparseable.
    """
    if not utc_string:
        return {"display": "Time TBC", "datetime": None, "hour": 0}

    try:
        # Handle both 'Z' suffix and '+00:00' suffix
        clean = utc_string.replace("Z", "+00:00")
        utc_dt = datetime.fromisoformat(clean)
        ist_dt = utc_dt.astimezone(IST)
        display = ist_dt.strftime("%H:%M") + " IST"
        return {"display": display, "datetime": ist_dt, "hour": ist_dt.hour}
    except (ValueError, AttributeError, TypeError):
        return {"display": "Time TBC", "datetime": None, "hour": 0}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  format_match_status
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def format_match_status(status_short, minute):
    """Return a human-readable match status string.

    Parameters
    ----------
    status_short : str
        Short status code from the API (``'1H'``, ``'FT'``, etc.).
    minute : int | str | None
        Current match minute (used for live statuses).

    Mapping
    -------
    ``'1H'`` / ``'2H'`` → ``"74'"`` (the current minute)
    ``'HT'``            → ``'Half Time'``
    ``'ET'``            → ``'Extra Time'``
    ``'P'``             → ``'Penalties'``
    ``'FT'``            → ``'Full Time'``
    ``'AET'``           → ``'After Extra Time'``
    ``'PEN'``           → ``'After Penalties'``
    ``'NS'``            → kickoff time string (passed as *minute*)
    ``'PST'``           → ``'Postponed'``
    ``'CANC'``          → ``'Cancelled'``
    Anything else       → ``'Scheduled'``
    """
    status_map = {
        "HT": "Half Time",
        "ET": "Extra Time",
        "P": "Penalties",
        "FT": "Full Time",
        "AET": "After Extra Time",
        "PEN": "After Penalties",
        "PST": "Postponed",
        "CANC": "Cancelled",
    }

    if status_short in ("1H", "2H"):
        return f"{minute}'" if minute else "Live"

    if status_short in status_map:
        return status_map[status_short]

    if status_short == "NS":
        # minute may carry the kickoff time display string
        return str(minute) if minute else "Scheduled"

    return "Scheduled"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  normalize_team_name
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def normalize_team_name(raw_name):
    """Normalize known team-name variations.

    Examples::

        normalize_team_name('Korea Republic')  # → 'South Korea'
        normalize_team_name('IR Iran')         # → 'Iran'
        normalize_team_name('Türkiye')         # → 'Turkey'

    Returns *raw_name* unchanged if no mapping is found.
    """
    if not raw_name:
        return raw_name
    return _TEAM_NAME_MAP.get(raw_name, raw_name)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  calculate_match_importance
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calculate_match_importance(match, standings):
    """Return an integer 0–100 importance score for a match.

    Scoring
    -------
    * Base score: **50**
    * Knockout rounds: **+30**
    * Either team has ``qualification_status == 'must_win'``: **+15**
    * Either team has ``qualification_status == 'in_danger'``: **+10**
    * Result is capped at **100**.

    Parameters
    ----------
    match : dict
        A match object (see ``fallback_data`` for the schema).
    standings : dict
        The full group-standings dict, keyed by group name.
    """
    score = 50

    # Knockout-round bonus
    match_round = safe_get(match, ["round"], "")
    if match_round and "group" not in match_round.lower():
        score += 30

    # Qualification-pressure bonus (only applies to group matches)
    group = safe_get(match, ["group"], "")
    group_standings = standings.get(group, []) if standings else []

    home_name = safe_get(match, ["home_team", "name"], "")
    away_name = safe_get(match, ["away_team", "name"], "")

    for entry in group_standings:
        team_name = safe_get(entry, ["team", "name"], "")
        status = safe_get(entry, ["qualification_status"], "")
        if team_name in (home_name, away_name):
            if status == "must_win":
                score += 15
            elif status == "in_danger":
                score += 10

    return min(score, 100)

def get_watch_url(match):
    """Builds ppv.to watch URL for a match.
    
    URL format: https://ppv.to/live/wc/{date}/{team1}-{team2}
    
    Where:
    - date is kickoff_utc date in YYYY-MM-DD format
    - team1 is home_team tla lowercased
    - team2 is away_team tla lowercased
    
    Example: https://ppv.to/live/wc/2026-06-18/cze-rsa
    
    Returns None if tla is missing for either team.
    """
    try:
        home_tla = safe_get(match, ["home_team", "tla"], "")
        away_tla = safe_get(match, ["away_team", "tla"], "")
        
        if not home_tla or not away_tla:
            return None
        
        kickoff_utc = safe_get(match, ["kickoff_utc"], "")
        if not kickoff_utc:
            return None
        
        date = kickoff_utc[:10]  # Extract YYYY-MM-DD
        
        url = f"https://ppv.to/live/wc/{date}/{home_tla.lower()}-{away_tla.lower()}"
        return url
    except:
        return None
