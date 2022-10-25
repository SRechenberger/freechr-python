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


## QoL definitions
def in_domain(name, *values):
    return EnumDomainConstraint(name, *values)