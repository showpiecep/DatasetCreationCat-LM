from python_graphs import program_graph
from collections import defaultdict


def get_python_program_graph(filename):
    """ Get the python program graph."""
    with open(filename, errors='ignore') as f_in:
        file_content = f_in.read()

    graph = program_graph.get_program_graph(file_content)
    #print(graph.dump_tree())
    return graph, file_content



def get_all_method_defs_from_graph(graph, file_content):
    """ Extract all method definitions along with the span and the method bodies from the graph."""
    func_def_nodes = graph.get_ast_nodes_of_type('FunctionDef')
    method_defs = defaultdict(dict)
    file_content = file_content.split('\n')
    first_func_lineno = []
    for func_def_node in func_def_nodes:
        start_lineno = []
        end_lineno = []
        start_lineno.append(func_def_node.ast_node.lineno)
        end_lineno.append(func_def_node.ast_node.end_lineno)
        func_def_value = next(graph.children(func_def_node)).ast_value
        #print('func_def_value',func_def_value)
        children = list(graph.children(func_def_node))[3]
        for child in list(graph.children(children)):
            #child = list(graph.children(children))[0]
            #print(child.ast_node)
            #print(child.ast_node.lineno)
            #print(child.ast_node.end_lineno)
            #print(child.ast_value)
            start_lineno.append(child.ast_node.lineno)
            end_lineno.append(child.ast_node.end_lineno)
        class_value = get_class_name(graph, func_def_node)
        #print('start_lineno', start_lineno)
        #print('end_lineno', end_lineno)
        func_start_lineno = min(start_lineno)
        func_end_lineno = max(end_lineno)
        first_func_lineno.append(func_start_lineno)
        func_body = file_content[func_start_lineno-1:func_end_lineno]
        method_defs[class_value + func_def_value]['lineno'] = str(func_start_lineno) + '-' + str(func_end_lineno)
        method_defs[class_value + func_def_value]['body'] = '\n'.join(func_body)
    return method_defs









def get_class_name(graph, node):
    """ Helper: Get the enclosing class name(s)."""
    class_value = ''
    while graph.parent(node):
        node = graph.parent(node)
        if node.ast_type == 'ClassDef':
            class_value += next(graph.children(node)).ast_value + '.'
    return class_value

def resolve_object_type(method_calls, object_class_map):
    """ Helper: Resolve the type of objects."""
    resolved_method_calls = []
    for method_call in method_calls:
        if '.' in method_call and method_call.split('.')[0] in object_class_map.keys(): # obj.func()
            resolved_method_calls.append(object_class_map[method_call.split('.')[0]] + '.' + method_call.split('.')[1])
        elif method_call in object_class_map.keys(): # obj()
            resolved_method_calls.append(object_class_map[method_call])
        else:
            resolved_method_calls.append(method_call) # func()
    return resolved_method_calls


def get_all_class_names(graph):
    """ Get the names of all classes defined in the file."""
    code_classes = []
    class_def_nodes = graph.get_ast_nodes_of_type('ClassDef')
    for node in class_def_nodes:
        code_classes.append(next(graph.children(node)).ast_value)
    return code_classes


def get_all_method_calls_from_graph(graph, code_classes):
    """ Helper: Extract all the method calls made inside each function."""
    func_def_nodes = graph.get_ast_nodes_of_type('FunctionDef')
    method_calls_maps = defaultdict(list)
    for func_def_node in func_def_nodes:
        func_def_value = next(graph.children(func_def_node)).ast_value
        class_value = get_class_name(graph, func_def_node)
        func_graph = graph.copy_subgraph(func_def_node)
        call_nodes = func_graph.get_ast_nodes_of_type('Call')
        method_calls = []
        object_class_map = {}

        for call_node in call_nodes:
            method_call = ''
            call_child = next(func_graph.children(call_node))
            # method call of the form object.method()
            if call_child.ast_type == 'Attribute':
                object = ''
                method = ''
                for child_node in func_graph.children(call_child):
                    if child_node.ast_type == 'Name':
                        object = next(func_graph.children(child_node)).ast_value
                    elif child_node.ast_value:
                        method = child_node.ast_value
                if object != '' and method != '':
                    method_call = object + '.' + method

            # method call of the form method()
            elif call_child.ast_type == 'Name':
                method_call = next(graph.children(call_child)).ast_value

            # object creation, ie, object = Class()
            parent = func_graph.parent(call_node)
            if parent.ast_type == 'Assign':
                name_node = next(func_graph.children(parent))
                child_node = next(func_graph.children(name_node))
                return_node = next(func_graph.children(child_node)).ast_value
                if '.' not in method_call and method_call in code_classes:
                    object_class_map[return_node] = method_call
                    method_call = return_node + '.' + '__init__' # __init__ implicitly called during object creation

            if method_call != '':
                method_calls.append(method_call)
        method_calls_maps[class_value+func_def_value].extend(resolve_object_type(method_calls, object_class_map))
    return method_calls_maps


def get_changed_method_names(diff_lines, method_defs):
    """ Get the names of methods that changed using the diff line numbers."""
    changed_methods = []
    for method in method_defs.keys():
        span = method_defs[method]['lineno']
        start = int(span.split('-')[0])
        end = int(span.split('-')[1])
        for line in diff_lines:
            if line >= start and line <= end:
                changed_methods.append(method)
                break
    return changed_methods


def get_code_method_calls(graph, method_names, code_classes):
    """ Get the method calls for the given methods."""
    all_method_calls = get_all_method_calls_from_graph(graph, code_classes)
    method_calls = {method: all_method_calls[method] for method in method_names}
    return method_calls


def get_code_test_method_mapping_ast(test_changed_method_calls_before, test_changed_method_calls_after, code_changed_method_names):
    """Align the code and test methods based on the function calls in the test method.
    Code method must be present in both the before and after test file."""
    mapped = []
    if test_changed_method_calls_before and test_changed_method_calls_after and code_changed_method_names:
        for code_method in code_changed_method_names:
            if code_method in test_changed_method_calls_before and code_method in test_changed_method_calls_after:
                mapped.append(code_method)
    return mapped