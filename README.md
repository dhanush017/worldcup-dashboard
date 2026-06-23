# CupPulse 2026

![Live on Render](https://img.shields.io/badge/Render-Live-brightgreen?style=flat-square)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

> Real-Time FIFA World Cup 2026 Intelligence Dashboard for Indian football fans

![Dashboard Screenshot](assets/screenshot.png)

## 🚀 Features

- **Live scores and match status** updates in real time.
- **Smart match cards** (live → upcoming → completed priority).
- **Today's matches** with IST timing.
- **Upcoming and completed matches** overviews.
- **Group standings (A through L)** with qualification badges.
- **Top scorers** with hype scores.
- **Watch Live links** for each match.
- **Auto-refresh** (live data every 60s, other data every 10min).
- **Demo mode** fallback when the API is unavailable.
- **IST timezone display** customized for Indian users.
- **Dark glassmorphism UI** for a premium viewing experience.

## 💻 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Dashboard** | Plotly Dash |
| **Styling** | Dash Bootstrap Components |
| **Language** | Python 3.12 |
| **API** | football-data.org |
| **Deployment** | Render |

## 🛠️ Local Setup Instructions

```bash
git clone https://github.com/dhanush017/worldcup-dashboard.git
cd worldcup-dashboard
pip install -r requirements.txt
```

Create a `.env` file in the root directory and add your API key:
```env
FOOTBALL_API_KEY=your_key_here
```

Run the application:
```bash
python app.py
```
Open `http://localhost:8050` in your web browser.

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `FOOTBALL_API_KEY` | football-data.org API token |
| `FOOTBALL_COMPETITION_CODE` | WC |
| `FOOTBALL_COMPETITION_ID` | 2000 |
| `FOOTBALL_API_HOST` | api.football-data.org |

## 📂 Project Structure

```text
worldcup-dashboard/
├── app.py                # Main Dash application entry point
├── components.py         # UI components and layout elements
├── data_store.py         # Data caching and aggregation layer
├── fallback_data.py      # Demo data for testing / API unavailability
├── football_api.py       # API integration with football-data.org
├── utils.py              # Helper functions, timezones, logic
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── assets/               # Static assets (images, fonts, custom css)
    ├── favicon.ico
    └── favicon.svg
```

## 🗺️ Roadmap

- **V1 MVP** ✅ Complete
- **V2 Intelligence** (predictions, player hype, sentiment)
- **V3 Creator Mode** (captions, reel ideas, hashtags)
- **V4 Monetization** (branded dashboards, cafe mode)

---

<p align="center">
  <b>Built for Indian football fans 🇮🇳⚽ during FIFA World Cup 2026</b><br>
  <a href="https://worldcup-dashboard-m1gp.onrender.com/">Live Demo</a> | <a href="https://github.com/dhanush017/worldcup-dashboard">GitHub Repo</a>
</p>
