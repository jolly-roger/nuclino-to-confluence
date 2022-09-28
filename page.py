import codecs
import markdown

import macros
import comment
import code
import image
import refs
import breakline
import table

def get_body(file_path):
  """
  get the body of a markdown file as html

  :return:string
  """
  mdfile = codecs.open(file_path, 'r', 'utf-8')
  mdtext = mdfile.read()
  html = markdown.markdown(mdtext, extensions=['extra'])
  html = macros.convert_info_macros(html)
  html = comment.convert_comment_block(html)
  html = code.convert_code_block(html)
  html, attachments = image.convert_img_block(html)
  html = refs.process_refs(html)
  html = breakline.convert_br_block(html)
  html = table.convert_table_block(html)

  return (html, attachments)