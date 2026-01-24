# Alembic Migration Tests

This directory contains integration tests for Alembic database migrations.

## Test Coverage

The test suite (`test_alembic_migrations.py`) covers:

### Migration Functionality
- ✅ **test_migrations_run_successfully** - All migrations apply without errors
- ✅ **test_can_downgrade_migrations** - Migrations can be rolled back
- ✅ **test_migration_from_clean_database** - Migrations work on empty database
- ✅ **test_idempotent_migrations** - Running migrations multiple times is safe
- ✅ **test_check_for_pending_migrations** - Detects migration status correctly

### Schema Validation
- ✅ **test_current_head_matches_models** - Database schema matches SQLAlchemy models
- ✅ **test_holdings_daily_table_schema** - holdings_daily table has correct columns and constraints
- ✅ **test_positions_table_schema** - positions table has correct columns and indexes
- ✅ **test_instruments_table_schema** - instruments table has correct columns

### Data Integrity
- ✅ **test_can_insert_data_after_migration** - Data insertion works after migration
- ✅ **test_unique_constraint_holdings_daily** - Unique constraint on (symbol, as_of_date) is enforced

### Migration Quality
- ✅ **test_migration_history_is_linear** - No branched migrations
- ✅ **test_all_migrations_have_docstrings** - All migrations are documented

## Running Tests

### Locally (if you have dependencies installed)
```bash
pytest tests/test_alembic_migrations.py -v
```

### In Docker
```bash
# Run all Alembic tests
docker-compose run --rm api pytest tests/test_alembic_migrations.py -v

# Run specific test
docker-compose run --rm api pytest tests/test_alembic_migrations.py::test_holdings_daily_table_schema -v

# Run with coverage
docker-compose run --rm api pytest tests/test_alembic_migrations.py --cov=app.db --cov-report=term-missing
```

### During Build
The Dockerfile already runs all tests (including these) during the build process.

## Test Database

Tests use an in-memory SQLite database, so they:
- Run fast
- Don't affect your real database
- Don't require PostgreSQL to be running
- Are completely isolated

## Adding New Migration Tests

When creating a new migration, consider adding tests for:

1. **Schema changes** - Verify columns, types, constraints
2. **Data migrations** - Test data transformation logic
3. **Indexes** - Ensure performance indexes are created
4. **Constraints** - Verify foreign keys, unique constraints, etc.

Example:
```python
def test_new_table_schema(alembic_config, test_engine):
    """Test that new_table has the correct schema."""
    command.upgrade(alembic_config, "head")
    
    inspector = inspect(test_engine)
    columns = {col["name"]: col for col in inspector.get_columns("new_table")}
    
    assert "id" in columns
    assert "new_column" in columns
```

## Troubleshooting

### SQLite vs PostgreSQL Differences
Some PostgreSQL-specific features may not work in SQLite tests:
- Array columns
- JSON/JSONB columns
- PostgreSQL-specific constraints

For these, you may need to:
1. Mock the functionality
2. Use conditional logic based on database type
3. Run additional tests against a real PostgreSQL database

### Migration Not Found
If you get "Can't locate revision identified by 'xyz'":
- Ensure migration files are in `alembic/versions/`
- Check that `script_location` in `alembic.ini` is correct
- Verify the migration file naming follows Alembic conventions
