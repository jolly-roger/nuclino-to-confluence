import os
import sys
import re
from shutil import copy

import logger

LINK_REGEXP = r'^.* \[.*]\(<(.*)>\)'

def check_plan_requirements(workFolder, planFolder):
  """
  Check if the index.md file can be found under WORKING_FOLDER
  Check if a previous plan was made
  Create the plan folder
  :return:
  """
  index_file = os.path.join(workFolder, "index.md")

  if not os.path.isfile(index_file):
    logger.LOGGER.error('Error: The index file of the Workspace cannot be found at %s', index_file)
    sys.exit(1)

  logger.LOGGER.info('Workspace Index file found %s', index_file)

  if os.path.isdir(planFolder):
    logger.LOGGER.error('Error: Previous plan detected under %s Remove the plan folder, and run the script again', planFolder)
    sys.exit(1)

  logger.LOGGER.info("Creating plan folder...")
  os.makedirs(planFolder)

def is_index_file(file_path):
  """
  Check if file_path is an Index file

  :return:boolean
  """
  pattern = re.compile(LINK_REGEXP)
  try:
    with open(file_path) as index_file:
      for line in index_file:
        if not pattern.match(line):
          return False
  except Exception as err:
    logger.LOGGER.error('\n\nFailed to open file\n%s ', err)
    sys.exit(1)
  return True

def get_subfolder_name(file_name):
  """
  Removes the .md extension and replaces spaces with _ in file_name and returns it

  :return:string
  """
  if file_name.endswith('.md'):
      file_name = file_name[:-12]
  file_name = file_name.replace(" ", "_")
  return file_name

def process_index(file_path, file_name, workFolder, planFolder):
  """
  Process an index file by creating a subfolder for it (except for the root index.md)
  Then iterate over its entryes and either copy them to the folder created (the root plan folder in case of index.md)
  or recursivly call process_index on them if they are index files themselves

  :return:
  """
  logger.LOGGER.info('Processing Index file %s ...', file_name)
  if file_path:
    logger.LOGGER.info('Creating subfolder %s', file_path)
    os.makedirs(os.path.join(planFolder, file_path))
  try:
    with open(os.path.join(workFolder, file_name)) as index_file:
      for line in index_file:
        md_file = os.path.join(workFolder, re.search(LINK_REGEXP, line).group(1))
        if not os.path.isfile(md_file):
          escaped_md_file = md_file.replace("\\", "")
          if os.path.isfile(escaped_md_file):
            md_file = escaped_md_file
          else:
            logger.LOGGER.error('Error: Cannot find markdown file %s', md_file)
            sys.exit(1)
        logger.LOGGER.info('Markdown file found %s', md_file)
        if is_index_file(md_file):
          process_index(
            os.path.join(file_path, get_subfolder_name(os.path.basename(md_file))),
            os.path.basename(md_file),
            workFolder,
            planFolder)
        else:
          dest = os.path.join(planFolder, file_path)
          logger.LOGGER.info('Copying %s to %s', md_file, dest)
          copy(md_file, dest)
  except Exception as err:
    logger.LOGGER.error('\n\nFailed to open file\n%s ', err)
    sys.exit(1)

def plan_import(workFolder, planFolder):
  """
  Create plan folder and populate it with the markdown files

  :return:
  """
  check_plan_requirements(workFolder, planFolder)
  process_index("", "index.md", workFolder, planFolder)