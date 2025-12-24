# My CI/CD App

A multi-service containerized application with FastAPI backend, React frontend, PostgreSQL database, and Kubernetes orchestration using Kluctl and Taskfile.

## 📁 Project Structure

```
my-ci-cd-app/
├── services/
│   ├── backend/
│   │   ├── main.py              # FastAPI application
│   │   ├── engine.py            # SQLAlchemy async engine config
│   │   ├── metrics.py           # Prometheus metrics
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── Dockerfile           # Docker build for Python service
│   │   ├── .dockerignore        # Docker exclude patterns
│   │   └── Taskfile.yaml        # Task automation
│   │
│   ├── frontend/
│   │   ├── src/                 # React source code
│   │   ├── package.json         # Node.js dependencies
│   │   ├── vite.config.ts       # Vite build configuration
│   │   ├── tsconfig.json        # TypeScript configuration
│   │   ├── eslint.config.js     # ESLint rules
│   │   ├── index.html           # HTML entry point
│   │   ├── nginx.conf           # Nginx configuration
│   │   ├── Dockerfile           # Multi-stage Docker build
│   │   └── .dockerignore        # Docker exclude patterns
│   │
│   └── database/
│       ├── migrations/          # Database migration files
│       ├── Dockerfile           # Migrate tool container
│       └── .dockerignore        # Docker exclude patterns
│
├── k8s/
│   ├── application/
│   │   ├── deployment.yaml      # Kluctl deployment configuration
│   │   ├── .kluctl.yaml         # Kluctl project settings
│   │   ├── services/
│   │   │   └── application/     # Application services
│   │   │       ├── backend/     # Backend Helm charts
│   │   │       ├── frontend/    # Frontend Helm charts
│   │   │       └── database/    # Database configurations
│   │   └── config/
│   │       ├── staging.yaml     # Staging environment vars
│   │       └── production.yaml  # Production environment vars
│   │
│   └── controller/
│       ├── deployment.yaml      # Controller deployment
│       ├── Taskfile.yaml        # Deployment tasks
│       ├── clusters/            # Cluster configurations
│       ├── namespaces/          # Namespace definitions
│       └── .kluctl.yaml         # Kluctl settings
│
├── pyproject.toml               # Project metadata (Python)
├── uv.lock                      # UV lock file (dependency lock)
├── .python-version              # Python version (3.13)
├── .gitignore                   # Git exclusions
├── locustfile.py                # Load testing scenarios
└── main.py                      # Root entry point
```

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (for containerization)
- **Python 3.13** (for backend development)
- **Node.js 20+** (for frontend development)
- **Kubernetes cluster** (for deployment)
- **Kluctl** (for GitOps deployments)
- **Task** (task runner)
- **PostgreSQL** (database backend)

### Local Development

**Backend Setup:**
```bash
cd services/backend
pip install -r requirements.txt
# Set up environment variables
export BACKEND_DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/mydb"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend Setup:**
```bash
cd services/frontend
npm install  # or yarn install
npm run dev  # Vite dev server on http://localhost:5173
```

**Database Setup:**
```bash
docker build -t my-db-migrator services/database/
docker run my-db-migrator  # Run migrations against your DB
```

### Docker Compose Stack (coming soon)

For local full-stack development, add a `docker-compose.yml`:
```bash
docker-compose up
```

## 📦 Services Overview

### Backend (FastAPI)
- **Port:** 8000
- **Metrics:** `/metrics` (Prometheus)
- **Health Check:** `/health`
- **API:** `/requests`, `/react`
- **Features:**
  - Async database operations (SQLAlchemy)
  - CORS middleware enabled
  - Prometheus metrics collection
  - Database connection pooling

### Frontend (React + Vite)
- **Port:** 5173 (dev), 8080 (production)
- **Build Tool:** Vite
- **Linting:** ESLint with TypeScript
- **Runtime:** Node.js 20
- **Served via:** Nginx (production)

### Database (PostgreSQL)
- Managed via migration tool
- Runs async migrations on deployment
- Connection pooling from backend

## 🔧 Development Workflow

### Available Tasks

```bash
# Backend tasks
cd services/backend && task

# Controller deployment
cd k8s/controller && task -l
task deploy-staging-cluster
task deploy-production-cluster
task get-webui-password
task port-forward-webui
```

### Environment Configuration

Create `.env` files in respective directories:

**Backend `.env`:**
```
BACKEND_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
REACT_PUBLIC_ANTON=your-config-value
```

**Frontend `.env`:**
```
VITE_API_URL=http://localhost:8000
```

### Load Testing

Run load tests using Locust:
```bash
pip install locust
locust -f locustfile.py --host=http://localhost:8000
```

## 🐳 Docker Builds

### Backend
- **Base:** `python:3.11-slim`
- **Optimization:** Multi-stage with cached pip
- **User:** Non-root `backend` user
- **Entrypoint:** Uvicorn

### Frontend
- **Base:** `node:20.14` (build) → `nginxinc/nginx-unprivileged` (runtime)
- **Optimization:** Multi-stage, npm cache mounting
- **Entrypoint:** Nginx

### Database
- **Base:** `migrate/migrate:v4.17.1`
- **Usage:** Container for running migrations

## 🌍 Kubernetes Deployment

### Configuration Management

- **Tool:** Kluctl + Helm
- **GitOps:** Configuration in `/k8s/application/config/`
- **Environments:**
  - `staging.yaml` - Staging deployments
  - `production.yaml` - Production deployments

### Deployment

```bash
cd k8s/controller
task deploy-staging-cluster   # Deploy to staging
task deploy-production-cluster # Deploy to production
```

### Accessing Web UI

```bash
task port-forward-webui
# Get admin password
task get-webui-password
# Open http://localhost:8080
```

## 📊 Monitoring & Metrics

- **Prometheus Metrics:** `/metrics` endpoint (FastAPI)
- **Tracked Metrics:**
  - `fastapi_requests_total` - Total HTTP requests
  - `fastapi_responses_total` - Response counts by status code
  - `fastapi_exceptions_total` - Exception counts
  - `fastapi_requests_duration_seconds` - Request latency histogram
  - `fastapi_requests_in_progress` - Current in-flight requests

## 🛠️ Build & Deployment

### Local Container Build

```bash
# Backend
docker build -t my-backend:latest services/backend/

# Frontend
docker build -t my-frontend:latest services/frontend/

# Database
docker build -t my-database:latest services/database/
```

### Registry Push (update as needed)

```bash
docker tag my-backend:latest ghcr.io/vlad-yarko/my-backend:latest
docker push ghcr.io/vlad-yarko/my-backend:latest
```

## 🗂️ Cache & Build Artifacts (Excluded from Git)

**Recommended `.gitignore` additions:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
*.egg-info/
dist/
build/

# Node/Frontend
services/frontend/node_modules/
services/frontend/dist/
services/frontend/.vite/
*.tsbuildinfo

# Environment files
.env
.env.local
.env.*.local

# Docker
.dockerignore

# IDE
.vscode/
.idea/
*.swp
*.swo
```

## 📝 Code Quality

### Backend
- Python 3.13+
- FastAPI + Uvicorn
- SQLAlchemy ORM
- Async/await patterns

### Frontend
- React 19.2
- TypeScript 5.9
- Vite 7.2
- ESLint + TypeScript ESLint

### Linting & Formatting

```bash
# Frontend
npm run lint
npm run build  # Type check + build
```

## 🚨 Known Issues & TODOs

- [ ] Docker Compose configuration needed for local dev
- [ ] Add integration tests
- [ ] Configure CI/CD pipeline (GitHub Actions, etc.)
- [ ] Add database schema documentation
- [ ] Implement API documentation (Swagger)
- [ ] Add secret management (Sealed Secrets for K8s)
- [ ] Performance profiling for load testing

## 📚 Dependencies

### Python (Backend)
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `asyncpg` - PostgreSQL async driver
- `prometheus-client` - Metrics
- `python-dotenv` - Environment management

### Node (Frontend)
- `react` - UI library
- `vite` - Build tool
- `typescript` - Type safety
- `axios` - HTTP client
- `eslint` - Linting

## 🔐 Security Considerations

- Backend user runs as non-root in Docker
- CORS configured for localhost dev (update for production)
- Environment variables for sensitive data
- Nginx unprivileged image for frontend

## 📞 Support & Contribution

For issues or improvements, please check the project structure and tests before submitting changes.

---

**Last Updated:** 2025-12-24  
**Python Version:** 3.13  
**Node Version:** 20.14+