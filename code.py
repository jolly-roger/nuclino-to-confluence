import re

def convert_code_block(html):
  """
  Convert html code blocks to Confluence macros

  :param html: string
  :return: modified html string
  """
  code_blocks = re.findall(r'<pre><code.*?>.*?</code></pre>', html, re.DOTALL)
  if code_blocks:
    for tag in code_blocks:
      conf_ml = '<ac:structured-macro ac:name="code">'
      conf_ml = conf_ml + '<ac:parameter ac:name="theme">Midnight</ac:parameter>'
      conf_ml = conf_ml + '<ac:parameter ac:name="linenumbers">true</ac:parameter>'

      lang = re.search('code class="(.*)"', tag)
      if lang:
        lang = lang.group(1)
      else:
        lang = 'none'

      conf_ml = conf_ml + '<ac:parameter ac:name="language">' + lang + '</ac:parameter>'
      content = re.search(r'<pre><code.*?>(.*?)</code></pre>', tag, re.DOTALL).group(1)
      content = '<ac:plain-text-body><![CDATA[' + content + ']]></ac:plain-text-body>'
      conf_ml = conf_ml + content + '</ac:structured-macro>'
      conf_ml = conf_ml.replace('&lt;', '<').replace('&gt;', '>')
      conf_ml = conf_ml.replace('&quot;', '"').replace('&amp;', '&')

      html = html.replace(tag, conf_ml)

  return html
