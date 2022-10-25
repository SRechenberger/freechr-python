from free_chr.generic.state import CHRState
from free_chr.generic.edsl import *

class EnumDomainConstraint:
    """Enumeration-Domain constraint"""
    def __init__(self, ident, *values):
        self.ident = ident
        self.values = set(values)

    def is_consistent(self):
        return bool(self.values)

    def __eq__(self, other):
        return isinstance(other, EnumDomainConstraint) and \
            self.ident == other.ident and \
            self.values == other.values



def in_domain(name, *values):
    return EnumDomainConstraint(name, *values)


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