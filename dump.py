global eop
    if eop:
        return None
    print(f'parsing: {element}')
    global token_popped
    if token_popped:
        get_new_token()
        print(f'new token is: {get_token()}: {get_token_type()}')
        token_popped = False
    diagram_node = Node(f'{diagram[0]}')

    if element[1] == 'T':
        if diagram[0] == 'EPSILON':
            diagram_node.children = [Node('epsilon')]
            return diagram_node
        if get_token() == element[0] or get_token_type() == element[0]:
            print(f'parsed {get_token()}')
            if get_token() == '$':
                diagram_node.name = '$'
                token_popped = True
                return diagram_node
            else:
                diagram_node.name = f'({get_token_type()}, {get_token()})'
                token_popped = True
                return diagram_node
        else:
            if get_token() == '$':
                update_syntax_errors(get_token_line(), 'Unexpected EOF', '')
                eop = True
                return None
            else:
                update_syntax_errors(get_token_line(), element[0], 'missing')
                return None
    else:

        children = []
        for sequence in td.diagram_tuples:
            if element[0] == sequence[0]:

                for route in sequence[1]:
                    if fafs.is_token_in_firsts(route[0][0], get_token()) or fafs.is_token_in_firsts(route[0][0],
                                                                                                    get_token_type()):
                        for edge in route:
                            new_node = parse_diagram(edge)
                            if new_node is not None:
                                children.append(new_node)

                        if children:
                            diagram_node.children = children
                            return diagram_node

                for route in sequence[1]:
                    if fafs.is_token_in_follows(element[0], get_token()) or fafs.is_token_in_follows(element[0],
                                                                                                     get_token_type()):
                        if fafs.is_token_in_firsts(diagram[0], 'EPSILON'):
                            if route[0][0] == 'EPSILON':
                                diagram_node.children = [Node('epsilon')]
                                return diagram_node

                for route in sequence[1]:
                    if fafs.is_token_in_firsts(route[0][0], 'EPSILON') and (
                            fafs.is_token_in_follows(route[0][0], get_token()) or fafs.is_token_in_follows(route[0][0],
                                                                                                           get_token_type())):
                        for edge in route:
                            new_node = parse_diagram(edge)
                            if new_node is not None:
                                children.append(new_node)
                        diagram_node.children = children
                        return diagram_node

                if fafs.is_token_in_follows(sequence[0], get_token()) or fafs.is_token_in_follows(sequence[0],
                                                                                                  get_token_type()):
                    update_syntax_errors(get_token_line(), sequence[0], 'missing')
                    return None

                else:
                    if get_token_type() == 'ID' or get_token_type() == 'NUM':
                        if get_token_type() == 'SYMBOL':
                            print('\n\n\nhi\n\n\n')
                        update_syntax_errors(get_token_line(), get_token_type(), 'illegal')
                        token_popped = True
                        return parse_diagram(diagram)
                    else:

                        update_syntax_errors(get_token_line(), get_token(), 'illegal')
                        token_popped = True
                        return parse_diagram(diagram)