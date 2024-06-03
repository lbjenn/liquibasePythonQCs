###
### This script checks for a validator when creating a new collection
###

###
### Script helper comes from jar
###
import sys
import script_helper

###
### Constants
###
NOSQL_DATABASES = ["MongoDB"]

###
### Retrieve log handler
### Ex. liquibase_logger.info(message)
###
liquibase_logger = script_helper.get_logger()

###
### Retrieve status handler
###
liquibase_status = script_helper.get_status()

###
### Check for Mongo
###
liquibase_database = script_helper.get_database()
product_name = str(liquibase_database.getDatabaseProductName())
if not product_name.casefold() in map(str.casefold, NOSQL_DATABASES):
    liquibase_logger.info(f"Database {product_name} ignored")
    liquibase_status.fired = False
    sys.exit(1)

###
### Retrieve all changes in changeset
###
changes = script_helper.get_changeset().getChanges()

###
### Loop through all changes
###
for change in changes:
    ###
    ### Retrieve sql as string
    ###
    sql = script_helper.generate_sql(change).casefold()
    ###
    ### Remove extra whitespace
    ###
    sql = " ".join(sql.split())
    ###
    ### Locate createCollection
    ###
    if "createcollection" in sql and not "validator:" in sql:
        liquibase_status.fired = True
        liquibase_status.message = script_helper.get_script_message()
        sys.exit(1)

###
### Default return code
###
False
