from dataclasses import dataclass

@dataclass
class ParseField:
    name: str
    desc: str
    field_type: str

FIELD_LINE_TEMPLATE = "{name} - {desc}: typescript type {field_type}"
def format_field_list(fl):
    formatted_list = [FIELD_LINE_TEMPLATE.format(name=e.name, desc=e.desc, field_type=e.field_type) for e in fl]
    return '\n'.join(formatted_list)
