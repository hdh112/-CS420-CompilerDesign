###Build a tree node###
class Node(object):
    def __init__(self, type, val=None, child1=None, child2=None):
        self.type=type
        self.value=val
        self.child1=child1
        self.child2=child2

###Functions to construct non-terminals###
def parse_factor(tokens):
    tok = tokens.pop(0)
    if tok.isalpha():   # identifier
        return Node(type="id", val=tok)
    else:               # number
        while tokens[0].isdigit():
            tok = list(tok)             # change token into mutable type
            tok.append(tokens.pop(0))   # make token multiple-digit number
        return Node(type="num", val=''.join(tok))

def parse_term_pr(tokens):
    if len(tokens)>0:
        tok = tokens[0]    # one lookahead
        if tok == '*' or tok == '/':
            tok = tokens.pop(0)
            return Node(type='op', val=tok, child1=parse_term(tokens))
    else:
        return Node(type='empty')

def parse_term(tokens):
    return Node(type="term", child1=parse_factor(tokens), child2=parse_term_pr(tokens))

def parse_expr_pr(tokens):
    if len(tokens)>0:
        tok = tokens[0]    # one lookahead
        if tok == '+' or tok == '-':
            tok = tokens.pop(0)
            return Node(type='op', val=tok, child1=parse_term(tokens), child2=parse_expr_pr(tokens))
    else:
        return Node(type='empty')

def parse_expr(tokens):
    return Node(type="expr", child1=parse_term(tokens), child2=parse_expr_pr(tokens))
##########################################

'''Helper function to eliminate white space in input string line
                    & change into mutable data type(list)'''
def tokenize(str_line):
    return list(str_line.rstrip().replace(" ",""))

'''Parse the given input string line'''
def parser(str_line):
    tokens = tokenize(str_line)
    if len(tokens)==0:
        return "incorrect syntax"
    return parse_expr(tokens)


'''Helper function to concatenate strings'''
def merge(str1, str2, str3):
    return str1+str2+str3

'''Express the parsed tree in pre_order syntax string'''
def pre_order(root):
    try:
        if root.type in ["id", "num", "op"]:
            val = root.value
        else:
            val = ''
        return merge(val, pre_order(root.child1), pre_order(root.child2))
    except AttributeError:  # root is NoneType
        return ''


def main():
    # Read input file
    file_in = open("input.txt", "r")
    file_out = open("output.txt", "w")

    # Iterate lines in file
    for line in file_in:
        expr_result = pre_order(parser(line))
        print(expr_result)
        file_out.write(expr_result+'\n')

    file_in.close()
    file_out.close()

if __name__ == "__main__":
    main()