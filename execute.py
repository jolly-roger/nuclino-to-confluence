import sys
import requests
import json
import urllib
import os

import logger
import page
import pageAttachments

def get_space_base_id(username, password, confluenceApiUrl, spaceKey):
  """
  Gets the base page's ID of the Confluence Space

  :return:string
  """
  session = requests.Session()
  session.auth = (username, password)
  session.headers.update({'Content-Type': 'application/json'})

  url = '%s/rest/api/space/%s' % (confluenceApiUrl, spaceKey)

  response = session.get(url)
  try:
    response.raise_for_status()
  except requests.exceptions.HTTPError as excpt:
    logger.LOGGER.error("error: %s - %s", excpt, response.content)
    exit(1)

  if response.status_code == 200:
    data = response.json()
    return data[u'_expandable'][u'homepage'][len("/rest/api/content/"):]
  logger.LOGGER.error('Cannot get Space main page ID')
  logger.LOGGER.error('Status: %s', response.status_code)
  logger.LOGGER.error('Response: %s', response.content)
  sys.exit(1)

def is_child(child, ancestor, username, password, confluenceApiUrl):
  """
  Determine if a page ID is a direct child of an ancestor ID

  :return:bool
  """
  session = requests.Session()
  session.auth = (username, password)
  session.headers.update({'Content-Type': 'application/json'})

  url = '%s/rest/api/content/%s?expand=ancestors' % (confluenceApiUrl, child)

  response = session.get(url)
  try:
    response.raise_for_status()
  except requests.exceptions.HTTPError as excpt:
    logger.LOGGER.error("error: %s - %s", excpt, response.content)
    return ""

  if response.status_code == 200:
    data = response.json()
    if data[u'ancestors'][len(data[u'ancestors'])-1][u'id'] == child:
      return True
  return False

def get_page_id(title, ancestor, username, password, confluenceApiUrl, spaceKey):
  """
  Gets the a page's ID by title

  :return:string
  """
  session = requests.Session()
  session.auth = (username, password)
  session.headers.update({'Content-Type': 'application/json'})

  url = '%s/rest/api/content?title=%s&spaceKey=%s' % (confluenceApiUrl, urllib.parse.quote_plus(title), spaceKey)

  response = session.get(url)
  try:
    response.raise_for_status()
  except requests.exceptions.HTTPError as excpt:
    logger.LOGGER.error("error: %s - %s", excpt, response.content)
    return ""

  if response.status_code == 200:
    data = response.json()
    for res in data[u'results']:
      if is_child(res[u'id'], ancestor, username, password, confluenceApiUrl):
        return res[u'id']
    return ""

  logger.LOGGER.error('Cannot get page ID by title: %s', title)
  logger.LOGGER.error('Status: %s', response.status_code)
  logger.LOGGER.error('Response: %s', response.content)
  return ""

def create_page(title, body, ancestor, username, password, confluenceApiUrl, spaceKey):
  """
  Create a new page

  :param title: confluence page title
  :param body: confluence page content
  :param ancestor: confluence page ancestor
  :return:string
  """

  existing_id = get_page_id(title, ancestor, username, password, confluenceApiUrl, spaceKey)
  if existing_id:
    logger.LOGGER.info('Page already exists...')
    return existing_id

  logger.LOGGER.info('Creating page...')
  logger.LOGGER.info('Title: %s\nBody: %s\nAncestor: %s', title, body, ancestor)

  url = '%s/rest/api/content/' % confluenceApiUrl

  session = requests.Session()
  session.auth = (username, password)
  session.headers.update({'Content-Type': 'application/json'})

  ancestors = [{'type': 'page', 'id': ancestor}]

  new_page = {'type': 'page',
              'title': title,
              'space': {'key': spaceKey},
              'body': {
                  'storage': {
                      'value': body,
                      'representation': 'storage'
                  }
              },
              'ancestors': ancestors,
              }

  logger.LOGGER.info("data: %s", json.dumps(new_page))

  response = session.post(url, data=json.dumps(new_page))
  try:
    response.raise_for_status()
  except requests.exceptions.HTTPError as excpt:
    logger.LOGGER.error("error: %s - %s", excpt, response.content)
    exit(1)

  if response.status_code == 200:
    data = response.json()
    space_name = data[u'space'][u'name']
    page_id = data[u'id']
    link = '%s%s' % (confluenceApiUrl, data[u'_links'][u'webui'])

    logger.LOGGER.info('Page created in %s with ID: %s.', space_name, page_id)
    logger.LOGGER.info('URL: %s', link)
    return page_id

  logger.LOGGER.error('Could not create page.')
  logger.LOGGER.info('Response Status:\n%s', response.status_code)
  logger.LOGGER.info('Response Body:\n%s', response.content)
  sys.exit(1)

def execute_import(username, password, confluenceApiUrl, spaceKey, workFolder, planFolder):
  """
  Traverses the plan folder and creates Confluence pages accordingly

  :return:
  """

  confluence_pages = {}

  base_id = get_space_base_id(username, password, confluenceApiUrl, spaceKey)

  for paths, dirs, files in os.walk(planFolder):
    page_path = paths.split(planFolder)[1]
    elems = page_path.split("/")[1:]
    ancestor_id = confluence_pages["/" + "/".join(elems[:-1])]["page_id"] if len(elems) > 1 else base_id
    page_id = base_id
    if page_path:
      page_id = create_page(elems[len(elems) - 1], "", ancestor_id, username, password, confluenceApiUrl, spaceKey)
      confluence_pages[page_path] = {"page_id": page_id}
    for md_file in files:
      body, attachments = page.get_body(os.path.join(workFolder, md_file))
      file_name = md_file[:-12]
      page_id = create_page(file_name, body, page_id, username, password, confluenceApiUrl, spaceKey)
      pageAttachments.upload_attachments(page_id, attachments, username, password, confluenceApiUrl, workFolder)