import markdown
import random


def generate_api_key(length: int = 30) -> str:
    """ Generates an api key of a certain length. """

    output = ""
    symbols = list("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890")
    for _ in range(length):
        output += random.choice(symbols)

    return output


def generate_html(title: str, text: str) -> str:
    """ Generates formatted Html markup from Markdown markup. """

    meta_style_sheet = "<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='/styles/doc_style.css') }}\">"
    meta_title = f"<title>Quof - {title}</title>"
    header_href = "href=\"{{ url_for('main.index') }}\""
    header_logo = "<img class=\"header-logo\" width=\"48\" height=\"48\" " \
                  "src=\"{{ url_for('static', filename='/images/logo.png') }}\" alt=\"logo\" />"

    output = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        {meta_style_sheet}
        {meta_title}
    </head>
    <body>
        <header>
            <a {header_href}>
                {header_logo}
            </a>
        </header>

        <form>
            <div class="container">
                {markdown.markdown(text)}
            </div>
        </form>
    </body>
</html>
"""

    return output
