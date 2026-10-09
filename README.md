# Food Packaging AI

An intelligent decision-support platform that recommends suitable packaging materials for food commodities based on food properties, storage conditions, barrier properties, cost and sustainability.

Built as a prototype for Smart India Hackathon (SIH) 2026.

## Problem

Choosing the wrong packaging leads to food spoilage, waste and unnecessary cost. Selecting a material means balancing moisture, oxygen and light protection against cost, sustainability and the storage environment. This is difficult to do manually and inconsistently done in practice.

## Solution

Food Packaging AI takes a food commodity (for example Rice, Wheat, Potato, Peanuts or Apple) and its storage conditions, then:

- Scores each packaging material on quality, cost and sustainability.
- Calculates an overall suitability score and ranks the options.
- Estimates shelf life with the recommended packaging against a baseline.
- Explains in plain language why a material was recommended.
- Lets users compare all materials side by side and review past recommendations.

## Features

- User registration and login (token-based authentication)
- Food commodity catalogue with food properties (moisture content, oil/fat content, pH, respiration rate)
- Packaging recommendation with scores, shelf-life estimate, explanation and ranked alternatives
- Packaging comparison table for any commodity and storage condition
- Saved recommendation history per user
- Admin view of packaging materials and commodities

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** React (Vite), Tailwind CSS
- **Architecture:** layered backend with API routers, use cases, repositories and database mappers
- **Auth:** password hashing and bearer access tokens

## Project Structure

```
FoodPackagingAI/
  backend/    FastAPI application (app/main.py, app/api/v1/...)
  frontend/   React + Vite application (src/App.jsx, src/api.js)
```

## API Overview

All routes are under `/api/v1`.

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| POST | `/auth/register` | Create an account | No |
| POST | `/auth/login` | Sign in, returns access token | No |
| GET | `/commodities/` | List food commodities | No |
| POST | `/commodities/` | Add a commodity | No |
| POST | `/recommendations/` | Generate a packaging recommendation | Yes |
| GET | `/history/` | List the user's past recommendations | Yes |
| GET | `/history/{id}` | Get one past recommendation | Yes |
| POST | `/compare/` | Compare packaging materials | No |

Interactive API docs are available at `http://127.0.0.1:8000/docs` when the backend is running.

## Setup and Run

### Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer

### 1. Backend

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

### 2. Frontend

Open a second terminal:

```
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

### 3. Use the app

1. Open `http://localhost:5173`.
2. Register an account, then sign in.
3. Go to Recommendations, choose a commodity, set storage conditions and click Generate.
4. Use Compare Packaging and History to explore further.

## How Scoring Works

Each material is rated on three criteria on a 0 to 10 scale:

- **Quality:** how well the material's barrier properties (moisture, oxygen, light) match the food's needs.
- **Cost:** how economical the material is.
- **Sustainability:** environmental impact of the material.

These are combined into an overall suitability score used to rank materials. Shelf life is estimated by adjusting a baseline for the commodity using the material's protection and the storage conditions.

## Limitations

- The current engine is rule-based. Scores and shelf-life figures are model estimates, not validated food-safety guarantees.
- Results need scientific and laboratory validation before real-world use.
- The dataset covers a small set of commodities and packaging materials.

## Future Scope

- Machine-learning model trained on experimental shelf-life data to predict spoilage and shelf life.
- Larger commodity and material databases, including regional data.
- Cost and carbon-footprint analysis using real supplier and lifecycle data.
- Sensor and IoT integration for live storage monitoring.
- Cloud deployment and an admin console for managing materials.

## Team

Ishita Verma (Leader)
Jugal Mahour
Indresh Pratap Singh
Kunal Singh
Adarsh Chaurasia
Abhishek Verma
