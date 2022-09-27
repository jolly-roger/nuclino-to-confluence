import re

def process_refs(html):
  """
  Process references

  :param html: html string
  :return: modified html string
  """
  refs = re.findall(r'\n(\[\^(\d)\].*)|<p>(\[\^(\d)\].*)', html)

  if refs:

    for ref in refs:
      if ref[0]:
          full_ref = ref[0].replace('</p>', '').replace('<p>', '')
          ref_id = ref[1]
      else:
          full_ref = ref[2]
          ref_id = ref[3]

      full_ref = full_ref.replace('</p>', '').replace('<p>', '')
      html = html.replace(full_ref, '')
      href = re.search('href="(.*?)"', full_ref).group(1)

      superscript = '<a id="test" href="%s"><sup>%s</sup></a>' % (href, ref_id)
      html = html.replace('[^%s]' % ref_id, superscript)

  return html
