# Vote_APP_API 🚀

🌟 **FastAPI Backend for Vote App API**

This project provides a backend API using FastAPI for a voting application.

## Project Structure 📁

```
app/
├── database.py       # 🗃️ Database connection and setup
├── main.py           # 🚀 Main FastAPI application entry point
├── models.py         # 📊 SQLAlchemy database models
├── oauth2.py         # 🔐 OAuth2 authentication utilities
├── __pycache__/      # 📦 Compiled Python bytecode
│   ├── database.cpython-310.pyc
│   ├── main.cpython-310.pyc
│   └── models.cpython-310.pyc
├── routers/
│   ├── auth.py       # 🔑 Authentication routes
│   ├── post.py       # 📝 Post related routes
│   ├── user.py       # 👤 User management routes
│   └── vote.py       # 🗳️ Voting operations routes
├── schemas.py        # 📋 Pydantic schemas for data validation
├── secrets/          # 🔒 Directory for storing secrets (not included in repository)
└── utils.py          # 🛠️ Utility functions used across the application
```

## Installation 🛠️

### Prerequisites

- Python 3.10 or higher
- Virtual environment (optional but recommended)

### Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd Vote_APP_API
   ```

2. **Setup virtual environment (optional):**

   ```bash
   python -m venv myenv
   source myenv/bin/activate   # On Windows use `myenv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will start running at `http://localhost:8000`.

## Features ✨

- **Authentication:** OAuth2 with JWT tokens.
- **Endpoints:** CRUD operations for users, posts, and voting.
- **Schema Validation:** Data validation using Pydantic.

## Contributing 🤝

Contributions are welcome! Please fork the repository and submit pull requests.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

---
