import asyncio
from alembic.config import Config
from alembic import command
from config import settings

async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, autogenerate=True, message="Initial migration")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    asyncio.run(run_migrations())