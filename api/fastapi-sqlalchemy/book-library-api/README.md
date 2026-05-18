# Alembic usage

## Database Migrations (Alembic)

### Setup (first time)
```bash
pip install alembic
alembic upgrade head
```

### After changing a model
```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

### Useful commands
```bash
alembic history       # show all migrations
alembic current       # show current migration
alembic downgrade -1  # roll back one step
```