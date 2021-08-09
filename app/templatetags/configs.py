from django import template
from app.models import Configs
register = template.Library()


@register.simple_tag
def get_config_flag(chave):
    return Configs.get_flag(chave)


@register.simple_tag
def get_config_value(chave):
    return Configs.get_valor(chave)