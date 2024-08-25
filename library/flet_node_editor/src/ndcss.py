
def ndcss_parser(path):
    with open(path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    css_rules = {}
    selector = None
    lines = css_content.splitlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('/*') or line.endswith('*/'):
            continue
        if line.endswith('{'):
            selector = line[:-1].strip()
            css_rules[selector] = {}
        elif line.endswith('}'):
            selector = None
        elif selector:
            property_name, property_value = line.split(':', 1)
            css_rules[selector][property_name.strip()] = property_value.strip(';').strip()

    return css_rules
