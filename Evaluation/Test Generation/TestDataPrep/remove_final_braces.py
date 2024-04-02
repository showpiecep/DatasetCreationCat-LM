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

def find_class_method(tree):
    for node in tree.root_node.children:
        if node.type == 'class_declaration':
            return node
    return None


def extract_code_before_braces(java_code):
    tree = parser.parse(bytes(java_code, 'utf8'))
    class_node = find_class_method(tree)
    if class_node:
        end_line = class_node.end_point[0]
        code_lines = java_code.split('\n')
        return '\n'.join(code_lines[:end_line])
    return ""

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        java_code = f.read()

    code_before_braces = extract_code_before_braces(java_code)
    with open(output_file, 'w') as f:
        f.write(code_before_braces+"\n")