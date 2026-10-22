Db2 Service Portal

A read-only web portal for monitoring the health and performance of IBM Db2 LUW databases. It collects the key indicators a DBA checks every day (health status, locks, long-running queries, buffer pool and cache hit ratios, backups, HADR state, diagnostic log entries and more) and shows them in one dashboard, so DBAs and support teams can triage issues quickly without running manual queries.

Stack: FastAPI (Python) · React 19 + Vite · IBM Db2 LUW (ibm_db) · Docker · Jenkins

<img width="1280" height="745" alt="SP_Db2_2" src="https://github.com/user-attachments/assets/3a0c0983-e493-41fd-8190-143692984177" />
Features

The dashboard has four views, each backed by its own API endpoint.

DB-Summary: instance and database name, service level, database size, partitions (DPF), HADR role and state.

DB-Health: one card per check, with a clear "all normal" or detail view when something is wrong:

Database status, activation state, connection status and start time
Lock waits, lock escalations and lock timeouts
Log utilisation and database memory
Latest full, incremental and delta backups
Tablespace, container and table states
HADR status
Load-pending, reorg-pending and index-rebuild-pending tables
Invalid views, packages, triggers and other invalid objects
Event monitor errors
Tables without a primary key
Running utilities
<img width="1280" height="745" alt="SP_db2_3" src="https://github.com/user-attachments/assets/10c17d1e-a599-43e5-b6a9-cd5d9dc414f2" />

DB-Performance:

Buffer pool, package cache and catalog cache hit ratios
Deadlocks, lock escalations and lock timeouts, with current lock details
Long-running queries
Problem queries: high CPU, frequently executed, top sort, table scans and temp-table usage
Table read efficiency, I/O wait and HADR log gap
<img width="1280" height="787" alt="SP_DB2_4" src="https://github.com/user-attachments/assets/b17b478b-4368-4522-8e9c-1029e9f98231" />

DiagLog: db2diag entries from the last 24 hours, split by severity (critical, error, warning, info).

<img width="1280" height="524" alt="SP_Db2_5" src="https://github.com/user-attachments/assets/288830bd-7a85-42d2-85ec-cab521d9ed44" />

All checks only read from Db2 monitoring functions and administrative views (MON_GET_*, SYSIBMADM.*, SYSCAT.*). The portal does not change anything in the database.

Architecture
React (Vite, nginx)  ──HTTP/JSON──▶  FastAPI backend  ──ibm_db──▶  Db2 LUW
   dashboard                          /api/v1/...                  monitoring views

The database name is part of the URL, so one backend can serve several databases on the same Db2 server.

.
├── backend/               # FastAPI app
│   └── app/
│       ├── api/           # Routes: databases, healthcheck, performance, db2diag
│       ├── services/      # Health, performance, summary and diag-log queries
│       ├── db/            # Db2 connection (ibm_db)
│       └── main.py
├── frontend/              # React + Vite dashboard (served by nginx in Docker)
├── docker-compose.yml     # Db2 test container + backend + frontend
└── Jenkinsfile            # Builds and pushes both Docker images
Getting started
Option 1: Docker Compose (quickest)

Starts a Db2 test container, the backend and the frontend.

bash
git clone https://github.com/abhianand20/db2_serviceportal.git
cd db2_serviceportal
docker compose up --build
Service	URL
Frontend	http://localhost:5174
Backend API docs	http://localhost:8000/docs
Db2	localhost:50000

The Db2 image takes several minutes to create the database on first start. The compose file uses a throwaway test password; change it for anything beyond local testing.

Option 2: Run locally against your own Db2

Backend (Python 3.11):

bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

Create backend/.env:

DB2_HOST=your-db2-host
DB2_PORT=50000
DB2_USER=monitor_user
DB2_PASSWORD=your-password
bash
uvicorn app.main:app --reload --port 8000

Frontend (Node 18+):

bash
cd frontend
npm install
npm run dev

The frontend reads the API address from VITE_API_BASE (default http://localhost:8000/api/v1). To change it, set the variable before building:

bash
VITE_API_BASE=http://your-host:8000/api/v1 npm run build
API

Base path: /api/v1/databases/{db_name}

Endpoint	Description
GET /summary	Instance, size, partitions and HADR summary
GET /healthcheck	All health-check results
GET /performance	Hit ratios, locking, problem queries
GET /db2diag/crit	Critical diagnostic log entries
GET /db2diag/err	Error entries
GET /db2diag/warn	Warning entries
GET /db2diag/info	Informational entries

There is also GET /health on the backend as a simple liveness check. Full interactive documentation is at /docs (Swagger UI).

Required Db2 privileges

Use a dedicated monitoring user. It needs permission to run the monitoring table functions and read the administrative views the checks use, for example EXECUTE on MON_GET_* and SELECT on SYSIBMADM and SYSCAT views, plus the DBADM-level or monitoring authority your Db2 version requires for those functions.

CI/CD and deployment
The Jenkinsfile builds the frontend and backend images in parallel, tags them with the build number and latest, and pushes them to Docker Hub.
The frontend image takes VITE_API_BASE as a build argument, so the same code can point at different backends.
The frontend's nginx config exposes a /health endpoint for container and Kubernetes health probes.
Security notes
Use a read-only monitoring account with the minimum privileges required.
Keep credentials in environment variables or a secrets manager. .env is git-ignored; never commit it.
The backend currently allows requests from any origin (CORS *) and has no authentication. Restrict the allowed origins and put it behind authentication and TLS before exposing it outside a trusted network.
Roadmap
 Authentication and role-based access
 Alert thresholds and notifications
 Prometheus metrics endpoint
 Kubernetes manifests / Helm chart
 Additional checks (CPU utilisation, disk I/O, filesystem usage, temp-table availability)
License

TBD

Author

Abhishek Anand · Database Reliability Engineer · 
LinkedIn: https://www.linkedin.com/in/abhishek-anand2015
