from django import template
import re

register = template.Library()

@register.filter
def is_farsi(text):
    return bool(re.search(r'[\u0600-\u06FF]', text or ""))
