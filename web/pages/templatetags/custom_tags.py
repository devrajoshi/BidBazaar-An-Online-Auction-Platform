from django import template
import json

register = template.Library()

@register.filter("json_dump")
def json_dump(bid):
    val = {}
    for key, value in vars(bid).items():
        val[key] = str(value)
    return json.dumps(val)
