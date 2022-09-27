#!/usr/bin/env python3
"""
# --------------------------------------------------------------------------------------------------
# Import a Nuclino Workspace to Confluence
# --------------------------------------------------------------------------------------------------
# This script can be run in two modes plan and execute:
# - The plan mode traverses an exported Nuclino Workspace's folder and creates the "plan" subfolder
# - The execute mode traverses the "plan" folder and creates Pages accordingly in Confluence
#   then uploads the files as subpages
# --------------------------------------------------------------------------------------------------
# Usage: import.py spacekey folder command
# --------------------------------------------------------------------------------------------------
"""

import sys
import os
import argparse
import logging

import plan
import execute
import logger

# ArgumentParser to parse arguments and options
PARSER = argparse.ArgumentParser()
PARSER.add_argument('spacekey',
                    help="Confluence Space key for the page. If omitted, will use user space.")
PARSER.add_argument("folder", help="Path to the exported Nuclino Workspace")
PARSER.add_argument("command", help="The import command: plan or execute")
PARSER.add_argument('-u', '--username', help='Confluence username if $CONFLUENCE_USERNAME not set.')
PARSER.add_argument('-p', '--password', help='Confluence password if $CONFLUENCE_PASSWORD not set.')
PARSER.add_argument('-o', '--orgname',
                    help='Confluence organisation if $CONFLUENCE_ORGNAME not set. '
                         'e.g. https://XXX.atlassian.net/wiki'
                         'If orgname contains a dot, considered as the fully qualified domain name.'
                         'e.g. https://XXX')
PARSER.add_argument('-l', '--loglevel', default='INFO',
                    help='Use this option to set the log verbosity.')

ARGS = PARSER.parse_args()

# Assign global variables
try:
    # Set log level
    logger.LOGGER.setLevel(getattr(logging, ARGS.loglevel.upper(), None))

    SPACE_KEY = ARGS.spacekey
    WORK_FOLDER = ARGS.folder
    IMPORT_COMMAND = ARGS.command
    USERNAME = os.getenv('CONFLUENCE_USERNAME', ARGS.username)
    PASSWORD = os.getenv('CONFLUENCE_PASSWORD', ARGS.password)
    ORGNAME = os.getenv('CONFLUENCE_ORGNAME', ARGS.orgname)


    if USERNAME is None:
        logger.LOGGER.error('Error: Username not specified by environment variable or option.')
        sys.exit(1)

    if PASSWORD is None:
        logger.LOGGER.error('Error: Password not specified by environment variable or option.')
        sys.exit(1)

    if not os.path.exists(WORK_FOLDER):
        logger.LOGGER.error('Error: Path: %s does not exist.', WORK_FOLDER)
        sys.exit(1)

    if not os.path.isdir(WORK_FOLDER):
        logger.LOGGER.error('Error: Path: %s is not a folder.', WORK_FOLDER)
        sys.exit(1)

    PLAN_FOLDER = os.path.join(WORK_FOLDER, "plan")

    if SPACE_KEY is None:
        SPACE_KEY = '~%s' % (USERNAME)

    if ORGNAME is not None:
        if ORGNAME.find('.') != -1:
            CONFLUENCE_API_URL = 'https://%s' % ORGNAME
        else:
            CONFLUENCE_API_URL = 'https://%s.atlassian.net/wiki' % ORGNAME
    else:
        logger.LOGGER.error('Error: Org Name not specified by environment variable or option.')
        sys.exit(1)

except Exception as err:
    logger.LOGGER.error('\n\nException caught:\n%s ', err)
    logger.LOGGER.error('\nFailed to process command line arguments. Exiting.')
    sys.exit(1)

def main():
    """
    Main program

    :return:
    """

    if IMPORT_COMMAND not in ["plan", "execute"]:
        logger.LOGGER.error('Error: Invalid command %s The command must be: plan or execute', IMPORT_COMMAND)
        sys.exit(1)

    if IMPORT_COMMAND == "plan":
        plan.plan_import(WORK_FOLDER, PLAN_FOLDER)
    else:
        execute.execute_import(USERNAME, PASSWORD, CONFLUENCE_API_URL, SPACE_KEY, WORK_FOLDER, PLAN_FOLDER)

    logger.LOGGER.info('Confluence Import %s completed successfully.', "Planning" if IMPORT_COMMAND == "plan" else "Execution")

if __name__ == "__main__":
    main()
