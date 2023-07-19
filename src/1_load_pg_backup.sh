export PGPASSWORD=mypassword
pg_restore --verbose --clean --no-acl --no-owner -h localhost -p 54321 -U myuser -d mydatabase ./downloads/QSARToolbox46May2023/Database/Toolboxv4v23.backup
