if [ -f .env ]; then
  export $(echo $(cat .env | sed "s/#.*//g"| xargs) | envsubst)
fi

SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

rm -R -f ./migrations/versions/ &&
mkdir ./migrations/versions/ &&
if [ $DB_MANAGER == "postgresql" ]
  then
    psql -U $DB_USERNAME -c "DROP DATABASE "$DB_NAME";" || true && 
    psql -U $DB_USERNAME -c "CREATE DATABASE "$DB_NAME";" &&
    psql -U $DB_USERNAME -c "CREATE EXTENSION unaccent;" -d $DB_NAME
else
  mysql -u $DB_USERNAME -p -e "DROP DATABASE IF EXISTS "$DB_NAME";" || true && echo "DROP DATABASE" &&
  mysql -u $DB_USERNAME -p -e "CREATE DATABASE "$DB_NAME";" && echo "CREATE DATABASE"
fi
pipenv run migrate &&
pipenv run upgrade &&

if [ "$DB_MANAGER" == "postgresql" ]; then
  if psql -U $DB_USERNAME -d $DB_NAME -f "$SCRIPT_DIRECTORY/starwars_psql_data.sql"; then
    echo "DATA POPULATED"
  else
    echo "Failed to populate data"
    exit 1
  fi
else
  if mysql -u $DB_USERNAME -p $DB_NAME < "$SCRIPT_DIRECTORY/starwars_mysql_data.sql"; then
    echo "DATA POPULATED"
  else
    echo "Failed to populate data"
    exit 1
  fi
fi