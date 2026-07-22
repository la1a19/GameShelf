# 🎮 GameShelf

A personal game backlog tracker — search for games, add them to your shelf, track your progress, and jot down notes as you play.

Built as a solo project to practice full-stack development with Django, live search via AJAX, and third-party API integration.

![screenshot](screenshot.png)
<!-- Add a real screenshot of your tracker page here, saved in your repo root -->

## Features

- 🔍 **Live search** — search for games via the IGDB API, results appear as you type (debounced, no page reload)
- ➕ **Add to shelf** — one click adds a game to your personal tracker
- 🏷️ **Status tracking** — mark games as Not Started, Playing, Done, or Dropped, with instantly updating colored status pills
- 📝 **Per-game notes** — open a slide-out sidebar to jot down notes on any tracked game
- 🗑️ **Remove games** — delete a game from your shelf with a hover-revealed button
- 🔐 **User accounts** — sign up, log in, and keep your own private tracker (built on Django's auth system)

## Tech Stack

- **Backend:** Django 6, Python
- **Database:** SQLite (development)
- **Frontend:** Vanilla JavaScript (fetch API, no frameworks), HTML, CSS
- **Styling:** Bootstrap 4 (Bootswatch "Lux" theme) + custom CSS
- **External API:** [IGDB](https://api-docs.igdb.com/) (via Twitch OAuth) for game search and cover art

## Setup

1. Clone the repo
   ```bash
   git clone https://github.com/la1a19/GameShelf.git
   cd GameShelf
   ```

2. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your IGDB credentials:
   ```
   IGDB_CLIENT_ID=your_client_id_here
   IGDB_CLIENT_SECRET=your_client_secret_here
   ```
   (Get these by registering an app at [dev.twitch.tv](https://dev.twitch.tv/console/apps) — IGDB uses Twitch's developer platform for authentication.)

4. Run migrations and start the server
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/` and sign up for an account

## What I'd improve next

- Cache the IGDB auth token instead of requesting a new one on every search
- Replace the "reload page after adding a game" approach with proper DOM updates via event delegation
- Add drag-and-drop reordering for tracked games
- Build a fully custom dropdown component to fix native `<select>` styling inconsistencies across browsers

## Screenshots

<!-- Add 2-3 screenshots here: the search dropdown, the tracker table, the notes sidebar -->
