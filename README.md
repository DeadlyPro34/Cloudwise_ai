# CloudWise AI

## Overview
**Autonomous FinOps Copilot for AWS Infrastructure**

CloudWise AI connects to your AWS account, discovers infrastructure, analyzes costs, detects anomalies, forecasts spending, generates optimization recommendations, and explains it all in plain English via an AI Copilot.

## Features
- **User Authentication:** Secure JWT-based auth with Argon2 password hashing.
- **AWS Integration:** IAM role-based AWS account connection UI with read-only access (with LocalStack fallback for local testing).
- **Resource Discovery:** UI and backend integrations for AWS EC2 and EBS.
- **Cost Analysis:** In-depth cost tracking and an overall Cloud Health Score.
- **Recommendations Engine:** Identifies idle and unattached resources for rightsizing.
- **Spend Forecasting:** Uses ML (Prophet) to predict future AWS costs.
- **AI Copilot:** Groq Llama 3.3 70B API integration to answer plain-English questions about your cloud environment.
- **Reporting:** Downloadable PDF reports for infrastructure and costs.

## Tech Stack
- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS v4, TanStack Query, Recharts, Nginx (Proxy & Serving)
- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic v2
- **Database & Cache:** PostgreSQL 16, Redis (Caching & Rate Limiting)
- **AWS & ML:** Boto3, LocalStack (Local AWS mock), scikit-learn, Prophet (forecasting)
- **AI & Auth:** Groq API (Llama 3.3 70B), JWT, Argon2
- **Tools/Deployment:** Docker Compose, Docker Multi-stage Builds

---

## Installation & Running Locally (Recommended: Docker Compose)

The easiest and most reliable way to run the entire application stack locally is using Docker Compose. This will automatically spin up the Frontend, Backend, PostgreSQL database, Redis instance, and LocalStack environment.

### Prerequisites
- [Docker & Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- A Groq API key (Free at https://console.groq.com).
- Optional: LocalStack installed locally if you prefer running it outside of Docker (the application uses `host.docker.internal` to connect to it).

### 1. Clone the repository
```bash
git clone <YOUR_REPO_URL>
cd cloudwise-ai
```

### 2. Environment Configuration
You need to set up the environment variables for the backend and frontend. 

**Backend (`backend/.env`):**
```bash
cd backend
cp .env.example .env
```
*Edit `backend/.env` and add your `GROQ_API_KEY` along with a random `ENCRYPTION_KEY` and `JWT_SECRET`. To generate a secure encryption key, run: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`*

**Frontend (`frontend/.env`):**
```bash
cd ../frontend
cp .env.example .env
```
*(The defaults in the frontend `.env` are pre-configured to work perfectly with the Docker Nginx Proxy setup.)*

### 3. Run the Application
Navigate back to the root of the project where `docker-compose.yml` is located and run:

```bash
# Build and start all services in the background
docker-compose up --build -d
```

### 4. Access the Application
- **Frontend App:** Open your browser to http://localhost:5173
- **Backend API Docs:** Open your browser to http://localhost:8000/docs
- **Nginx Proxy:** The frontend container automatically routes any traffic starting with `/api/v1/` to the backend container to bypass CORS restrictions entirely.

### 5. Managing the Containers
To view live logs from the containers:
```bash
docker-compose logs -f
```
To stop the application:
```bash
docker-compose down
```

---

## Running Locally (Manual Development Mode)

If you need to run the application natively for active debugging without Docker:

### Prerequisites
- Python 3.11+
- Node.js 22+
- A running PostgreSQL instance (or remove `DATABASE_URL` in `.env` to fallback to SQLite)
- A running Redis instance (or remove `REDIS_URL` in `.env` to fallback to Memory Limiter)

### Start the Backend
```bash
cd backend
python -m venv venv

# Activate Virtual Environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head           # Run database migrations
uvicorn app.main:app --reload --port 8000
```

### Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173 and will directly communicate with the backend at `http://localhost:8000`.

---

## AWS Integration & LocalStack
The application has built-in support for mocking AWS API responses using LocalStack to avoid incurring any costs during development.

If you have LocalStack running on your host machine (e.g., `localstack start`), the backend Docker container will automatically route AWS credential verifications to `http://host.docker.internal:4566`. Ensure you toggle "Use LocalStack Mock Environment" in the UI when connecting.

## API Endpoints Reference
Once the backend is running, you can access the interactive Swagger documentation at `http://localhost:8000/docs`.

**Key Endpoints:**
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Authenticate and receive JWT
- `GET /api/v1/dashboard` - Fetch dashboard KPIs (Cached via Redis)
- `POST /api/v1/aws/connect` - Authenticate AWS IAM credentials
- `GET /api/v1/aws/resources` - Fetch discovered AWS resources
- `POST /api/v1/copilot/chat` - Interact with the AI Copilot

## License
This project is licensed under the MIT License - see the LICENSE file for details.
