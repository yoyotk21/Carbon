from compiler import compile
from parse import parse
from tokenizer import tokenize
from sys import argv

to_add = """(require 2htdp/image)
(require 2htdp/universe)
(define (then x) x)
(define (-else x) x)
(define (== x y) (= x y))
(define (!= x y) (not (= x y)))
;; The above code was added by the compiler.

"""

if len(argv) < 3:
    raise Exception("Expected 2 files")

readfile = argv[1]
writefile = argv[2]

with open(readfile, 'r') as f:
    code = f.readlines()

code = "".join([line for line in code if not line.strip().startswith(";;")])

code = code.replace("\n", " ")
all_good = False
try:
    parsed_code = parse(tokenize(code))
    lines = [compile(l) + "\n" for l in parsed_code]
    all_good = True
except KeyError as e:
    print("Compiler Error:", e)

if all_good:
    with open(writefile, 'w') as f:
        f.writelines([to_add] + lines)