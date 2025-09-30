# Weather App API 🌤️

A lightweight RESTful API built with **Django + Django REST Framework** for fetching weather data.
Supports containerized deployment with Docker.

---

## 📑 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation / Setup](#installation--setup)
- [Usage](#usage)
  - [Environment Variables](#environment-variables)
  - [Endpoints](#endpoints)
- [Healthcheck](#healthcheck)
- [Docker &amp; Docker Compose](#docker--docker-compose)
- [Contributing](#contributing)

---

## 🚀 Features

- Fetch **current weather** and **forecast data** (via provider API OpenWeatherMap).
- Environment-based configuration with `.env`.
- RESTful endpoints with **Django REST Framework (DRF)**.
- **Healthcheck endpoint** for container monitoring.
- Dockerized setup with `docker-compose`.

---

## 🔧 Prerequisites

- Python **3.10+**
- `pip` package manager
- Docker & Docker Compose (if you want containerized setup)
- A valid weather API key ([OpenWeatherMap](https://openweathermap.org/api))

---

## ⚙️ Installation / Setup

1. **Clone this repo**

   ```bash
   git clone https://github.com/CodeVnebula/weather_app_api.git
   cd weather_app_api
   ```
2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   pip install -r weather_app/requirements.txt
   ```
3. **Set up environment variables**

   Copy `.env.example` → `.env` and configure it:

   ```dotenv
   SECRET_KEY="your-secret-key-here"
   WEATHERMAP_API_KEY="your-api-key-here"
   DEBUG=True
   ```
4. **Run migrations & start server**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

   **or If you are running inside Docker**

   ```bash
   docker exec container_name python manage.py makemigrations
   docker exec container_name python manage.py migrate
   ```

---

## 📡 Usage

### Environment Variables

- `WEATHER_API_KEY` → your provider API key (OpenWeatherMap, etc.)
- `SECRET_KEY` → Django secret key
- `DEBUG` → toggle Django debug mode

### Example API Endpoints

| Method | Endpoint                                                      | Description                                                  |
| ------ | ------------------------------------------------------------- | ------------------------------------------------------------ |
| GET    | `/api/current?lat=123.123&lon=123.123`                      | Get current weather by location coordinates                  |
| GET    | `/api/forecast?lat=123.123&lon=123.123`                     | Get forecast (e.g. 5-day)                                    |
| GET    | `/api/locations/?q={city name},{state code},{country code}` | Get location data by name, state code (if USA), country code |
| GET    | `/api/health/`                                              | Healthcheck endpoint (monitoring)                            |

**Sample Request**

```http
GET /api/locations/?q=new-york
```

**Sample Response**

```json
{
    "name": "New York",
    "lat": 40.7127281,
    "lon": -74.0060152,
    "country": "US",
    "state": "New York"
 },
```

---

## ❤️ Healthcheck

Providing a simple healthcheck at `/api/health/`

**Example response**

```json
{
    "status": "ok",
    "time": "2025-09-30T21:07:10.233783+00:00",
    "services": {
        "database": "connected"
    }
}
```

---

## 🐳 Docker & Docker Compose

**Build and run**

```bash
docker-compose up --build
```

The app will be available at `http://localhost:8000`.

## 🤝 Contributing

Contributions are welcome!

---
