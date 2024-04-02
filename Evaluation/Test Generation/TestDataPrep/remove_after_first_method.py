import sys
from tree_sitter import Language, Parser

# Load tree-sitter-java grammar
Language.build_library(
    'build/my-languages.so',
    ['tree-sitter-java']
)
JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

def find_first_test_method(tree):
    for node in tree.root_node.children:
        if node.type == 'class_declaration':
            for child in node.children[-1].children:
                if child.type == 'method_declaration':
                    if any(x.type == 'modifiers' and "@Test" in str(x.text) for x in child.children):
                        return child
                    if any(x.type == 'identifier' and "test" in str(x.text).lower() for x in child.children):
                        return child
    return None

def extract_code_and_first_test(java_code):
    tree = parser.parse(bytes(java_code, 'utf8'))
    first_test_method = find_first_test_method(tree)
    if first_test_method:
        start_line = first_test_method.end_point[0] + 1

        code_lines = java_code.split('\n')
        return '\n'.join(code_lines[:start_line])
    return ""

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        java_code = f.read()

    code_first_test = extract_code_and_first_test(java_code)
    with open(output_file, 'w') as f:
        f.write(code_first_test+"\n")