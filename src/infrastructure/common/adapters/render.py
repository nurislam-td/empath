from jinja2 import Environment, FileSystemLoader, select_autoescape

template_loader = FileSystemLoader(searchpath="template.path")
template_env = Environment(
    loader=template_loader,
    autoescape=select_autoescape("html", "xml"),
    lstrip_blocks=True,
    trim_blocks=True,
)


def render_template(template_name, **data):
    template = template_env.get_template(template_name)
    return template.render(**data)
