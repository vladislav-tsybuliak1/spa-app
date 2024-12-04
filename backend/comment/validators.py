from django.core.exceptions import ValidationError
from lxml import html


ALLOWED_TAGS = {
    "a": ["href", "title"],
    "code": [],
    "i": [],
    "strong": []
}

def validate_comment_text(value: str) -> str:
    parsed = html.fromstring(value)

    for element in parsed.iter():
        if element.tag not in ALLOWED_TAGS:
            raise ValidationError(f"Tag <{element.tag}> is not allowed.")
        for attribute in element.attrib.keys():
            if attribute not in ALLOWED_TAGS[element.tag]:
                raise ValidationError(f"Attribute {attribute} not allowed in <{element.tag}> tag.")

    valid_html = html.tostring(parsed, encoding="unicode")
    return valid_html
