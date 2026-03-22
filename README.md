# Task Management System - FastAPI Backend

A complete, production-ready FastAPI backend for managing tasks with full CRUD operations, filtering, and validation.

## Features

✅ **Complete CRUD Operations**
- Create, Read, Update, Delete tasks
- Mark tasks as completed/pending
- Filter tasks by status

✅ **Database Integration**
- SQLAlchemy ORM with SQLite
- Automatic timestamps (created_at, updated_at)
- Database migrations support ready

✅ **Validation & Error Handling**
- Pydantic schema validation
- Title validation (cannot be empty)
- Comprehensive error messages
- Proper HTTP status codes

✅ **Best Practices**
- Modular code structure
- Dependency injection for database sessions
- Proper separation of concerns (models, schemas, CRUD, database)
- Type hints for better IDE support
- Comprehensive docstrings and comments
- CORS middleware enabled

✅ **API Documentation**
- Auto-generated Swagger UI (OpenAPI)
- Interactive API testing
- ReDoc alternative documentation

## Project Structure

```
Task_Manager/
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration and session management
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic schemas for validation
├── crud.py              # Create, Read, Update, Delete operations
├── requirements.txt     # Python dependencies
├── task_manager.db      # SQLite database (auto-created on first run)
└── README.md           # This file
```

## Installation

### 1. Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

### Option 1: Using Uvicorn Command (Recommended)

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Parameters:**
- `--reload`: Auto-reload on code changes (development only)
- `--host 127.0.0.1`: Bind to localhost
- `--port 8000`: Server port

### Option 2: Using Python Directly

```bash
python main.py
```

### Expected Output

```
============================================================
Task Management System API
============================================================
Starting server on http://127.0.0.1:8000
API Documentation: http://127.0.0.1:8000/docs (Swagger UI)
Alternative Docs: http://127.0.0.1:8000/redoc (ReDoc)
============================================================
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Started server thread [12345]
```

## API Endpoints

### Health & Info

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and documentation links |
| GET | `/health` | Health check endpoint |

### Task Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | Get all tasks with statistics |
| GET | `/tasks/{task_id}` | Get a specific task by ID |
| PUT | `/tasks/{task_id}` | Update a task |
| PATCH | `/tasks/{task_id}/complete` | Mark task as completed |
| PATCH | `/tasks/{task_id}/pending` | Mark task as pending |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Filtering

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/filter/completed` | Get all completed tasks |
| GET | `/tasks/filter/pending` | Get all pending tasks |

### Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stats` | Get task statistics |

## Usage Examples

### 1. Create a Task

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the API"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the API",
  "completed": false,
  "created_at": "2026-03-22T10:30:00+00:00",
  "updated_at": "2026-03-22T10:30:00+00:00"
}
```

### 2. Get All Tasks

```bash
curl "http://127.0.0.1:8000/tasks"
```

**Response:**
```json
{
  "total": 1,
  "completed_count": 0,
  "pending_count": 1,
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive documentation for the API",
      "completed": false,
      "created_at": "2026-03-22T10:30:00+00:00",
      "updated_at": "2026-03-22T10:30:00+00:00"
    }
  ]
}
```

### 3. Get a Specific Task

```bash
curl "http://127.0.0.1:8000/tasks/1"
```

### 4. Mark Task as Completed

```bash
curl -X PATCH "http://127.0.0.1:8000/tasks/1/complete"
```

### 5. Update a Task

```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "description": "Updated description"
  }'
```

### 6. Delete a Task

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```

### 7. Get Statistics

```bash
curl "http://127.0.0.1:8000/stats"
```

**Response:**
```json
{
  "total": 3,
  "completed": 1,
  "pending": 2,
  "completion_percentage": 33.33
}
```

## Interactive API Documentation

Once the server is running, you can access the interactive API documentation:

1. **Swagger UI (Recommended)**: http://127.0.0.1:8000/docs
   - Try out endpoints directly
   - See request/response examples
   - View all available endpoints

2. **ReDoc**: http://127.0.0.1:8000/redoc
   - Alternative documentation style
   - Great for reference

## Data Validation

### Title Validation
- **Required**: Yes
- **Type**: String
- **Min Length**: 1 character
- **Max Length**: 255 characters
- **Error**: "Field required" if not provided

### Description Validation
- **Required**: No
- **Type**: String (optional)
- **Max Length**: 1000 characters

### Pagination Parameters
- **skip**: Non-negative integer (default: 0)
- **limit**: 1-100 (default: 100)

## Error Handling

### Task Not Found (404)
```json
{
  "detail": "Task with ID 999 not found",
  "status_code": 404
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Internal Server Error (500)
```json
{
  "detail": "Internal server error",
  "status_code": 500
}
```

## Database

### SQLite Database File
- **Location**: `task_manager.db` (created automatically in the project root)
- **Connection String**: `sqlite:///./task_manager.db`
- **Auto-created**: Yes (on first application run)

### Database Schema

**Tasks Table**
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Advanced Features

### Pagination
All list endpoints support pagination:
```bash
curl "http://127.0.0.1:8000/tasks?skip=0&limit=10"
```

### Task Statistics
Get insights into your tasks:
```bash
curl "http://127.0.0.1:8000/stats"
```

### Filtering
Filter tasks by completion status:
```bash
# Get completed tasks
curl "http://127.0.0.1:8000/tasks/filter/completed"

# Get pending tasks
curl "http://127.0.0.1:8000/tasks/filter/pending"
```

## Performance Considerations

- **Indexed Fields**: `id`, `title`, `completed`, `created_at`
- **Query Optimization**: Limited pagination (default 100 items per request)
- **Connection Pooling**: Configured for database efficiency
- **Session Management**: Automatic cleanup after each request

## Security Considerations

⚠️ **Development Mode Only**
The current configuration is suitable for development. For production:

1. **CORS**: Change `allow_origins=["*"]` to specific domains
2. **Database**: Use PostgreSQL or MySQL instead of SQLite
3. **Authentication**: Add JWT or OAuth2 authentication
4. **Rate Limiting**: Implement rate limiting
5. **Validation**: Add additional security checks
6. **Environment Variables**: Use `.env` file for sensitive configuration
7. **HTTPS**: Enable SSL/TLS in production

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --port 8001
```

### Database Locked Error
```bash
# Delete the database file to reset (development only)
del task_manager.db
# Then restart the server
```

### Module Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Issues
The application has CORS enabled. If you encounter CORS errors:
1. Check that the API URL matches the request origin
2. Verify CORS middleware configuration in `main.py`

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.104.1 | Web framework |
| uvicorn | 0.24.0 | ASGI server |
| sqlalchemy | 2.0.23 | ORM |
| pydantic | 2.5.0 | Data validation |
| python-multipart | 0.0.6 | Form data parsing |

## File Descriptions

### `main.py`
- FastAPI application setup
- Route definitions for all endpoints
- Error handling and middleware configuration
- Entry point for the application

### `database.py`
- SQLite database configuration
- Session factory for database connections
- Dependency injection function for sessions
- Database engine and base model setup

### `models.py`
- SQLAlchemy ORM models
- Task table definition with fields
- Column types and constraints
- Automatic timestamp management

### `schemas.py`
- Pydantic models for request/response validation
- Task creation schema (TaskCreate)
- Task update schema (TaskUpdate)
- Task response schema (TaskResponse)
- List response schema (TaskListResponse)

### `crud.py`
- CRUD operations implementation
- Database query methods
- Task creation, retrieval, update, deletion
- Statistical analysis queries

### `requirements.txt`
- Python package dependencies
- Version specifications

## Best Practices Implemented

✅ **Code Organization**
- Separate files for models, schemas, CRUD, and database
- Clear separation of concerns
- DRY (Don't Repeat Yourself) principle

✅ **Validation**
- Pydantic schema validation
- Type hints throughout
- Field constraints (min/max length)
- Required/optional fields clearly defined

✅ **Error Handling**
- Comprehensive error messages
- Proper HTTP status codes
- Custom exception handlers

✅ **Documentation**
- Comprehensive docstrings
- Inline comments
- Type hints for better IDE support
- Auto-generated API docs

✅ **Database**
- Connection pooling
- Automatic session cleanup
- Automatic timestamp management
- Proper index creation

✅ **API Design**
- RESTful principles
- Consistent naming conventions
- Versioning ready
- Pagination support

## Future Enhancements

- [ ] Add user authentication (JWT)
- [ ] Add task categories/tags
- [ ] Add due dates and reminders
- [ ] Add task priorities
- [ ] Add task comments
- [ ] Add task assignments/sharing
- [ ] Add rate limiting
- [ ] Add comprehensive logging
- [ ] Add database backup functionality
- [ ] Add WebSocket support for real-time updates
- [ ] Add task search functionality
- [ ] Add task sorting options
- [ ] Add batch operations
- [ ] Add API versioning

## Support & Documentation

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Uvicorn Documentation**: https://www.uvicorn.org/

## License

This project is provided as-is for educational and development purposes.

## Author

Created as a demonstration of FastAPI best practices and backend development patterns.

---

**Happy coding! 🚀**
