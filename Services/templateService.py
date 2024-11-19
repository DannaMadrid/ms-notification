import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')))

def load_html_template(template_name):
    try:
        return env.get_template(template_name)
    except Exception:
        return None
