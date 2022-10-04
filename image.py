import re

def convert_img_block(html):
  """
  Convert html images to Confluence attachments

  :param html: string
  :return: modified html string
  """
  images = re.findall(r'<img.*?/>', html, re.DOTALL)
  attachments = []
  if images:
    for image in images:
      conf_ml = '<ac:image>'

      data = re.search('alt="(.*)".*? src="(.*)"', image)
      alt = data.group(1)
      src = data.group(2)

      if alt:
        attachments.append(src)    
        conf_ml = conf_ml + '<ri:attachment ri:filename="' + alt + '" />'
        conf_ml = conf_ml + '</ac:image>'

        html = html.replace(image, conf_ml)        

  return (html, attachments)
