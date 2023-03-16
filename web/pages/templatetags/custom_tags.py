from django import template
import json

register = template.Library()

@register.filter("json_dump")
def json_dump(bid):
    val = {}
    for key, value in vars(bid).items():
        val[key] = str(value)
    return json.dumps(val)

@register.filter(name='startswith')
def starts_with(string, prefix):
    if not isinstance(string, str):
        string = string.url.replace("/uploads/", "")
        print(string)
    if string.startswith(prefix):
        return True
    return False
