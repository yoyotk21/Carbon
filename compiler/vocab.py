symbols = ['(', ')', ',', '[', ']', ';']
symbol_operations = ['<=', '>=',  '+', '-', '*', '/', '<', '>', '^', '~', "&", '@']
keyword_operations = ['and', 'or', 'not',  "==", "!="]
keywords = ['if', 'else', 'then', 'while', 'for', 'fun', "=", "expects", "expects_random", "satisfies", 'struct']

operation_order = [['~'], ['@'], ['^'], ['*', '/'], ['+', '-'], ['not'], ['>', '>=', '<', '<='], ['==', '!='], ['and', 'or', 'new'], ['&']]
keyword_order = [['if', 'else', 'then'], ['for', 'while' ], ["expects", "expects_random", "satisfies"], ['fun', '=', 'struct']]

def same_level(t1, t2):
    for li in keyword_order:
        if t1 in li and t2 in li:
            return True
    for li in operation_order:
        if t1 in li and t2 in li:
            return True
    return False

symkey_args = {}
for s in ['<=', '>=', '==', '!=', '+', '-', '*', '/', '<', '>', '^', '=', 'and', 'or', 'expects', 'expects_random', "satisfies", '&', '@']:
    symkey_args[s] = (1, 1) # one argument before one after

for s in ['~', 'not', 'else', 'then']:
    symkey_args[s] = (0, 1)

for s in ['val', 'struct']:
    symkey_args[s] = (0, 2)

for s in ['fun', 'if']:
    symkey_args[s] = (0, 3)

