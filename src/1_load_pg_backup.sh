# Clear existing Postgres data by deleting the cache/Postgres directory
rm -rf cache/postgres
mkdir -p cache/postgres

# Launch a clean Postgres container using Docker Compose up
# Remove the volume mount from your docker-compose file to make this simpler
docker-compose up -d

# Provide the Postgres password
export PGPASSWORD=mypassword

# Restore the database from the backup file
pg_restore --verbose --clean --no-acl --no-owner \
-h localhost \
-p 54321 \
-U myuser \
-d mydatabase \
./downloads/QSARToolbox46May2023/Database/Toolboxv4v23.backup
