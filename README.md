# Discord Embed Web Server

A Flask-based web application that provides Discord OAuth2 login, embed sending, editing, and deletion functionalities. Users can view their embed history and edit or delete embeds through the records.

## Structure

- `app/` - Flask application source
  - `config.py` - Load environment variables
  - `db.py` - SQLAlchemy database models
  - `discord_oauth.py` - Handles Discord OAuth2 authentication
  - `discord_client.py` - Calls Discord message REST API
  - `services/embeds.py` - CRUD logic for records
  - `routes.py` - Defines Flask routes
  - `web.py` - Application entry point
  - `templates/` - HTML templates
- `data/` - SQLite database storage
- `requirements.txt` - Python dependencies
- `.env.example` - Sample environment variables

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the root and set the following values:

```ini
SECRET_KEY=change-me
DATABASE_URL=sqlite:///data/app.db
DISCORD_CLIENT_ID=your_client_id
DISCORD_CLIENT_SECRET=your_client_secret
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=target_channel_id
DISCORD_REDIRECT_URI=http://localhost:5000/callback
```

## Running

```bash
python app/web.py
```

## Usage Flow

1. Log in via Discord OAuth2 at `/login`
2. Create an embed on the home page
3. View your embed history at `/history`
4. Select a record to edit or delete

