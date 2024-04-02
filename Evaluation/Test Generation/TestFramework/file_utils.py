import javalang
import ast

class CountFunc(ast.NodeVisitor):
    func_count = 0
    def visit_FunctionDef(self, node):
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            pass
        else:
            self.func_count += 1

def __get_start_end_for_node(tree, node_to_find):
    start = None
    end = None
    for path, node in tree:
        if start is not None and node_to_find not in path:
            end = node.position
            return start, end
        if start is None and node == node_to_find:
            start = node.position
    return start, end


def __get_string(code_content, start, end):
    if start is None:
        return ""

    # positions are all offset by 1. e.g. first line -> lines[0], start.line = 1
    end_pos = None

    if end is not None:
        end_pos = end.line - 1

    lines = code_content.splitlines(True)
    string = "".join(lines[start.line:end_pos])
    string = lines[start.line - 1] + string

    # When the method is the last one, it will contain a additional brace
    if end is None:
        left = string.count("{")
        right = string.count("}")
        if right - left == 1:
            p = string.rfind("}")
            string = string[:p]

    return string

def filter_file_java(fn):
    file_content = open(fn).read()
    tree = javalang.parse.parse(file_content)
    num_non_trivial_methods = 0
    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        start, end = __get_start_end_for_node(tree, node)
        body_code = __get_string(file_content, start, end)
        if "{" in body_code and "}" in body_code:
            body_no_whitespace = body_code.split("{")[1].split("}")[0].strip()
            if len(body_no_whitespace) > 0:
                num_non_trivial_methods += 1
    return num_non_trivial_methods  


def filter_file_python(fn):
    p = ast.parse(open(fn).read())
    f = CountFunc()
    f.visit(p)
    return f.func_count