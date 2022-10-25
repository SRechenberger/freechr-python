from free_chr.generic.state import *
from free_chr.generic.edsl import *

gcd_solver = run_solver(compose(
    rule("zero", [], [eq(0)], true, top),
    rule("subtract", [gt(0)], [gt(0)], (lambda n, m: n <= m), (lambda n, m: [m-n]))
))