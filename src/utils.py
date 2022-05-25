import jinja2
import pathlib

def write_html_file(contents, filename, destdir, subfolder=None):
    """ simple wrapper contents writes contents to files """

    if subfolder is not None:
        pathlib.Path(f"{destdir}{subfolder}").mkdir(parents=True, exist_ok=True)
        filename = f'{subfolder}/{filename}'
    with open(f'{destdir}{filename}', 'w', encoding="utf-8", errors="xmlcharrefreplace") as d:
        d.write(contents)