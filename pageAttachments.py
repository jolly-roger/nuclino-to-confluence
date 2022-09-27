import requests
import os

import logger

def upload_attachment(contentId, attachment, username, password, confluenceApiUrl, workFolder):
  logger.LOGGER.info('Uploading attchment...')
  logger.LOGGER.info('Content id: %s', contentId)

  url = '%s/rest/api/content/%s/child/attachment' % (confluenceApiUrl, contentId)

  session = requests.Session()
  session.auth = (username, password)
  session.headers.update({'X-Atlassian-Token': 'no-check'})
  filePath = os.path.join(workFolder, attachment)

  response = session.post(url, files={ 
    'file': open(filePath, 'rb')
  })
  try:
    response.raise_for_status()
  except requests.exceptions.HTTPError as excpt:
    logger.LOGGER.error("error: %s - %s", excpt, response.content)
    exit(1)

  if response.status_code == 200:
    logger.LOGGER.info('Attachment uploaded')
    return

  logger.LOGGER.error('Could not upload attachment')
  logger.LOGGER.info('Response Status:\n%s', response.status_code)
  logger.LOGGER.info('Response Body:\n%s', response.content)
  sys.exit(1)

def upload_attachments(contentId, attachments, username, password, confluenceApiUrl, workFolder):
  for attachment in attachments:
    upload_attachment(contentId, attachment, username, password, confluenceApiUrl, workFolder)
