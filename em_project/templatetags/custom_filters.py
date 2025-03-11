from django import template

register = template.Library()


@register.filter
def currency(value):
    try:
        return f"{value:.2f} Р"
    except (ValueError, TypeError):
        return value
