# GarimpoBot (ProspectorBot)

An AI-assisted marketplace scout that helps users track second-hand deals with a FastAPI backend and a Flutter Web frontend.

## What You Get

- FastAPI backend with preference management, mock search results, and AI helpers.
- Flutter Web UI ready for live demos.
- Local JSON storage for fast setup and no external DB.

## Project Structure

- `src/prospector_bot/` Backend (FastAPI, scrapers, storage)
- `frontend/` Flutter Web app
- `data/` Local JSON state
- `assets/` Shared assets

## Quick Start

1. Create a `.env` file:

```env
GEMINI_API_KEY=your-gemini-api-key
API_KEY=
```

2. Install backend dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

3. Start the API:

```bash
python run.py --mode api
```

4. Start the frontend:

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

The API runs on `http://localhost:8000` by default. The frontend points to it via `frontend/lib/config/api_config.dart`.

## API Highlights

- `GET /health`
- `GET /api/preferences`
- `POST /api/preferences`
- `PUT /api/preferences/{index}`
- `DELETE /api/preferences/{index}`
- `POST /api/search`
- `POST /api/ai/analyze`
- `POST /api/ai/suggest-search`

## Notes

- If you set `API_KEY` in `.env`, send it as `X-API-Key` on all requests.
- The demo search uses mock listings for fast hackathon demos.
