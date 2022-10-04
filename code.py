import re

def convert_code_block(html):
  """
  Convert html code blocks to Confluence macros

  :param html: string
  :return: modified html string
  """
  code_blocks = re.findall(r'```.*?```', html, re.DOTALL)
  if code_blocks:
    for code_block in code_blocks:
      code = re.search(r'```(.*?)```', code_block)
      if code:
        code = code.group(1)
      else:
        code = ''

      html = '<pre>' + code + '</pre>'

  return html
