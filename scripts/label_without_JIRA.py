###
### This script checks for labels having a JIRA tkt reference per format of JIRA-####

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
### retrieve changes in changeset
###
change_set = script_helper.get_changeset().getChanges()
labels = change_set.getLabels()
liquibase_logger.info("Labels are " + labels.toString())
   
###
### trigger for no label on changeset
###
if labels.isEmpty() == True:
    status = script_helper.get_status()
    status.fired = True
###
### Locate 'JIRA-' from in list
###
if "JIRA-" not in labels:
    status = script_helper.get_status()
    status.fired = True
    liquibase_status.message = script_helper.get_script_message()
    sys.exit(1)

###
### Default return code
###
False