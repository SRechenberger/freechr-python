from free_chr.generic.state import CHRState
from free_chr.generic.edsl import *

from free_chr.finite_domains.constraints import *


fd_solver = run_solver(compose(
    rule("inconsistency",
        [], [lambda c: not c.is_consistent()],
        true,
        bottom
    ),
    rule("subsumption",
        [true], [true],
        lambda x, y: x.ident == y.ident and x.values.issubset(y.values),
        top
    ),
    rule("intersection",
        [], [true, true],
        lambda x, y: x.ident == y.ident,
        lambda x, y: [in_domain(x.ident, *x.values.intersection(y.values))]
    ),
))