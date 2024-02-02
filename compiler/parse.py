from tokenizer import Token, tokenize
from vocab import *

def list_has_tp(li, tp):
    for val in li:
        if type(val) != list and val.type == tp:
            return True 
    return False

def list_has(li, token):
    for val in li:
        if type(val) == Token and val == token:
            print("list_has returning True")
            return True
    return False

def find_token(li, token):
    if type(li) == Token:
        return li == token
    for i in range(len(li)):
        if type(li[i]) == Token and li[i] == token:
            return i
    return False

def has_some(li):
    for i in li:
        if type(i) == Token and i.value in symkey_args:
            return True 
    return False

def replace(tokens, operation, ind):
    before, after = symkey_args[operation.value]
    li = [operation]
    while has_some(tokens[ind-before:ind]):
        for i in range(1, before+1):
            if type(tokens[ind-1]) == Token and same_level(operation.value, tokens[ind-i].value):
                tokens = replace(tokens, tokens[ind-i], ind-i)
                break
    while has_some(tokens[ind+1:ind+after+1]):
        for i in range(1, after+1):
            if type(tokens[ind+i]) == Token and same_level(operation.value, tokens[ind+i].value):
                tokens = replace(tokens, tokens[ind+i], ind+i)
                break
    li += tokens[ind-before:ind]
    li += tokens[ind+1:ind+after+1]
    tokens[ind] = li
    new_tokens = []
    for i in range(len(tokens)):
        if i not in range(ind-before, ind+after+1) or i == ind:
            new_tokens.append(tokens[i])
    return new_tokens


def replace_operations(tokens):
    while list_has_tp(tokens, "Operation"):
        for operation_list in operation_order:
            for i in range(len(tokens)):
                if type(tokens[i]) == Token and tokens[i].value in operation_list:
                    tokens = replace(tokens, tokens[i], i)
                    break
    return tokens

def replace_keywords(tokens):
    while list_has_tp(tokens, "Keyword"):
        for keyword_list in keyword_order:
            to_brake = False
            for i in range(len(tokens)):
                if type(tokens[i]) == Token and tokens[i].value in keyword_list:
                    tokens = replace(tokens, tokens[i], i)
                    # tokens[i] = [tokens[i][0]] + replace_keywords(tokens[i][1:])
                    to_brake = True
                    break
            if to_brake:
                break
    return tokens

def parse_1d(tokens):
    tokens = replace_operations(tokens) # operations should come first 
    tokens = replace_keywords(tokens)
    return tokens
    

def parse(tokens):
    left_par = Token('(', 'Symbol')
    right_par = Token(')', 'Symbol')

    token_tree = []
    tmps = []
    par_count = 0
    for token in tokens:
        if token == left_par:
            par_count += 1
            tmps.append([])
        elif token == right_par:
            if par_count == 0:
                raise Exception("Expected '(' before ')'")
            par_count -= 1
            if par_count == 0:
                tmps[-1] = parse_1d(tmps[-1])
                token_tree.append(tmps[-1])
            else:
                tmps[-2].append(tmps[-1])
            tmps = tmps[:-1]
        elif par_count == 0:
            token_tree.append(token)
        else:
            tmps[-1].append(token)

    token_tree = parse_1d(token_tree)
    if par_count > 0:
        raise Exception(f"Expected {par_count} more ')'")

    return token_tree

if __name__ == "__main__":
    while True:
        print(parse(tokenize(input())))





