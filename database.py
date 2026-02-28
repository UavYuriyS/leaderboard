from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from typing import Optional, AsyncGenerator
from config import settings
from db_models import Base


class Database:
    """SQLAlchemy database connection manager"""

    def __init__(self):
        self.engine: Optional[create_async_engine] = None
        self.async_session_maker: Optional[async_sessionmaker] = None

    async def connect(self):
        """Create database engine and session factory"""
        # Create async engine with asyncpg driver
        database_url = settings.database_url.replace('postgresql://', 'postgresql+asyncpg://')

        self.engine = create_async_engine(
            database_url,
            echo=False,  # Set to True to see SQL queries in console
            poolclass=NullPool,  # Or use default pool
        )

        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def disconnect(self):
        """Close database engine"""
        if self.engine:
            await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session"""
        async with self.async_session_maker() as session:
            yield session


# Global database instance
db = Database()
