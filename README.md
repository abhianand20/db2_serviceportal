Db2 Service Portal

A web application for monitoring the health of IBM Db2 LUW databases. It gathers the key health indicators (locks, long-running queries, bufferpool status and more) and presents them in a single dashboard, so DBAs and support teams can triage issues quickly without running manual queries.

Stack: FastAPI (Python) backend · React frontend · IBM Db2 LUW

<img width="1280" height="745" alt="SP_Db2_2" src="https://github.com/user-attachments/assets/3a0c0983-e493-41fd-8190-143692984177" />


Features
Lock monitoring: current lock waits and lock holders
Long-running queries: active statements above a configurable runtime threshold
Bufferpool status: bufferpool usage and hit ratios

<img width="1280" height="745" alt="SP_db2_3" src="https://github.com/user-attachments/assets/10c17d1e-a599-43e5-b6a9-cd5d9dc414f2" />

<img width="1280" height="787" alt="SP_DB2_4" src="https://github.com/user-attachments/assets/b17b478b-4368-4522-8e9c-1029e9f98231" />


Single-view dashboard: health indicators for a database at a glance
REST API: every check is available as an endpoint, so it can be reused by scripts or other tools
<!-- TODO: add or remove checks to match what the portal actually covers (tablespaces, backups, HADR, connections, etc.) -->
Architecture
React dashboard  ──HTTP/JSON──▶  FastAPI backend  ──SQL──▶  Db2 LUW
                                 (health checks)         (monitoring views / admin functions)
The backend runs health-check queries against Db2 monitoring interfaces and exposes the results as JSON.
The frontend calls the API and renders the results.
Prerequisites
Python 3.10+
Node.js 18+ and npm
Network access to a Db2 LUW instance
A Db2 user with privileges to query the monitoring views (for example, EXECUTE on the monitoring functions and SELECT on the relevant administrative views)

<img width="1280" height="524" alt="SP_Db2_5" src="https://github.com/user-attachments/assets/288830bd-7a85-42d2-85ec-cab521d9ed44" />

<!-- TODO: Db2 client / driver requirement (for example the ibm_db Python package) -->
Getting started
1. Clone the repository
bash
git clone https://github.com/<your-username>/<repo>.git
cd <repo>
2. Backend
bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then edit with your Db2 connection details
uvicorn main:app --reload

The API runs on http://localhost:8000. Interactive API docs are at http://localhost:8000/docs.

3. Frontend
bash
cd frontend
npm install
npm start

The dashboard runs on http://localhost:3000.

<!-- TODO: confirm folder names, entry-point module and start commands match the repo -->
Configuration

Set these in backend/.env:

Variable	Description	Example
DB2_HOST	Db2 server hostname	db2host.example.com
DB2_PORT	Db2 port	50000
DB2_DATABASE	Database name	SAMPLE
DB2_USER	Monitoring user	monitor_user
DB2_PASSWORD	Password for that user	(do not commit)

Never commit .env or credentials. Use a read-only monitoring account with the minimum privileges required.

API overview
Endpoint	Description
GET /locks	Current lock waits and holders
GET /long-running-queries	Statements running longer than a threshold
GET /bufferpools	Bufferpool status and hit ratios
<!-- TODO: replace with your real routes, or link to /docs -->
Project structure
.
├── backend/     # FastAPI app and Db2 health-check logic
├── frontend/    # React dashboard
└── README.md
<!-- TODO: update to match the real layout -->
Roadmap
 Alert thresholds and notifications
 Prometheus metrics endpoint
 Docker / docker-compose packaging
 Multi-database support
<!-- TODO: keep only the items you actually plan to build -->
Security notes
Use a dedicated read-only monitoring user.
Keep credentials in environment variables or a secrets manager, never in source control.
Run the API behind authentication and TLS if you deploy it beyond a local environment.
License
<!-- TODO: choose a license, for example MIT -->
Author

Abhishek Anand · Database Reliability Engineer · LinkedIn
