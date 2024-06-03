###
### This script checks for special characters in the names of columns
###

###
### Script helper comes from jar
###
import sys
import script_helper
import re

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
### Function to search for find any special characters
###
def find_special_characters(s):
    # Define a regular expression pattern to match special characters
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    
    # Find all special characters in the string
    special_characters = pattern.findall(s)
    
    return special_characters


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
    ### Search changesets for special characters
    ###
    if "create" in sql_list or "alter" in sql_list or "add" in sql_list:
        print (sql_list)
        test_special_chars = find_special_characters(" ".join(sql_list))
        length = len(test_special_chars)
        if length != 0:
            liquibase_status.fired = True
            liquibase_status.message = script_helper.get_script_message()
            sys.exit(1)

###
### Default return code
###
False