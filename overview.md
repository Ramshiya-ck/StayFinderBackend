# StayFinder Backend Overview

Comprehensive summary of the Django REST backend that powers StayFinder, including tech stack, layout, environment expectations, and deployment/testing workflows.

## Tech Stack & Services
- Python 3.x, Django 5, Django REST Framework, SimpleJWT
- PostgreSQL primary datastore (local + Render managed instance)
- Stripe SDK for payment intents, CORS headers for cross-origin SPA clients
- Gunicorn application server, `render-build.sh` for migrations/static collection

## High-Level Architecture
- `StayFinder` project config holds settings, ASGI/WSGI, URL routing.
- Domain-specific Django apps (`user`, `customer`, `Hotel`, `Room`, `booking`, `Request`, `Payment`) encapsulate models and admin registrations.
- API layer lives under `api/v1/<domain>/` with serializers and function-based views organized per feature (hotel search, room CRUD, booking flow, customer profiles, payment integration).
- Media assets stored under `media/` with per-feature upload subfolders; static assets collected into `staticfiles/` for deployment.

## Directory Layout (trimmed)
```
StayFinder/
├── api/
│   └── v1/
│       ├── booking/
│       ├── customer/
│       ├── hotel/
│       ├── request/
│       └── room/
├── booking/
├── customer/
├── Hotel/
├── Room/
├── Request/
├── Payment/
├── user/
├── StayFinder/              # settings, urls, wsgi/asgi
├── media/                   # uploaded assets
├── static/                  # local static assets
├── manage.py
├── requirements.txt
├── Procfile
└── render-build.sh
```

## Django Apps & Models
- `user`: custom `User` model (email login, role flags) with `UserManager`.
- `customer`: wraps `Customer` and `Profile` (default profile enforcement).
- `Hotel`: `Hotal` entity (manager linkage, slider banner support).
- `Room`: room inventory with type, price, availability, hotel FK.
- `booking`: booking lifecycle (status + payment statuses, amount auto-calculation).
- `Payment`: Stripe-aligned records referencing bookings.
- `Request`: handles partner hotel onboarding requests.
- Each app maintains its own migrations under `<app>/migrations/`.

## API Layer
- Namespaced under `api.v1`, imported into `StayFinder/urls.py`.
- Views use DRF function-based handlers; authentication enforced via JWT where required (`IsAuthenticated`), `AllowAny` for public browsing endpoints.
- Serializers live beside the views per domain to keep DTO logic close to feature modules.
- Example flows:
  - Hotels: public listing/search, authenticated detail, manager edit/delete.
  - Rooms: CRUD tied to `Hotel` inventory.
  - Booking: create/update bookings, compute balances, tie into payments.
  - Customer: profile management and address book.

## Settings & Configuration
- Environment controlled via `.env` (loaded through `python-dotenv`).
- Critical variables: `SECRET_KEY`, `DEBUG`, `DATABASE_URL` (Render), `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_CURRENCY`.
- `DEBUG=True` -> local Postgres connection defined inline; `DEBUG=False` -> `dj_database_url` parses `DATABASE_URL` (SSL enforced).
- CORS fully open (`CORS_ALLOW_ALL_ORIGINS=True`) — adjust for production security if needed.
- `AUTH_USER_MODEL = 'user.User'`, JWT tokens last 365 days.

## Local Development Workflow
1. Create `.env` beside `manage.py`:
   ```
   SECRET_KEY=local-secret
   DEBUG=True
   STRIPE_SECRET_KEY=...
   STRIPE_PUBLISHABLE_KEY=...
   STRIPE_CURRENCY=usd
   ```
2. Install dependencies: `pip install -r requirements.txt`.
3. Ensure Postgres is running and matches `StayFinder/StayFinder/settings.py` local credentials (NAME, USER, PASSWORD, HOST, PORT). Update as needed.
4. Run migrations: `python manage.py migrate`.
5. Create superuser: `python manage.py createsuperuser --email admin@example.com`.
6. Start dev server: `python manage.py runserver`.
7. Optionally seed data using the Django admin or custom scripts.

## Testing
- Default Django test runner: `python manage.py test`.
- App-level tests currently minimal; recommended to expand coverage for API views and serializers.
- For manual verification, use DRF browsable API or an API client (Postman) with JWT tokens obtained via the auth endpoints.

## Deployment on Render
1. Push code to GitHub.
2. Create a Render PostgreSQL instance; copy its `DATABASE_URL`.
3. Create a Render Web Service:
   - Start command handled via `Procfile` (`web: gunicorn StayFinder.wsgi:application`).
   - Build command: `./render-build.sh` (executes migrations + `collectstatic`).
4. Configure environment variables:
   - `SECRET_KEY`, `DEBUG=False`
   - `DATABASE_URL` (from managed Postgres)
   - `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_CURRENCY`
   - Optional: `ALLOWED_HOSTS` if using different domain.
5. Set auto-deploy from the main branch.
6. After first deploy, verify static files served (Render auto-serves via Gunicorn + `whitenoise` dependency if enabled) and media storage strategy (currently local `media/`; consider S3 or Render persistent disk for production).

## Operational Notes & Next Steps
- Media uploads stored on the app filesystem; for scalable deployments switch to cloud storage.
- JWT lifetime is 1 year; adjust for security posture.
- `hotel_search` view contains redundant filtering logic — consider refactor.
- Add automated tests for booking/payment flows and permissions.
- Consider adding DRF viewsets/routers for consistency and schema generation (Swagger/OpenAPI).


