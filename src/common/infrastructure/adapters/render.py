from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import get_settings

settings = get_settings().app

template_loader = FileSystemLoader(searchpath=settings.TEMPLATE_PATH)
template_env = Environment(
    loader=template_loader,
    autoescape=select_autoescape("html", "xml"),
    lstrip_blocks=True,
    trim_blocks=True,
)


def render_template(template_name: str, **data: Any) -> str:  # noqa: ANN401
    template = template_env.get_template(template_name)
    return template.render(**data)
