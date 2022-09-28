import re

def convert_br_block(html):
  """
  Fix html br

  :param html: string
  :return: modified html string
  """
  brs = re.findall(r'<br.*?>', html, re.DOTALL)
  if brs:
    for br in brs:
      html = html.replace(br, '<br/>')

  return html
