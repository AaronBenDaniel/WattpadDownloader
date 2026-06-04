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

**Vite dev server proxy** — already configured in `vite.config.js`. Proxies `/download`, `/activate`, `/admin`, `/user` to `http://localhost:5042`.

**Workflow summary**:

| Changing | Action |
|---|---|
| Backend Python code | Restart `uv run main.py` |
| Frontend (quick iteration) | `npm run dev` with Vite proxy |
| Frontend (full test) | `npm run build`, backend picks it up via symlink |
| Both | Run backend + Vite dev server with proxy |

**Environment variables**: Backend reads from `src/api/.env`. Set `DEBUG=1` to enable Eliot structured logging to `eliot.log`. Feature gating requires `FEATURE_GATING_ENABLED=true`, `REDIS_CONNECTION_URL`, and `ADMIN_API_KEY`.

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

- **`main.py`** — FastAPI app with download endpoint (`GET /download/{download_id}`) that handles five modes: `story`, `part`, `list`, `archive`, `library`. Supports `epub` and `pdf` output formats. Includes request-cancellation middleware, download throttling (per-user `max_download_minutes` via feature gating), and lifespan handler for Redis/user-store init.
- **`routers.py`** — Admin, user, and activation API routers (see Feature Gating section below).
- **`users/`** — User management package:
  - `repository.py` — ABC (`UserRepository`) + Pydantic models (`UserRecord`, `FeatureGrant`). `FeatureGrant` supports `expires_at` (optional expiration) and `value` (optional numeric value for features like `max_download_minutes`).
  - `redis_repository.py` — Redis implementation. Keys: `wpd:user:{uuid}` (primary, stores JSON), `wpd:user:ext:{identifier}` (external identifier → UUID index).
  - **UserRecord fields**: `id` (UUID), `external_identifier` (string, e.g. Discord username), `features` (dict of feature name → `FeatureGrant`), `created_at` (datetime).
  - **FeatureGrant fields**: `expires_at` (optional datetime, `null` = never expires), `value` (optional float, used for numeric features like `max_download_minutes`).
- **`create_book/`** — Core library:
  - `create_book.py` — Wattpad API client functions (`fetch_story`, `fetch_cookies`, `fetch_list`, etc.) using aiohttp with optional caching.
  - `parser.py` — HTML parsing and image fetching from story content.
  - `generators/epub.py`, `generators/pdf.py` — Book generators. PDF uses WeasyPrint with Jinja2 templates (`generators/pdf/book.html`, `generators/pdf/stylesheet.css`).
  - `config.py` — Pydantic settings from env vars (`USE_CACHE`, `CACHE_TYPE`, `REDIS_CONNECTION_URL`, `FEATURE_GATING_ENABLED`, `ADMIN_API_KEY`).
  - `vars.py` — Initializes the aiohttp cache backend (file or Redis) at import time.

Cache backend is configurable: file-based (default, 12h TTL) or KeyDB (Redis-compatible). Uses a forked `aiohttp-client-cache` with KeyDB TTL support. **Note:** This project uses KeyDB, not Redis. The `redis` Python library and `REDIS_CONNECTION_URL` env var are used because KeyDB is wire-compatible with Redis, but the actual database is KeyDB.

### Frontend (`src/frontend/`)

SvelteKit 5 app with Tailwind CSS v4 and DaisyUI. Built as a static site via `@sveltejs/adapter-static` with `fallback: "200.html"` for client-rendered pages.

- **Routes**: `+page.svelte` (main form), `download/+page.svelte` (download page), `activated/+page.svelte` (activation confirmation, client-rendered).
- **State**: `src/lib/stores/features.svelte.js` — reactive feature state backed by localStorage (`wpd-user-id`). Exports `getUserId()`, `setUserId()`, `clearUser()`, `hasFeature()`, `getExternalIdentifier()`, `loadFeatures()`.
- **i18n**: Client-side translation system in `src/lib/i18n/`. Locale JSON files in `src/lib/i18n/locales/` (9 locales). To add a locale: create the JSON file, import it in `index.svelte.js`, add to `allTranslations`, `SUPPORTED`, and `LOCALES` arrays.

### Feature Gating

Per-user feature gating system using Redis. Disabled by default (`FEATURE_GATING_ENABLED=false`).

**Feature keys**:
| Key | Type | Effect |
|---|---|---|
| `pdf_download` | boolean grant | Enables PDF format for single story/part downloads |
| `unrestricted_pdf` | boolean grant | Enables PDF format for bulk downloads (list/archive/library) |
| `max_download_minutes` | numeric (`value` field) | Per-user download time limit in minutes (default: 10) |

**Env vars** (in `src/api/.env`):
```
FEATURE_GATING_ENABLED=true
REDIS_CONNECTION_URL=redis://localhost:6379
ADMIN_API_KEY=your-secret-key
```

**Admin endpoints** (all require `X-API-Key` header):
```bash
# Create user with PDF access and 30-minute download time
curl -X POST http://localhost:5042/admin/users \
  -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"features": {"pdf_download": {}, "max_download_minutes": {"value": 30}}, "external_identifier": "johndoe"}'

# Get user by UUID
curl http://localhost:5042/admin/users/{uuid} -H "X-API-Key: $KEY"

# Get user by external identifier
curl http://localhost:5042/admin/users/by-external/johndoe -H "X-API-Key: $KEY"

# Update user (partial — omitted fields unchanged, null removes a feature)
curl -X PUT http://localhost:5042/admin/users/{uuid} \
  -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"features": {"pdf_download": {"expires_at": "2026-12-31T00:00:00Z"}, "unrestricted_pdf": null}}'

# Delete user
curl -X DELETE http://localhost:5042/admin/users/{uuid} -H "X-API-Key: $KEY"
```

**User-facing endpoints:**
```bash
# Verify server identity (no auth required) and optionally validate API key
curl http://localhost:5042/server/verify                    # => {"server": "WattpadDownloader"}
curl http://localhost:5042/server/verify -H "X-API-Key: $KEY"  # => {"server": "WattpadDownloader", "authenticated": true}

# Check active features (returns {"features": [...]}, cached 5 min)
curl "http://localhost:5042/user/features?user_id={uuid}"

# Activation link (redirects to /activated?id={uuid}, frontend stores UUID)
# Share this URL with users: http://localhost:5042/activate/{uuid}
```

**Activation flow**: Admin creates user -> shares `/activate/{uuid}` link -> user clicks it -> backend validates UUID and redirects to `/activated?id={uuid}` -> frontend stores UUID in localStorage and loads features -> PDF option becomes available in format selector.
