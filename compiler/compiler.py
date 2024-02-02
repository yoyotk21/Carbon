from tokenizer import Token, tokenize, get_type
from vocab import *
from parse import parse

to_replace = {
    "=": "define",
    "true": "#true",
    "false": "#false",
    "else": "-else",
    "expects": "check-expect",
    "expects_random": "check-random",
    "satisfies": "check-satisfy",
    "struct": "define-struct",
    '&': 'make-posn',
    '@': 'list-ref'
}

def compile_1d(tokens):
   
    new_tokens = []
    for token in tokens:
        if token.value in to_replace:
            if get_type(to_replace[token.value]) != "None":
                new_tokens.append(Token(to_replace[token.value], get_type(to_replace[token.value])))
        elif token.type == "Name":
            token.value = token.value.replace("_", "-")
            new_tokens.append(token)
        else:
            new_tokens.append(token)
    
    tokens = new_tokens

    if len(tokens) == 1:
        return tokens

    func = tokens[0]
    args = tokens[1:]

    s = [Token('(', "Symbol"), func]

    for arg in args:
        s.append(arg)

    s.append(Token(')', "Symbol"))

    return s

def compiled_li(tokens):
    if type(tokens) != list:
        return compiled_li([tokens])
    if len(tokens) == 1 and type(tokens[0]) == list:
        return compiled_li(tokens[0])
    new_tokens = []
    for token in tokens:
        if type(token) == list:
            new_tokens.extend(compiled_li(token))
        else:
            new_tokens.append(token)
    return compile_1d(new_tokens)

def compile(tokens):
    li = compiled_li(tokens)
    s = ""
    just_par = True
    for token in li:
        if just_par:
            just_par = False
            s += token.value
        elif token == Token(')', "Symbol"):
            s += token.value
        else:
            s += " " + token.value
        if token == Token('(', "Symbol"):
            just_par = True
    return s

if __name__ == "__main__":
    while True:
        s = input()
        p = parse(tokenize(s))
        print(compile(p))
                


