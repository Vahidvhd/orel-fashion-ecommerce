# Orel Fashion — Premium Online Fashion Store

Production-ready Django 5 ecommerce platform for a single fashion brand with multiple branch locations. English-language storefront inspired by premium retailers (Zara, H&M, M&S).

## Tech Stack

- **Backend:** Python 3.12, Django 5, Django REST Framework
- **Frontend:** Django Templates, Tailwind CSS, Alpine.js, HTMX
- **Database:** PostgreSQL (SQLite for quick local dev)
- **Async:** Celery + Redis
- **Payments:** Stripe test-mode mock flow
- **Storage:** Local media (dev) or Cloudinary (production)

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed
python manage.py runserver
```

Visit http://127.0.0.1:8000/

### Demo Accounts (after seed)

| Role     | Email                      | Password      |
|----------|----------------------------|---------------|
| Admin    | admin@maisonatelier.com    | admin12345    |
| Customer | customer@example.com       | customer123   |

## Features

- Fullscreen editorial hero (image/video) — navbar + hero = 100vh
- Scroll-triggered Men/Women category cards
- Product variants (color + size) with independent stock/pricing/discounts
- Predefined colors, sizes, categories (admin selects, never free-text)
- Multi-filter catalog + sorting (HTMX partial updates)
- Sale discounts with live countdown timers
- Email verification before login
- Country restriction middleware (IR + GB only for auth)
- Session + user carts with badge count
- Checkout → mock Stripe payment → order tracking
- Branch locations with map embeds in footer
- Docker, Gunicorn, Nginx-ready deployment

## Country Restriction (Auth Only)

Browsing works globally. Login/register require geo headers:

- `CF-IPCountry` (Cloudflare)
- `X-Country-Code`
- `X-Debug-Country` (development)

Allowed: **IR**, **GB**

## Running Tests

```bash
pytest
```

## Docker

```bash
cp .env.example .env
docker compose up --build
```

Services: `web`, `db` (PostgreSQL), `redis`, `celery`, `nginx`

## Environment Variables

See `.env.example` for all options including `DATABASE_URL`, `REDIS_URL`, `STRIPE_*`, `CLOUDINARY_*`, `ALLOWED_AUTH_COUNTRIES`.

## Project Structure

```
config/           # Settings (dev/test/production), URLs, Celery
apps/
  accounts/       # User, verification
  catalog/        # Products, variants, discounts
  cart/           # Cart system
  orders/         # Orders, checkout
  core/           # Hero, branches, geo middleware
  storefront/     # Views & templates
  api/            # DRF endpoints
templates/        # Premium UI templates
static/           # CSS & JS animations
tests/            # Pytest suite
deploy/           # Nginx config
```

## Production Settings

```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## License

Proprietary — Orel Fashion demo project.
