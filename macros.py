import re

def upper_chars(string, indices):
  """
  Make characters uppercase in string

  :param string: string to modify
  :param indices: character indice to change to uppercase
  :return: uppercased string
  """
  upper_string = "".join(c.upper() if i in indices else c for i, c in enumerate(string))
  return upper_string

def strip_type(tag, tagtype):
  """
  Strips Note or Warning tags from html in various formats

  :param tag: tag name
  :param tagtype: tag type
  :return: modified tag
  """
  tag = re.sub(r'%s:\s' % tagtype, '', tag.strip(), re.IGNORECASE)
  tag = re.sub(r'%s\s:\s' % tagtype, '', tag.strip(), re.IGNORECASE)
  tag = re.sub(r'<.*?>%s:\s<.*?>' % tagtype, '', tag, re.IGNORECASE)
  tag = re.sub(r'<.*?>%s\s:\s<.*?>' % tagtype, '', tag, re.IGNORECASE)
  tag = re.sub(r'<(em|strong)>%s:<.*?>\s' % tagtype, '', tag, re.IGNORECASE)
  tag = re.sub(r'<(em|strong)>%s\s:<.*?>\s' % tagtype, '', tag, re.IGNORECASE)
  tag = re.sub(r'<(em|strong)>%s<.*?>:\s' % tagtype, '', tag, re.IGNORECASE)
  tag = re.sub(r'<(em|strong)>%s\s<.*?>:\s' % tagtype, '', tag, re.IGNORECASE)
  string_start = re.search('<.*?>', tag)
  tag = upper_chars(tag, [string_start.end()])
  return tag

def convert_doctoc(html):
  """
  Convert doctoc to confluence macro

  :param html: html string
  :return: modified html string
  """

  toc_tag = '''<p>
  <ac:structured-macro ac:name="toc">
    <ac:parameter ac:name="printable">true</ac:parameter>
    <ac:parameter ac:name="style">disc</ac:parameter>
    <ac:parameter ac:name="maxLevel">7</ac:parameter>
    <ac:parameter ac:name="minLevel">1</ac:parameter>
    <ac:parameter ac:name="type">list</ac:parameter>
    <ac:parameter ac:name="outline">clear</ac:parameter>
    <ac:parameter ac:name="include">.*</ac:parameter>
  </ac:structured-macro>
  </p>'''

  html = re.sub(r'\<\!\-\- START doctoc.*END doctoc \-\-\>', toc_tag, html, flags=re.DOTALL)

  return html

def convert_info_macros(html):
  """
  Converts html for info, note or warning macros

  :param html: html string
  :return: modified html string
  """
  info_tag = '<p><ac:structured-macro ac:name="info"><ac:rich-text-body><p>'
  note_tag = info_tag.replace('info', 'note')
  warning_tag = info_tag.replace('info', 'warning')
  close_tag = '</p></ac:rich-text-body></ac:structured-macro></p>'

  # Custom tags converted into macros
  html = html.replace('<p>~?', info_tag).replace('?~</p>', close_tag)
  html = html.replace('<p>~!', note_tag).replace('!~</p>', close_tag)
  html = html.replace('<p>~%', warning_tag).replace('%~</p>', close_tag)

  # Convert block quotes into macros
  quotes = re.findall('<blockquote>(.*?)</blockquote>', html, re.DOTALL)
  if quotes:
    for quote in quotes:
      note = re.search('^<.*>Note', quote.strip(), re.IGNORECASE)
      warning = re.search('^<.*>Warning', quote.strip(), re.IGNORECASE)

      if note:
        clean_tag = strip_type(quote, 'Note')
        macro_tag = clean_tag.replace('<p>', note_tag).replace('</p>', close_tag).strip()
      elif warning:
        clean_tag = strip_type(quote, 'Warning')
        macro_tag = clean_tag.replace('<p>', warning_tag).replace('</p>', close_tag).strip()
      else:
        macro_tag = quote.replace('<p>', info_tag).replace('</p>', close_tag).strip()

      html = html.replace('<blockquote>%s</blockquote>' % quote, macro_tag)

  # Convert doctoc to toc confluence macro
  html = convert_doctoc(html)

  return html