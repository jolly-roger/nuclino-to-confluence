import codecs
import markdown

import macros
import comment
import code
import image
import refs

def get_body(file_path):
  """
  get the body of a markdown file as html

  :return:string
  """
  with codecs.open(file_path, 'r', 'utf-8') as mdfile:
    html = markdown.markdown(mdfile.read(), extensions=['markdown.extensions.tables', 'markdown.extensions.fenced_code'])
  html = macros.convert_info_macros(html)
  html = comment.convert_comment_block(html)
  html = code.convert_code_block(html)
  html, attachments = image.convert_img_block(html)
  html = refs.process_refs(html)

  return (html, attachments)