# CCODEL Tickets

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/Frontend-React_19-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Bundler-Vite_6-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Styles-Tailwind_CSS_4-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy_2.0-D71F00?style=flat)](https://www.sqlalchemy.org/)

A multi-role ticketing and student support helpdesk platform developed for **CCODEL** (Centre for Continuing Education / Distance and Open Learning). The platform bridges distance-learning students, designated support staff, and administrative teams to track, triage, and resolve academic, administrative, and technical issues.

---

## Table of Contents

- [Overview](#overview)
- [Key Features & Role Matrix](#key-features--role-matrix)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Backend Setup (FastAPI)](#2-backend-setup-fastapi)
  - [3. Frontend Setup (React + Vite)](#3-frontend-setup-react--vite)
- [Environment Variables](#environment-variables)
- [API Overview](#api-overview)
- [Current Project Status & Roadmap](#current-project-status--roadmap)
- [License](#license)

---

## Overview

Distance and open-learning students frequently encounter barriers relating to portal access, course registration, tuition verification, and academic advisement. **CCODEL Tickets** organizes these inquiries into structured, trackable tickets with distinct priority levels, department categories, audit histories, file attachments, and direct student-to-support messaging.

---

## Key Features & Role Matrix

| Feature | Student | Support Staff | Administrator |
| :--- | :---: | :---: | :---: |
| **Authentication & Profile Management** | ✅ | ✅ | ✅ |
| **Create Support Tickets (with Attachments)** | ✅ | — | — |
| **Track Submitted Tickets & Real-Time Status** | ✅ | — | — |
| **Cancel Submitted Ticket** | ✅ | — | ✅ |
| **Ticket Discussion / Comments Thread** | ✅ (Assigned) | ✅ (Assigned) | ✅ |
| **View Assigned Tickets Queue** | — | ✅ | — |
| **Update Ticket Status (In Progress, Resolved, Closed)** | — | ✅ | ✅ |
| **Modify Priority & Category** | — | ✅ | ✅ |
| **Global Ticket Oversight (All Tickets)** | — | — | ✅ |
| **Assign / Reassign Tickets to Support Staff** | — | — | ✅ |
| **User & Staff Account Administration** | — | — | ✅ |
| **Operational Analytics & SLA Metrics** | — | Assigned Summary | Full Suite |

### System Highlights
- **Stateless JWT Authentication:** Access tokens paired with refresh tokens and a server-side revocation list for immediate token invalidation on logout.
- **Heartbeat Middleware:** Automatically records support staff's `last_active` timestamp on authenticated requests to measure online availability.
- **Analytics Engine:** SQL aggregations calculate average resolution times, category load distributions, high-priority ticket counts, and staffing workload.

---

## Architecture & Tech Stack

```mermaid
graph LR
    subgraph Client ["Client Layer (Frontend)"]
        React["React 19 SPA (Vite)"]
        Router["React Router v7"]
        UI["Tailwind CSS + Recharts"]
    end

    subgraph API ["Application Layer (Backend)"]
        FastAPI["FastAPI REST API (Uvicorn)"]
        Auth["JWT Auth + Passlib Bcrypt"]
        Middleware["Auth & Last-Active Middleware"]
    end

    subgraph Persistence ["Data & Storage Layer"]
        SQLAlchemy["SQLAlchemy 2.0 ORM"]
        Alembic["Alembic Migrations"]
        DB[("PostgreSQL / Supabase")]
        Storage["Local Disk / Cloud Storage"]
    end

    React -->|REST / JSON| FastAPI
    FastAPI --> Auth
    FastAPI --> Middleware
    FastAPI --> SQLAlchemy
    SQLAlchemy --> Alembic
    SQLAlchemy --> DB
    FastAPI --> Storage
```

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Server:** [Uvicorn](https://www.uvicorn.org/) (ASGI)
- **Database & ORM:** PostgreSQL, [SQLAlchemy 2.0](https://www.sqlalchemy.org/), [Alembic](https://alembic.sqlalchemy.org/)
- **Authentication & Security:** [python-jose](https://github.com/mpdavis/python-jose) (JWT), [Passlib](https://passlib.readthedocs.io/) (Bcrypt password hashing)
- **File Handling:** `python-multipart`, local disk storage (`uploads/`), with architecture for Google Cloud Storage.

### Frontend
- **Library:** [React 19](https://react.dev/)
- **Tooling & Build:** [Vite 6](https://vitejs.dev/)
- **Routing:** [React Router v7](https://reactrouter.com/)
- **Styling:** [Tailwind CSS 4](https://tailwindcss.com/)
- **Data Visualization:** [Recharts](https://recharts.org/)
- **Icons & Components:** `react-icons`, `antd`, `flowbite`
- **HTTP Client:** [Axios](https://axios-http.com/)

---

## Repository Structure

```text
ccodel_tickets/
├── backend/                     # FastAPI Application
│   ├── alembic/                 # Database migration scripts & history
│   │   └── versions/            # Version-controlled migration files
│   ├── api/
│   │   ├── core/                # Core configuration & settings
│   │   ├── db/                  # Engine setup, session pooling & Base
│   │   ├── utils/               # Auth helpers, file storage, user services
│   │   └── v1/
│   │       ├── models/          # SQLAlchemy ORM definitions
│   │       ├── routes/          # API route controllers (auth, tickets, users, analytics)
│   │       ├── schemas/         # Pydantic request/response schemas
│   │       └── services/        # Service-layer business logic
│   ├── main.py                  # FastAPI entry point & middleware stack
│   ├── alembic.ini              # Alembic environment config
│   ├── requirements.txt         # Python dependencies
│   └── .env.sample              # Backend environment template
│
├── frontend/                    # React SPA Application
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── assets/              # Logos and graphics
│   │   ├── components/          # Reusable UI components (Tables, Drawers, Navbars)
│   │   ├── hooks/               # Custom React hooks (role extraction, auth)
│   │   ├── pages/
│   │   │   ├── auth/            # Login and Register views
│   │   │   ├── student/         # Student portal views
│   │   │   ├── support/         # Support staff views
│   │   │   ├── admin/           # Admin views
│   │   │   └── __test__/        # Prototype dashboards & test components
│   │   ├── App.jsx              # Main routing definition
│   │   └── main.jsx             # React entry point
│   ├── package.json             # Node dependencies and scripts
│   ├── vite.config.js           # Vite build configuration
│   └── styles.css               # Global styles & Tailwind configuration
│
└── README.md                    # Repository documentation
```

---

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.10+**
- **Node.js 18+**
- **pnpm** (preferred for frontend) or `npm`
- **PostgreSQL** (local instance or cloud database such as Supabase / AWS RDS)

---

### 1. Clone the Repository

```bash
git clone https://github.com/Bluel0la/ccodel_tickets.git
cd ccodel_tickets
```

---

### 2. Backend Setup (FastAPI)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment files:**
   Copy the sample files to create your active configuration:
   ```bash
   cp .env.sample .env
   cp .env.config.sample .env.config
   ```
   *Edit `.env` and `.env.config` with your database credentials and secret key (see [Environment Variables](#environment-variables)).*

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the API server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The interactive API documentation will be available at:
   - **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 3. Frontend Setup (React + Vite)

1. **Open a new terminal and navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies using pnpm:**
   ```bash
   pnpm install
   ```

3. **Start the development server:**
   ```bash
   pnpm run dev
   ```
   Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## Environment Variables

### Backend Configuration (`backend/.env` & `backend/.env.config`)

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `DB_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/ccodel_db` |
| `SECRET_KEY` | Secret key used to sign JWT tokens | `generate-a-secure-random-key` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Lifetime of the access token in minutes | `60` |
| `APP_URL` | Base frontend URL for CORS | `http://localhost:5173` |
| `MAIL_USERNAME` | SMTP email username | `support@institution.edu` |
| `MAIL_PASSWORD` | SMTP password / app key | `your_smtp_password` |
| `MAIL_SERVER` | SMTP server host | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account key for GCS | `gcs-key.json` |

---

## API Overview

The backend mounts all versioned endpoints under `/api/v1`:

### 🔐 Authentication (`/api/v1/auth`)
- `POST /register` — Register a new student, support officer, or admin.
- `POST /login` — Authenticate and receive `access_token` and `refresh_token`.
- `GET /me` — Retrieve the authenticated user's profile.
- `POST /logout` — Revoke active token.
- `POST /refresh-token` — Issue a new access token using a valid refresh token.

### 🎫 Tickets (`/api/v1/tickets`)
- `POST /` — Create a ticket (accepts `multipart/form-data` for JSON payload and attachments).
- `GET /submitted` — List tickets submitted by the calling student.
- `GET /assigned` — List tickets assigned to the calling support officer.
- `GET /all` — List all system tickets (Admin only).
- `GET /{ticket_id}` — Get ticket details (role-protected).
- `PUT /{ticket_id}` — Update ticket status, priority, or description based on role permissions.
- `PUT /{ticket_id}/assign` — Assign a ticket to a support staff member (Admin only).
- `PUT /{ticket_id}/cancel` — Cancel a ticket (Ticket creator or Admin).
- `GET /{ticket_id}/attachments` — List files attached to a ticket.
- `POST /{ticket_id}/comments` — Add a message to the ticket conversation.
- `GET /{ticket_id}/comments` — Retrieve all conversation messages for a ticket.

### 📊 Analytics (`/api/v1/analytics`)
- `GET /analytics/tickets-summary` — Role-scoped ticket counts (open, in progress, resolved).
- `GET /analytics/average-resolution-time` — Average time from ticket creation to resolution.
- `GET /analytics/tickets-by-category` — Ticket distribution grouped by category.
- `GET /analytics/urgent-tickets` — Count of unresolved high-priority tickets.
- `GET /analytics/active-support-staff` — Support personnel active within the last 10 minutes.
- `GET /analytics/total-students` — Total registered student population (Admin only).

### 👥 User Administration (`/api/v1/users`)
- `GET /` — List all registered users (Admin only).
- `GET /{user_id}` — Retrieve specific user details.
- `PUT /{user_id}` — Modify user details or role.
- `DELETE /{user_id}` — Soft delete a user account.
- `PUT /change-password` — Change password for the current user.

---

## Current Project Status & Roadmap

> For a complete, granular architectural report, see [project_status_report.md](file:///C:/Users/JOSEPH%20AYODELE/.gemini/antigravity-ide/brain/637447d3-ac27-4ae8-bf59-9ae1a0752a0e/project_status_report.md).

### Completed ✅
- Full relational database models and 11 Alembic migrations.
- Complete authentication lifecycle (registration, login, refresh, logout revocation).
- Ticket submission, assignment, role-based editing, cancellation, and comments.
- Operational analytics queries and heartbeat middleware.
- Student ticket creation with file upload and ticket tracking views in React.

### Planned & Next Steps 🚧
- [ ] **Frontend Routing Unification:** Consolidate prototype components from `src/pages/__test__/` into production route paths (`/student/*`, `/support/*`, `/admin/*`) with a `<ProtectedRoute />` guard.
- [ ] **Live Dashboard Data:** Connect Recharts dashboards in Admin and Support views to the `/api/v1/analytics/` endpoints.
- [ ] **Chat UI:** Embed the comments/messaging thread directly into `TicketDrawer` for interactive discussions.
- [ ] **Cloud Storage Integration:** Connect Google Cloud Storage (`file_storage.py`) or Cloudinary for reliable remote file persistence.
- [ ] **Ticket History Auditing:** Trigger `TicketHistory` log entries automatically on ticket status, priority, and assignment updates.
- [ ] **Email Alerts:** Implement asynchronous email dispatch (`fastapi-mail`) for ticket status transitions and assignments.
- [ ] **Test Coverage:** Build integration test suites under `backend/tests/`.

---

## License

This project is licensed under the terms of the [Apache License 2.0](LICENSE).
