# PostgreSQL Pets Application

Required Python packages:
```
pip install flask psycopg2-binary python-dotenv
```

## Setup Steps

1. Create database and user:
```bash
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
psql -U postgres
CREATE DATABASE pets_db;
CREATE USER pets_app WITH PASSWORD 'petsAppPassword456!';
\c pets_db
GRANT ALL PRIVILEGES ON DATABASE pets_db TO pets_app;
\q

psql -U postgres -d pets_db -f setup_database.sql
psql -U postgres -d pets_db -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO pets_app;"
psql -U postgres -d pets_db -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO pets_app;"
```

2. Set environment variables:
```bash
export POSTGRES_HOST=localhost
export POSTGRES_DB=pets_db
export POSTGRES_USER=pets_app
export POSTGRES_PASSWORD=petsAppPassword456!
```

Or create .env file from .env.example:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run the application:
```bash
python app.py
```

4. Visit: http://localhost:5000

## Testing

Run database tests:
```bash
# Create test database first
psql -U postgres -c "CREATE DATABASE test_pets_db;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE test_pets_db TO pets_app;"

# Run tests
python database.py
```

## Security Notes

- Never commit .env file to version control
- Use strong passwords in production
- Enable SSL/TLS for production deployments
- Follow principle of least privilege for user permissions
- Regular backups with pg_dump

## See README.md for complete documentation
