# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run

### Docker (production)
```bash
docker build . -t wp_downloader
docker run -d -p 5042:5042 wp_downloader
```

### Local development

**Prerequisites**: Python 3.13+, Node.js 20+, npm, [uv](https://astral.sh/uv) (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

PDF generation requires system libraries:
```bash
# Debian/Ubuntu
sudo apt install libglib2.0-0 libpango-1.0-0 libpangoft2-1.0-0 build-essential python3-dev
```

**Backend** (from `src/api/`):
```bash
uv sync                    # install Python dependencies
cp .env_template .env      # default config (file cache, no Redis)
ln -s "$(pwd)/src/create_book/generators/pdf/fonts" /tmp/fonts  # fonts for PDF
cd src && uv run main.py   # starts FastAPI on port 5042
```

**Frontend** (from `src/frontend/`):
```bash
npm install
npm run build              # static build to src/frontend/build/
npm run dev                # Vite dev server with HMR
```

The backend serves the frontend as static files from `src/api/src/build/`. For local dev, symlink the frontend build output: `ln -s $(pwd)/src/frontend/build $(pwd)/src/api/src/build`.

**Vite dev server proxy** — when using `npm run dev`, API calls need proxying to the backend. Add to `vite.config.js`:
```js
server: {
  proxy: {
    '/download': 'http://localhost:5042',
    '/donate': 'http://localhost:5042',
  }
}
```

**Workflow summary**:

| Changing | Action |
|---|---|
| Backend Python code | Restart `uv run main.py` |
| Frontend (quick iteration) | `npm run dev` with Vite proxy |
| Frontend (full test) | `npm run build`, backend picks it up via symlink |
| Both | Run backend + Vite dev server with proxy |

**Environment variables**: Backend reads from `src/api/.env`. Set `DEBUG=1` to enable Eliot structured logging to `eliot.log`.

### Linting
```bash
# Python (from src/api/)
uv run ruff check src/
uv run ruff format src/

# Frontend (from src/frontend/)
npm run lint               # prettier --check
npm run format             # prettier --write
```

Ruff is configured in `pyproject.toml` — E402 (module-level import order) is ignored.

## Architecture

Two-service monorepo: a FastAPI backend (`src/api/`) and a SvelteKit frontend (`src/frontend/`). The frontend builds to static files (adapter-static) served by FastAPI's `StaticFiles` mount.

### Backend (`src/api/src/`)

- **`main.py`** — FastAPI app with a single download endpoint (`GET /download/{download_id}`) that handles five modes: `story`, `part`, `list`, `archive`, `library`. Supports `epub` and `pdf` output formats. Includes request-cancellation middleware and download throttling.
- **`create_book/`** — Core library:
  - `create_book.py` — Wattpad API client functions (`fetch_story`, `fetch_cookies`, `fetch_list`, etc.) using aiohttp with optional caching.
  - `parser.py` — HTML parsing and image fetching from story content.
  - `generators/epub.py`, `generators/pdf.py` — Book generators. PDF uses WeasyPrint with Jinja2 templates (`generators/pdf/book.html`, `generators/pdf/stylesheet.css`).
  - `config.py` — Pydantic settings from env vars (`USE_CACHE`, `CACHE_TYPE`, `REDIS_CONNECTION_URL`).
  - `vars.py` — Initializes the aiohttp cache backend (file or Redis) at import time.

Cache backend is configurable: file-based (default, 12h TTL) or Redis. Uses a forked `aiohttp-client-cache` with KeyDB TTL support.

### Frontend (`src/frontend/`)

SvelteKit 5 app with Tailwind CSS v4 and DaisyUI. Built as a static site via `@sveltejs/adapter-static`.

- **Routes**: `+page.svelte` (main form), `download/+page.svelte` (download page).
- **i18n**: Client-side translation system in `src/lib/i18n/`. Locale JSON files in `src/lib/i18n/locales/`. To add a locale: create the JSON file, import it in `index.svelte.js`, add to `allTranslations`, `SUPPORTED`, and `LOCALES` arrays.
