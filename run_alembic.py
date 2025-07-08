import os
import sys
from alembic.config import Config
from alembic import command
from config import settings

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

def run_migrations():
    sync_url = settings.database_url.replace("+asyncpg", "")
    
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)

    command.revision(
        config=alembic_cfg,
        autogenerate=True,
        message="add vk_data to users"
    )
    
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()