from src.helpers.validation_exception import ValidationException
from src.helpers.code import surround_code, require_solidity_code


def group_by_section_and_join(items):
    sections = {}
    for section, parsed_item in items:
        if section not in sections:
            sections[section] = parsed_item["text"]
            continue
        sections[section] += f"\n{parsed_item['text']}"
    return sections


def extract_function(items):
    description_items = filter(lambda item: item[0] == "description", items)
    func_items = list(filter(lambda item: item[1]["is_code"], description_items))

    if len(func_items) == 0:
        raise ValidationException()

    return func_items[0][1]["text"]


def validate_sections(sections):
    mandatory_sections = ["description", "recommendation"]

    for section in mandatory_sections:
        if section not in sections:
            raise ValidationException()

    return sections


next_section = None


# "name", "severity", "function", "description", "recommendation", "impact"
# Idea: skip title by returning None, and keep returning "next_section" until a
# new title is encountered
def get_section(text):
    global next_section

    if text.startswith("Summary"):
        next_section = "description"
        return None

    if text.startswith("Vulnerability Details"):
        next_section = "description"
        return None

    if text.startswith("Proof of Concept") or text.startswith("PoC"):
        next_section = "description"
        return None

    if text.startswith("Impact"):
        next_section = "impact"
        return None

    if text.startswith("Recommendations"):
        next_section = "recommendation"
        return None

    # IGNORED ONES
    if text.startswith("Severity"):
        next_section = None
        return None

    if text.startswith("Relevant GitHub Links"):
        next_section = None
        return None

    if text.startswith("Tools Used"):
        next_section = None
        return None

    return next_section


def parse_markdown_elements(elements):
    require_solidity_code(elements)

    parsed_items = [surround_code(element) for element in elements]
    sections = [get_section(item["text"]) for item in parsed_items]

    items = list(filter(lambda item: item[0] is not None, zip(sections, parsed_items)))

    func = extract_function(items)
    sections = group_by_section_and_join(items)
    sections["function"] = func

    global next_section
    next_section = None

    return validate_sections(sections)
