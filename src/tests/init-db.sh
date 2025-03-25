#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE "user_database";
    CREATE DATABASE "posts_database";
    GRANT ALL PRIVILEGES ON DATABASE user_database TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE posts_database TO $POSTGRES_USER;
EOSQL