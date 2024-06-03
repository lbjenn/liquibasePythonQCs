###
### This script checks for the phrase "DELETE FROM" not followed by "WHERE".
###

###
### Script helper comes from jar
###
import sys
import script_helper

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
### Retrieve all changes in changeset
###
changes = script_helper.get_changeset().getChanges()

###
### Loop through all changes
###
for change in changes:
    ###
    ### Skip LoadData change types
    ### https://www.geeksforgeeks.org/class-getsimplename-method-in-java-with-examples/
    ###
    if "LoadDataChange" in change.getClass().getSimpleName():
        continue
    ###
    ### Split sql into a list of strings to remove whitespace
    ###
    sql_list = script_helper.generate_sql(change).casefold().split()
    ###
    ### Locate delete from in list
    ###
    if "delete" in sql_list and "from" in sql_list and not "where" in sql_list:
        liquibase_status.fired = True
        liquibase_status.message = script_helper.get_script_message()
        sys.exit(1)

###
### Default return code
###
False