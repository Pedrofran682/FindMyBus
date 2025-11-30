# 🚌 FindMyBus: Where's My Bus? - Docker Environment

**FindMyBus** ("Cadê meu busão?") is an application that monitors and displays the **real-time location of buses** in the city of Rio de Janeiro. It uses the [DATA RIO Vehicle Position API](https://www.data.rio/documents/273e65607d5b4c1c81e05be3acb689ce/explore) to help the user find their bus and visualize its route on the map.

This guide outlines how to configure and run the **FindMyBus** application locally using **Docker**. The architecture consists of three main services: a **PostgreSQL** database for data persistence, a **Worker** for data processing and ingestion, and a **UI (Streamlit)** for the user interface.


## 🧐 Project Description

**FindMyBus** solves the problem of tracking urban buses.

  * **Data Source:** The system consumes real-time geolocation data from the **DATA RIO Vehicle Position API**.
  * **Functionality:** The user can search for a specific bus line.
  * **Visualization:** The application displays the location of active buses on the map and plots the **complete itinerary route** (in both directions) for that line, providing visual context to the user.

## 📋 Prerequisites

Ensure you have **Docker** and **Docker Compose** installed on your machine:

  * [Docker](https://docs.docker.com/get-docker/)
  * [Docker Compose](https://docs.docker.com/compose/install/)

## 🚀 How to Run the Project

Follow the steps below to initialize the development environment.

### 1\. Environment Variables Configuration

The project uses environment variables to manage database credentials and network configurations. You must create a `.env` file in the project root.

We provide a template in `dev.env`. Create a copy of this file:

```bash
# Linux / Mac
cp dev.env .env

# Windows (PowerShell)
Copy-Item dev.env .env
```

#### Understanding the `.env`

The `.env` file comes pre-configured for the Docker environment. Below is a description of each parameter:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `DB_HOST` | `postgres_db` | **Important:** The database service name in the Docker network. |
| `DB_PORT` | `5432` | Internal database port. |
| `POSTGRES_DB` | `postgres_findMyBus` | Name of the database to be created. |
| `POSTGRES_USER` | `super_user` | Admin user (Database owner). |
| `POSTGRES_PASSWORD`| `super_user_password`| Admin password. |
| `POSTGRES_WORKER_USER` | `worker` | User for the **Worker** service (Read/Write permissions). |
| `POSTGRES_WORKER_PASSWORD` | `worker_password` | Password for the Worker user. |
| `POSTGRES_UI_USER` | `ui` | User for the **Streamlit UI** (Read-only permissions). |
| `POSTGRES_UI_PASSWORD` | `ui_password` | Password for the UI user. |
| `SCHEMA_PUBIC` | `public` | Default database schema. |

### 2\. Docker Compose Configuration

The main orchestration file should be named `compose.yaml`. Use the provided `compose.dev.yaml` example as your base:

```bash
# Linux / Mac
cp compose.dev.yaml compose.yaml

# Windows (PowerShell)
Copy-Item compose.dev.yaml compose.yaml
```

### 3\. Running the Application

With the `.env` and `compose.yaml` files created, build the images and start the containers:

```bash
docker-compose up --build
```

This command will:

1.  Pull the **Postgres** image.
2.  Build the Python image (using multi-stage build optimization).
3.  Start the database and run initialization scripts (creating users and tables).
4.  Start the **Worker** (which begins populating the database with API data).
5.  Start the **UI** (**Streamlit**).


## 🌐 Accessing the Application

Once the logs indicate the services are running:

  * **Web Interface (Streamlit):** Access **http://localhost:8501**
  * **Database (External Access):** Connect via `localhost:5432` using a client like DBeaver or PgAdmin.
