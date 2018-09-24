###Build a tree node###
class Node(object):
    def __init__(self, type, val=None, child1=None, child2=None):
        self.type=type
        self.val=val
        self.ch1=child1
        self.ch2=child2

    def type(self):
        return self.type

    def value(self):
        return self.val

    def child1(self):
        return self.ch1

    def child2(self):
        return self.ch2

###Functions to construct non-terminals###
def parse_factor(str):
    tok = str.pop(0)
    if tok.isalpha():   # identifier
        return Node(type="id", val=tok)
    else:               # number
        while str[0].isdigit():
            tok.append(str.pop(0))  # make token multiple-digit number
        return Node(type="num", val=tok)

def parse_term_pr(str):
    if len(str)>0:
        tok = str[0]    # one lookahead
        if tok == '*' or tok == '/':
            tok = str.pop(0)
            return Node(type='op', val=tok, child1=parse_term(str))
    else:
        return Node(type='empty')

def parse_term(str):
    return Node(type="term", child1=parse_factor(str), child2=parse_term_pr(str))

def parse_expr_pr(str):
    if len(str)>0:
        tok = str[0]    # one lookahead
        if tok == '+' or tok == '-':
            tok = str.pop(0)
            return Node(type='op', val=tok, child1=parse_term(str), child2=parse_expr_pr)
    else:
        return Node(type='empty')

def parse_expr(str):
    return Node(type="expr", child1=parse_term(str), child2=parse_expr_pr(str))
##########################################

'''Helper function to eliminate white space in input string line
                    & change into mutable data type(list)'''
def tokenize(str):
    return list(str.rstrip().replace(" ",""))

'''Parse the given input string line'''
def parser(str):
    tokens = tokenize(str)
    if len(tokens)==0:
        return "incorrect syntax"
    return parse_expr(tokens)


'''Helper function to concatenate strings'''
def merge(str1, str2, str3):
    return str1+str2+str3

'''Express the parsed tree in pre_order syntax string'''
def pre_order(root):
    if root.type() in ["id", "num", "op"]:
        val = root.value()
    else:
        val = ''
    return merge(val, pre_order(root.child1()), pre_order(root.child2()))


def main():
    # Read input file
    file_in = open("input.txt", "r")
    file_out = open("output.txt", "w")

    # Iterate lines in file
    for line in file_in:
        expr_result = pre_order(parser(line))
        print(expr_result)
        file_out.write(expr_result)

    file_in.close()
    file_out.close()

if __name__ == "__main__":
    main()