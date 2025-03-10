###
### This script checks for uppercase table names during creation
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
    sql_list = script_helper.generate_sql(change).split()
    ###
    ### Locate create (or replace) table in list
    ###
    if "create" in map(str.casefold, sql_list) and "table" in map(str.casefold, sql_list):
        index_table = [token.lower() for token in sql_list].index("table")
        if index_table + 1 < len(sql_list):
            table_name = sql_list[index_table + 1]
            if not table_name.isupper():
                liquibase_status.fired = True
                liquibase_status.message = str(script_helper.get_script_message()).replace("__TABLE_NAME__", f"'{table_name}'", 1)
                sys.exit(1)

###
### Default return code
###
False