import jinja2
import pathlib

def write_html_file(contents, filename, destdir, subfolder=None):
    """ simple wrapper contents writes contents to files """

    if subfolder is not None:
        pathlib.Path(f"{destdir}{subfolder}").mkdir(parents=True, exist_ok=True)
        filename = f'{subfolder}/{filename}'
    with open(f'{destdir}{filename}', 'w', encoding="utf-8", errors="xmlcharrefreplace") as d:
        d.write(contents)

if __name__ == '__main__':

    # folders of relevance
    templates_dir   = './src/templates/'

    # load templates
    template_loader = jinja2.FileSystemLoader(searchpath=templates_dir)
    templateEnv = jinja2.Environment(loader=template_loader)

    # get the right template
    tmplt = templateEnv.get_template('friday.html')
    with open('./data/friday.log', 'r') as pwrlog:
        log_data = pwrlog.read().split('\n')
        log_data.reverse()

        payload = dict()
        payload['main_contents'] = '\n'.join(log_data)

    write_html_file(tmplt.render(payload), 'index.html', './docs/friday/', subfolder=None)