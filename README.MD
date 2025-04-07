# StarWars API

A powerful and easy-to-use StarWars API built with FastAPI, SQLAlchemy, Alembic, SQLAdmin, and more.

## Requirements

Before you begin, make sure you have the following tools installed:

- **Database**: PostgreSQL (Recommended), MySQL, or MariaDB
- **Git**
- **Python 3.12** (Using `pyenv` or `pyenv-win` is a recommended alternative)
- Compatible with **Linux** and **Windows** (Not tested on macOS)

## Project Setup

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### Step 2: Configure Environment Variables

In the project root directory, you will find a file called `.env.example`. Create a copy and rename it to `.env`:

```bash
cp .env.example .env
```

Your `.env` file should look like this:

```env
DB_USERNAME=your_database_username
DB_PASSWORD=your_database_password
DB_URL=your_database_url # localhost is mostly used
DB_PORT=your_database_port # 3306 for MySQL/MariaDB, 5432 for PostgreSQL
DB_NAME=your_database_name
DB_MANAGER=your_database_manager # mysql+mysqldb, mariadb+mariadbconnector, or postgresql

LIST_RESPONSE_LIMIT=10 # Recommended

JWT_SECRET_KEY=your_jwt_secret_key
# To generate a secret key, run: openssl rand -hex 32
```

This file contains your database connection details, list response limit, and the JWT secret key used for authentication.

### Step 3: Install Dependencies

Install all project dependencies using Pipenv:

```bash
pipenv install
pipenv shell
```

### Step 4: Initialize the Database

Depending on your operating system, run the appropriate command:

For **Linux**:

```bash
pipenv run reset_lin_db
```

For **Windows**:

```bash
pipenv run reset_win_db
```

If everything goes well, proceed to create an admin user:

```bash
pipenv run create_admin
```

Your database will now be populated with all the required data.

## Usage

To start the development server, run:

```bash
pipenv run start
```

## Features

- ✅ **Swagger Documentation** at `/docs` for easy exploration of the API.
- ✅ **Admin Panel** at `/admin` with authentication for secure management.
- ✅ Main route available at `/` for general access.

## Notes

- Ensure your database service is running and accessible before starting the API.
- Recommended to use PostgreSQL for better compatibility and performance.
- The project is tested on Linux and Windows environments.

---

Enjoy exploring the Star Wars universe with your API! 🚀
