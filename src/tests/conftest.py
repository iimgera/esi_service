import os

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ESI_URL", "https://esi.example.com")
os.environ.setdefault("ESI_CLIENT_ID", "test-client-id")
os.environ.setdefault("ESI_CLIENT_SECRET", "test-client-secret")
os.environ.setdefault("ESI_REDIRECT_URI", "http://localhost:8000/auth/callback")
