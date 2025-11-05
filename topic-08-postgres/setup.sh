#!/bin/bash
# Setup script for PostgreSQL pets database

echo "PostgreSQL Pets Database Setup"
echo "==============================="
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "ERROR: PostgreSQL is not installed."
    echo ""
    echo "Install PostgreSQL:"
    echo "  macOS:   brew install postgresql@15"
    echo "  Linux:   sudo apt install postgresql postgresql-contrib"
    exit 1
fi

echo "✓ PostgreSQL is installed"
echo ""

# Database configuration
DB_NAME="pets_db"
APP_USER="pets_app"
APP_PASSWORD="petsAppPassword456!"

echo "Creating database and user..."
echo ""

# Create database (as postgres superuser)
psql -U postgres -c "CREATE DATABASE ${DB_NAME};" 2>/dev/null || echo "Database ${DB_NAME} may already exist"

# Create application user
psql -U postgres -c "CREATE USER ${APP_USER} WITH PASSWORD '${APP_PASSWORD}';" 2>/dev/null || echo "User ${APP_USER} may already exist"

# Grant privileges
psql -U postgres -c "GRANT CONNECT ON DATABASE ${DB_NAME} TO ${APP_USER};"

echo ""
echo "Loading schema and data..."

# Load schema
psql -U postgres -d ${DB_NAME} -f setup_database.sql

# Grant permissions to application user
psql -U postgres -d ${DB_NAME} <<EOF
GRANT USAGE ON SCHEMA public TO ${APP_USER};
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ${APP_USER};
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${APP_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO ${APP_USER};

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT USAGE, SELECT ON SEQUENCES TO ${APP_USER};
EOF

echo ""
echo "✓ Setup complete!"
echo ""
echo "Test the connection:"
echo "  psql -U ${APP_USER} -d ${DB_NAME} -h localhost"
echo ""
echo "Run the Flask app:"
echo "  export POSTGRES_PASSWORD='${APP_PASSWORD}'"
echo "  python app.py"
