
import jinja2
import pathlib
import datetime

from utils import write_html_file

if __name__ == '__main__':

    # datetimeid 
    dtts = datetime.datetime.today().timestamp()    

    # folders of relevance
    templates_dir   = './src/templates/'

    # load templates
    template_loader = jinja2.FileSystemLoader(searchpath=templates_dir)
    templateEnv     = jinja2.Environment(loader=template_loader)

    # get the right template
    tmplt = templateEnv.get_template('landing_page.html')

    payload = dict()
    payload['dtts'] = dtts

    write_html_file(tmplt.render(payload), 'index.html', './docs/', subfolder=None)