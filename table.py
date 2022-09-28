import re

def convert_table_block(html):
  """
  Wrap ascii tables with pre tag

  :param html: string
  :return: modified html string
  """
  tables = re.findall(r'<p>\+-.*?-\+</p>', html, re.DOTALL)
  if tables:
    for table in tables:
      html = html.replace(table, table.replace('<p>', '<pre>').replace('</p>', '</pre>'))

  return html
