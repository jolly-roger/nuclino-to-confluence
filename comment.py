def convert_comment_block(html):
    """
    Convert markdown code bloc to Confluence hidden comment

    :param html: string
    :return: modified html string
    """
    open_tag = '<ac:placeholder>'
    close_tag = '</ac:placeholder>'

    html = html.replace('<!--', open_tag).replace('-->', close_tag)

    return html
