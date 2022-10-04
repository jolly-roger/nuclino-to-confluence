import re

def convert_tag_block(html):
  """
  Replace specific tags with text

  :param html: string
  :return: modified html string
  """
  html = html.replace('<script>', '&lt;script&gt;')
  html = html.replace('</script>', '&lt;/script&gt;')
  html = html.replace('<anything>', '&lt;anything&gt;')
  html = html.replace('<foo...>', '&lt;foo...&gt;')
  html = html.replace('<column is not shown>', '&lt;column is not shown&gt;')
  html = html.replace('<pod ip>', '&lt;pod ip&gt;')
  html = html.replace('<cluster name>', '&lt;cluster name&gt;')
  html = html.replace('<cluster>', '&lt;cluster&gt;')
  html = html.replace('<accountID>', '&lt;accountID&gt;')
  html = html.replace('<package\_name>', '&lt;package\_name&gt;')
  html = html.replace('<branch-name>', '&lt;branch-name&gt;')
  html = html.replace('<id>', '&lt;id&gt;')
  html = html.replace('<streamName>', '&lt;streamName&gt;')
  html = html.replace('<recordLimit>', '&lt;recordLimit&gt;')
  html = html.replace('<sleepSeconds>', '&lt;sleepSeconds&gt;')
  html = html.replace('<channel key>', '&lt;channel key&gt;')
  html = html.replace('<action>', '&lt;action&gt;')
  html = html.replace('<found/not found>', '&lt;found/not found&gt;')
  html = html.replace('<strategy>', '&lt;strategy&gt;')
  html = html.replace('<Supplement autogenerate setting>', '&lt;Supplement autogenerate setting&gt;')
  html = html.replace('<provided/not provided>', '&lt;provided/not provided&gt;')
  html = html.replace('<result>', '&lt;result&gt;')
  html = html.replace('<branch name>', '&lt;branch name&gt;')
  html = html.replace('<ingress', '&lt;ingress&gt;')

  return html
