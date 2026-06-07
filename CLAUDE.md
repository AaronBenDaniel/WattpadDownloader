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

**Clone with submodules** — the `epublib` dependency lives in a git submodule at `src/api/lib/epublib/`:
```bash
git clone --recurse-submodules <repo-url>
# or, if already cloned:
git submodule update --init
```

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

**Vite dev server proxy** — already configured in `vite.config.js`:
```js
server: {
  proxy: {
    '/auth': 'http://localhost:5042',
    '/download': 'http://localhost:5042',
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

**Environment variables**: Backend reads from `src/api/.env`. Key variables:

| Variable | Purpose | Default |
|---|---|---|
| `USE_CACHE` | Enable aiohttp response caching | `true` |
| `CACHE_TYPE` | `file` or `redis` | `file` |
| `REDIS_CONNECTION_URL` | Redis/KeyDB connection string | (empty) |
| `DEBUG` | Enable Eliot structured logging to `eliot.log` | (unset) |
| `DISCORD_AUTH_ENABLED` | Toggle Discord OAuth feature gating | `true` |
| `DISCORD_CLIENT_ID` | Discord OAuth app client ID | (empty) |
| `DISCORD_CLIENT_SECRET` | Discord OAuth app client secret | (empty) |
| `DISCORD_BOT_TOKEN` | Bot token for guild member lookups | (empty) |
| `DISCORD_GUILD_ID` | Guild to check membership against | (empty) |
| `DISCORD_UNRESTRICTED_ACCESS_ROLE_ID` | Role granting unlimited downloads | (empty) |
| `DISCORD_REDIRECT_URI` | OAuth callback URL | `http://localhost:5042/auth/discord/callback` |
| `JWT_SECRET` | Secret for signing session JWTs | (empty) |
| `COOKIE_SECURE` | Set `false` for HTTP dev servers | `true` |

When `DISCORD_AUTH_ENABLED=false`, all premium features (PDF, bulk downloads, no throttling) are available without login.

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

- **`main.py`** — FastAPI app with download endpoint (`GET /download/{download_id}`) handling five modes: `story`, `part`, `list`, `archive`, `library`. Supports `epub` and `pdf` output formats. Includes request-cancellation middleware and download speed throttling (tiered by auth role).
- **`auth.py`** — Discord OAuth2 authentication with guild-gated PDF access. Provides:
  - OAuth2 login/callback flow (`/auth/discord/login`, `/auth/discord/callback`)
  - Session management via JWT in httpOnly cookies (`/auth/me`, `/auth/logout`)
  - Guild membership and role checks via Discord Bot API (cached 30min)
  - `require_pdf_access()` guard for PDF downloads; `has_unrestricted_access()` for bulk/unlimited
  - `DISCORD_AUTH_ENABLED` flag to bypass all auth checks
- **`create_book/`** — Core library:
  - `create_book.py` — Wattpad API client functions (`fetch_story`, `fetch_cookies`, `fetch_list`, `fetch_archive`, `fetch_library`, `fetch_username`) using aiohttp with optional caching and exponential backoff.
  - `models.py` — TypedDict definitions (`Story`, `List`, `Part`, `User`, `Language`, `CopyrightData`).
  - `exceptions.py` — `WattpadError` → `StoryNotFoundError` → `PartNotFoundError`.
  - `parser.py` — HTML parsing and image fetching from story content.
  - `generators/epub.py`, `generators/pdf.py` — Book generators. PDF uses WeasyPrint with Jinja2 templates (`generators/pdf/book.html`, `generators/pdf/stylesheet.css`). PDF supports Creative Commons license rendering.
  - `config.py` — Pydantic settings from env vars (`USE_CACHE`, `CACHE_TYPE`, `REDIS_CONNECTION_URL`).
  - `vars.py` — Initializes the aiohttp cache backend (file or Redis) at import time.
  - `logs.py` — Eliot structured logging setup.

**Download throttling**: Unauthenticated users get 10-minute max download time; guild members get 5 minutes; users with unrestricted-access role get no throttle. When `DISCORD_AUTH_ENABLED=false`, throttling is disabled for all users.

Cache backend is configurable: file-based (default, 12h TTL) or Redis. Uses a forked `aiohttp-client-cache` with KeyDB TTL support.

### Frontend (`src/frontend/`)

SvelteKit 5 app with Tailwind CSS v4 and DaisyUI 5. Built as a static site via `@sveltejs/adapter-static`.

- **Routes**: `+page.svelte` (main download form), `download/+page.svelte` (post-download landing).
- **Themes**: Light (`bumblebee`) and dark (`abyss`) via DaisyUI, toggled with `ThemeToggle.svelte`. Custom CSS vars for dark theme in `app.css`.
- **Components**: `src/lib/components/` — `LanguageSelector.svelte`, `ThemeToggle.svelte`. Icons in `src/lib/icons/`.
- **Auth integration**: The main form fetches `/auth/me` on mount to determine `hasPdfAccess`, `hasUnrestrictedAccess`, and `authDisabled` state. When auth is disabled, Discord login UI is hidden and all formats are available. When auth is enabled, PDF format is gated behind Discord guild membership.
- **i18n**: Client-side translation system in `src/lib/i18n/`. Locale JSON files in `src/lib/i18n/locales/` (en, vi, th, si, my, es, pt, tr, ms). To add a locale: create the JSON file, import it in `index.svelte.js`, add to `allTranslations`, `SUPPORTED`, and `LOCALES` arrays.
- **`svelte.config.js`**: Prerender errors for `/auth/` paths are suppressed (these are backend-only routes).
