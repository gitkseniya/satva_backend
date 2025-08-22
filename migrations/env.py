from __future__ import with_statement
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

config = context.config

# Safely configure logging only if the INI actually has logging sections
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name, disable_existing_loggers=False)
    except Exception:
        # No [formatters]/[handlers]/[loggers] present – continue without logging setup
        pass

from app import app as flask_app, db  # noqa: E402

target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    # Prefer the Flask app's configured DB URI if present
    if flask_app and flask_app.config.get("SQLALCHEMY_DATABASE_URI"):
        url = flask_app.config["SQLALCHEMY_DATABASE_URI"]

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    # Prefer the Flask app's configured DB URI if present
    if flask_app and flask_app.config.get("SQLALCHEMY_DATABASE_URI"):
        configuration["sqlalchemy.url"] = flask_app.config["SQLALCHEMY_DATABASE_URI"]

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
