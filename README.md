# ESI Service

FastAPI-based microservice for integrating with ESI (Electronic Signature Interface) authentication system. Provides OAuth2 authentication flow and user management capabilities.

## Features

- **OAuth2 Authentication**: PKCE-enabled authorization flow with ESI
- **User Management**: Automatic user creation and profile synchronization
- **Token Management**: Secure storage and management of access/refresh tokens
- **Async Operations**: Full async/await support with SQLAlchemy and PostgreSQL
- **Database Migrations**: Alembic-based schema versioning
- **API Documentation**: Auto-generated Swagger UI and ReDoc
- **CORS Support**: Configurable cross-origin resource sharing
- **Production Ready**: Environment-based configuration with Docker support

## Tech Stack

- **Framework**: FastAPI 0.109.1
- **Server**: Uvicorn with async support
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 1.4.41 (async)
- **Migrations**: Alembic 1.13.3
- **Validation**: Pydantic 2.10.6
- **HTTP Client**: httpx 0.27.1 (async)
- **Testing**: pytest 7.2.0
- **Python**: 3.10+

## Project Structure

```
esi-service/
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration scripts
│   └── env.py                    # Alembic configuration
├── src/
│   ├── apps/
│   │   └── esi/                  # ESI application module
│   │       ├── model.py          # Database models (EsiUser, EsiToken)
│   │       ├── router.py         # API endpoints
│   │       ├── schema.py         # Pydantic schemas
│   │       └── service.py        # Business logic
│   ├── core/
│   │   ├── config.py             # Application settings
│   │   └── security.py           # Security utilities
│   ├── database/
│   │   ├── base.py               # Base model class
│   │   └── session.py            # Database session management
│   ├── dependencies/
│   │   └── database.py           # FastAPI dependencies
│   ├── services/                 # Shared services
│   ├── tests/                    # Test suite
│   └── main.py                   # Application entry point
├── .env-example                  # Environment variables template
├── alembic.ini                   # Alembic configuration
├── Dockerfile                    # Docker image definition
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip or poetry

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/iimgera/esi_service.git
cd esi_service
```

2. **Create and activate virtual environment**

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

```bash
cp .env-example .env
```

Edit `.env` file with your settings:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/esi_service

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.com
IS_PRODUCTION=False

# ESI Configuration
ESI_URL=https://esi.example.com
ESI_CLIENT_ID=your-client-id
ESI_CLIENT_SECRET=your-client-secret
ESI_REDIRECT_URI=http://localhost:8000/auth/callback
```

5. **Create database**

```sql
CREATE DATABASE esi_service
WITH OWNER your_user
ENCODING 'UTF8'
LC_COLLATE = 'en_US.UTF-8'
LC_CTYPE = 'en_US.UTF-8';
```

6. **Run migrations**

```bash
alembic upgrade head
```

7. **Start the server**

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

#### `POST /api/v1/esi_login`

Authenticate user via ESI OAuth2 flow and retrieve user information.

**Request:**

```json
{
  "code": "authorization_code_from_esi",
  "code_verifier": "pkce_code_verifier"
}
```

**Response:**

```json
{
  "access_token": "esi_access_token",
  "esi_user_info": {
    "sub": "user_esi_id",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "family_name": "Doe",
    "given_name": "John",
    "organization_tin": "123456789012",
    "organization_name": "Example Corp",
    "position_name": "Developer",
    "pin": "12345678901",
    "citizenship": "KZ",
    "gender": "M",
    "birthdate": "1990-01-01",
    "phone_number": "+77001234567"
  },
  "esi_user_id": 1
}
```

**Error Responses:**

- `400 Bad Request`: Missing code or code_verifier
- `500 Internal Server Error`: ESI service error

## Database Models

### EsiUser

Stores user profile information from ESI.

**Fields:**
- `id`: Primary key
- `esi_id`: Unique ESI identifier
- `organization_tin`: Tax identification number
- `organization_name`: Organization name
- `position_name`: Job title
- `pin`: Personal identification number
- `citizenship`: Country code (ISO 3166-1 alpha-3)
- `family_name`, `given_name`, `middle_name`: Full name components
- `name`: Full name
- `gender`: Gender
- `birth_date`: Date of birth
- `email`: Email address
- `phone`: Phone number
- `created_at`, `updated_at`: Timestamps
- `is_deleted`, `deleted_at`: Soft delete fields

### EsiToken

Stores ESI access and refresh tokens.

**Fields:**
- `id`: Primary key
- `esi_user_id`: Foreign key to EsiUser
- `token_type`: Token type (e.g., "Bearer")
- `token_value`: Access token
- `expires_in`: Token expiration datetime
- `refresh_token`: Refresh token
- `created_at`, `updated_at`: Timestamps
- `is_deleted`, `deleted_at`: Soft delete fields

## Database Migrations

**Create a new migration:**

```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations:**

```bash
alembic upgrade head
```

**Rollback migration:**

```bash
alembic downgrade -1
```

**View migration history:**

```bash
alembic history --verbose
```

**Check current version:**

```bash
alembic current
```

## Docker Deployment

### Build image

```bash
docker build -t esi-service .
```

### Run container

```bash
docker run -d \
  --name esi-service \
  -p 8000:8000 \
  --env-file .env \
  esi-service
```

### Docker Compose (example)

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: esi_service
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  postgres_data:
```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

Run specific test file:

```bash
pytest src/tests/test_auth.py
```

## Development

### Code Style

This project follows PEP 8 guidelines. Format code with:

```bash
black src/
isort src/
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

## Security Considerations

- Store secrets in `.env` file (never commit to version control)
- Use strong `SECRET_KEY` in production
- Enable HTTPS in production
- Configure `ALLOWED_ORIGINS` to restrict CORS
- Set `IS_PRODUCTION=True` to disable API documentation in production
- Regularly rotate ESI client credentials
- Implement rate limiting for production deployments

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `SECRET_KEY` | JWT signing key | - | Yes |
| `ALGORITHM` | JWT algorithm | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 | No |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | - | Yes |
| `IS_PRODUCTION` | Production mode flag | False | No |
| `ESI_URL` | ESI service base URL | - | Yes |
| `ESI_CLIENT_ID` | ESI OAuth2 client ID | - | Yes |
| `ESI_CLIENT_SECRET` | ESI OAuth2 client secret | - | Yes |
| `ESI_REDIRECT_URI` | OAuth2 callback URL | - | Yes |

## Troubleshooting

### Database connection errors

- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database exists and user has permissions

### ESI authentication fails

- Verify ESI credentials in `.env`
- Check ESI service availability
- Ensure redirect URI matches ESI configuration

### Migration errors

- Check database connection
- Review migration files for conflicts
- Try `alembic downgrade -1` then `alembic upgrade head`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Contact: iimgera28062004@gmail.com

---

**Built with FastAPI** | **Powered by PostgreSQL** | **Deployed with Docker**
