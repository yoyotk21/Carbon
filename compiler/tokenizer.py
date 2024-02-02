from vocab import *

def get_type(data_str):
    if data_str == '':
        return "None"

    if data_str[0] == '"':
        if data_str[-1] == '"':
            return "String"
        else:
            raise Exception('Mismatched quotes')
    
    if data_str in symbols:
        return "Symbol"

    number = True
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for c in data_str:
        if c not in digits:
            number = False
    if number:
        has_digit = False
        for digit in digits[:-1]:
            if digit in data_str:
                has_digit = True
        if has_digit:
            return "Number"

    if data_str in ("true", "false"):
        return "Boolean"

    if data_str in symbol_operations or data_str in keyword_operations:
        return "Operation"

    if data_str in keywords:
        return "Keyword"

    return "Name"
counter = 0
class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type 

    def empty(self):
        return self.type == "None"

    def __eq__(self, other):
        global counter
        counter += 1
        if counter % 1000 == 0:
            False
        return type(other) == Token and self.type == other.type and self.value == other.value

    def __repr__(self):
        return self.value + " : " + self.type

def tokenize(code):
    quotes = False

    handle_quotes = ['']
    for c in code:
        if c == '"':
            if quotes:
                handle_quotes[-1] += (c)
                handle_quotes.append("")
            else:
                handle_quotes.append(c)
            quotes = not quotes
        elif quotes:
            handle_quotes[-1] += c
        elif c == ' ':
            handle_quotes.append("")
        else:
            handle_quotes[-1] += (c)
    
    new_chars = []
    for s in handle_quotes:
        if s.startswith('"'):
            new_chars.append(s)
        else:
            new_s = []
            inds = {}
            prev = 0
            for symbol in (symbol_operations + symbols):
                while symbol in s:
                    inds[s.find(symbol)] = symbol
                    s = s.replace(symbol, ' ' * len(symbol), 1)
            for i in sorted(inds):
                new_s.append(s[prev:i])
                new_s.append(inds[i])
                prev = i
            new_s.append(s[prev:])
            added_str = [c.strip() for c in new_s if c.strip() != '']
            if added_str != ['']:
                new_chars += added_str
    return [Token(c, get_type(c)) for c in new_chars]
            
if __name__ == '__main__':
    while True:
        print(tokenize(input()))
    