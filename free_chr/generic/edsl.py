from free_chr.generic.state import CHRState

class Bottom(Exception):
    """Exception representing failure of computation (like Prologs 'false' or 'fail')."""
    pass


def match(patterns, active, state):
    """Iterator of the possible matchings for the given state and patterns,
    for the given active (called) constraint.
    """
    for i, p_active in reversed(list(enumerate(patterns))):
        if p_active(active[1]):

            def search(acc, j, used):
                nonlocal i
                nonlocal patterns
                nonlocal active

                if j >= len(patterns):
                    yield acc
                    return

                if i == j:
                    yield from search(acc + [active], j + 1, used | {active[0]})
                else:
                    for c in ((i, c) for i, c in iter(state) if i not in used):
                        if patterns[j](c[1]):
                            yield from search(acc + [c], j + 1, used | {c[0]})

            yield from search([], 0, {active[0]})


def rule(n, k, r, g, b):
    """Creates a solver from a single CHR rule"""

    def solver(state, active):

        matching = next((m
                         for m in match(k + r, active, state)
                         if g(*map(lambda c: c[1], m))
                         if not len(r) == 0 or not state.in_history(n, *map(lambda c: c[0], m))
                         ), None)

        if not matching:
            return False

        success = True

        for c in matching[len(k):]:
            if c[0] is not None:
                state.kill(c[0])

        for c in reversed(list(b(*map(lambda x: x[1], matching)))):
            if isinstance(c, Exception):
                raise c
            if c is not None:
                state.add_to_query(state.new(), c)

        if len(r) == 0:
            state.to_history(n, *map(lambda x: x[0], matching))

        return success

    return solver


def compose(*solvers):
    """Composes solvers, by sequentially applying them to the store,
    until application changes the state."""

    def composite_solver(state, active):
        for s in solvers:
            if s(state, active):
                return True

        return False

    return composite_solver


def run_solver(solver):
    """Runs a solver until a fixed point is reached"""

    def solve(*constraints, start_state=None):
        if not start_state:
            state = CHRState()
        else:
            state = start_state

        for c in constraints:
            state.add_to_query(state.new(), c)

        while state.query:
            i, c = state.query.pop()
            while state.alive(i) and solver(state, (i, c)):
                pass
            if state.alive(i):
                state.add(c, i)
        
        return state

    return solve


### Quality of life definitions

def true(*vargs):
    """Returns True, whatever may be"""
    return True


def false(*vargs):
    """Returns False, whatever may be"""
    return False


def top(*vargs):
    """Returns the empty list, whatever may be"""
    return []


def bottom(*vargs):
    """Fails computation, whatever may be"""
    return [Bottom()]


def eq(x):
    """Matched constraint is equal to x"""
    return lambda y: y == x


def leq(x):
    """Matched cosntraint is less-equal x"""
    return lambda y: y <= x


def lt(x):
    """Matched constraint is less than x"""
    return lambda y: y < x


def geq(x):
    """Matched constraint is greater-equal x"""
    return lambda y: y >= x


def gt(x):
    """Matched constraint is greater than x"""
    return lambda y: y > x


def body(*constraints):
    """Rule-body with given constraints, regardless of matched constraints."""
    def f(*_):
        return list(constraints)
