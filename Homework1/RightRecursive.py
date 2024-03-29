###Build a tree node###
class Node(object):
    def __init__(self, type, val=None, left=None, right=None):
        self.type=type
        self.val=val
        self.left=left
        self.right=right

###Detect incorrect syntax###
class IncorrectSyntax(Exception):
    def __init__(self, msg, tok):
        self.msg=msg
        self.tok=tok


###Functions to construct non-terminals###
def parse_factor(toks):
    if len(toks)==0:
        raise IncorrectSyntax("Expected factor, but input is empty", '')

    tok = toks.pop(0)
    if tok.isspace():       # white space; continue to next token
        return parse_factor(toks)
    elif tok.isalpha():     # identifier
        return Node(type="id", val=tok)
    elif tok.isdigit():     # number
        while len(toks)>0 and toks[0].isdigit():
            tok = list(tok)         # change token into mutable type
            tok.append(toks.pop(0)) # make token multiple-digit number
        return Node(type="num", val=str(int(''.join(tok))))   # save token value into a string type
    else:               # invalid character, such as operator
        raise IncorrectSyntax("Expected identifier or number", tok)

def parse_term(toks):
    factor = parse_factor(toks)
    if len(toks)>0:
        tok = toks[0]               # one lookahead
        if tok.isspace():           # white space; continue to next token
            toks.pop(0)
            tok = toks[0]

        if tok=='*' or tok=='/':
            tok = toks.pop(0)
            return Node(type='op', val=tok, left=factor, right=parse_term(toks))
        elif tok=='+' or tok=='-':  # continue parsing expression
            return factor
        else:
            raise IncorrectSyntax("Expected operation after factor", tok)
    else:
        return factor

def parse_expr(toks):
    term = parse_term(toks)
    if len(toks)>0:
        tok = toks[0]               # one lookahead
        if tok.isspace():           # white space; continue to next token
            toks.pop(0)
            tok = toks[0]

        if tok=='+' or tok=='-':  # one lookahead
            tok = toks.pop(0)
            return Node(type='op', val=tok, left=term, right=parse_expr(toks))
    else:
        return term
##########################################

'''Helper function to replace white space with a single space in input string line
                    & change into mutable data type(list)'''
def tokenize(str_line):
    return list(' '.join(str_line.strip().split()))

'''Parse the given input string line'''
def parser(str_line):
    toks = tokenize(str_line)
    if len(toks)==0:
        raise IncorrectSyntax("There is only white space on this line", toks)
    return parse_expr(toks)


'''Helper function to concatenate strings'''
def merge(str1, str2, str3):
    return str1+str2+str3

'''Express the parsed tree in pre_order syntax string'''
def pre_order(root):
    if root == None:
        return ''
    return merge(root.val, pre_order(root.left), pre_order(root.right))

def main():
    # Read input file
    file_in = open("input.txt", "r")
    file_out = open("output.txt", "w")

    # Iterate lines in file
    for line in file_in:
        try:
            expr_result = pre_order(parser(line))
            file_out.write(expr_result+'\n')
        except IncorrectSyntax as e:
            file_out.write("incorrect syntax" + '\n')

    file_in.close()
    file_out.close()

if __name__ == "__main__":
    main()