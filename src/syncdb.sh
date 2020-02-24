#!/bin/bash


LOCAL_DB="mongodb://localhost/companies"

# Load REMOTE_DB env variable
source .env

echo "Importing from local db: $LOCAL_DB"
echo "\t ...to remote: $REMOTE_DB"

mongodump --uri=$LOCAL_DB
mongorestore --uri=$REMOTE_DB