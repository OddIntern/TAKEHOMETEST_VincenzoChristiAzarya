# FLOW 
## A Simple Task Management App

Inspired by the Kanban system made for team collaboration. This platform features two interfaces (Kanban Board & Monthly Calendar), Team Management, Drag & Drop Tasks Cards, and a history tracking log for each task.

Full-stack app built with **Vue 3** for frontend, **Python Flask** for backend, and **PostgreSQL** for the database.

---

## Table of Contents


1.  [Key Features]
2.  [Technology Stack]
3.  [System Architecture]
4.  [Getting Started]
5.  [Project Structure]
6.  [User Flow]

---

## Key Features

### Core Productivity
* **Dual-View Interface:** Swap between a standard drag-and-drop Kanban Board and an interactive Monthly Calendar view.
* **Optimistic UI Updates:** Drag-and-drop actions reflect instantly on the screen while syncing with the server in the background, providing a native-app feel.
* **Smart Filtering:** Per-column filtering allows users to isolate tasks by tags (Feature, Bug, Design, Planned) without losing context.

### Team Collaboration
* **Isolated Workspaces:** Fully multi-tenant design. Each user account creates and manages its own isolated board instance.
* **Customizable Boards:** Users can rename their project boards, with titles persisted to the PostgreSQL database.
* **Team Management:** Dynamic addition of team members. Users can assign tasks to multiple collaborators, visualized via an overlapping avatar system.

### Data 
* **History Tracking Log:** Every action is tracked including: creation, edits, and status changes is recorded in a history log for every task.
* **Data Persistence:**  Session tokens and user preferences are stored in LocalStorage, while business data is secured in PostgreSQL.

---

## Technology Stack

### Frontend
* **Framework:** Vue 3 (Composition API)
* **State Management:** Pinia
* **Styling:** Tailwind CSS
* **Interaction:** VueDraggable (Sortable.js)
* **Icons:** Heroicons (SVG)

### Backend
* **Framework:** Python Flask
* **ORM:** SQLAlchemy
* **Serialization:** Marshmallow
* **Authentication:** JWT (JSON Web Tokens)
* **Database:** PostgreSQL (Production)

---

## System Architecture

The application follows a **Clean Architecture** approach to ensure scalability and maintainability.

### 1. Service Layer Pattern
Business logic is decoupled from HTTP routing. The API routes handle request/response formatting, while the underlying logic is managed by dedicated service functions and model methods. This allows for easy testing and feature expansion.

### 2. Optimistic Concurrency Control (Frontend)
To maximize performance, the frontend `taskStore` updates the local state immediately upon user interaction. It then dispatches the API request. If the server returns an error, the store rolls back the change, notifying the user. This ensures the interface remains responsive even on slower networks.

### 3. Hybrid State Persistence
* **Runtime State:** Managed by Pinia for fast reactivity.
* **Session State:** Managed by LocalStorage (Auth Tokens, Team Members) to survive page reloads.
* **Persistent State:** Managed by PostgreSQL for long-term data storage.

---

## Getting Started

Follow these instructions to set up the project locally for development.

### Prerequisites
* Node.js (v16+)
* Python (v3.8+)
* PostgreSQL (Must be installed and running)

### 1. Database Setup
Before running the app, make sure you have a PostgreSQL database named `taskdb`.

1.  Open your terminal or pgAdmin.
2.  Create the database:
    ```bash
    createdb taskdb
    # OR run this SQL: CREATE DATABASE taskdb;
    ```
3.  **Check Credentials:** The app defaults to user `postgres` and password `password`.
    * If your credentials differ, set the `DATABASE_URL` environment variable:
    * *Windows (PowerShell):* `$env:DATABASE_URL="postgresql://YOUR_USER:YOUR_PASS@localhost:5432/taskdb"`
    * *Mac/Linux:* `export DATABASE_URL="postgresql://YOUR_USER:YOUR_PASS@localhost:5432/taskdb"`

### 2. Backend Setup

Navigate to the backend directory and set up the Python environment.

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize the Database
# This script resets the DB and applies the correct schema
python force_init.py

# Start the Server
python run.py
```

The API will start running at http://127.0.0.1:5000.

### 3. Frontend Setup
Open a new terminal window and navigate to the frontend directory.


```bash
cd frontend/task-manager-ui

# Install Node dependencies
npm install

# Start the Development Server
npm run dev
```

The application will be accessible at http://localhost:5173.

### Project Structure
```bash
TaskManagement/
├── backend/
│   ├── app/
│   │   ├── models/       # Database Models (User, Task)
│   │   ├── routes/       # API Endpoints (Auth, Tasks)
│   │   ├── services/     # Business Logic
│   │   └── schemas.py    # Serialization & Validation
│   ├── run.py            # Application Entry Point
│   └── requirements.txt  # Python Dependencies
│
├── frontend/taskmanagementui
│   ├── src/
│   │   ├── components/   # Reusable UI Components (Modals, etc.)
│   │   ├── stores/       # Pinia State Stores
│   │   ├── views/        # Page Views (Board, Login)
│   │   └── assets/       # Static Assets & Global CSS
│   ├── index.html        # Entry HTML
│   └── vite.config.js    # Build Configuration
└── README.md             # Project Documentation
```

### User Flow

    Registration: Launch the app and click "Need an account? Register" to create your personal workspace.

    Board Management: Click the Pen icon next to the "Project Board" title to rename your workspace.

    Task Creation: Click the "+" icon in any column header.

    Team Members: Inside the Task Modal, click "+ Add People" to dynamically add new members to your team roster.

    Calendar View: Toggle between "Board" and "Calendar" in the top right to switch perspectives.
