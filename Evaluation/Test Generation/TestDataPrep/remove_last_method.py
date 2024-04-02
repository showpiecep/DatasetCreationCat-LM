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

def find_last_test_method(tree):
    last_test_method = None
    for node in tree.root_node.children:
        if node.type == 'class_declaration':
            for child in node.children[-1].children:
                if child.type == 'method_declaration':
                    if any(x.type == 'modifiers' and "@Test" in str(x.text) for x in child.children):
                        last_test_method = child
                    if any(x.type == 'identifier' and "test" in str(x.text).lower() for x in child.children):
                        last_test_method = child
    return last_test_method

def extract_code_before_last_test(java_code):
    tree = parser.parse(bytes(java_code, 'utf8'))
    last_test_method = find_last_test_method(tree)
    if last_test_method:
        print(last_test_method)
        start_line = last_test_method.start_point[0]

        code_lines = java_code.split('\n')
        return '\n'.join(code_lines[:start_line])
    return ""

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        java_code = f.read()

    code_before_last_test = extract_code_before_last_test(java_code)
    with open(output_file, 'w') as f:
        f.write(code_before_last_test+"\n")