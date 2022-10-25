class CHRState:
    """ CHR-State with propagation history and a query."""

    def __init__(self, *initial_query, store_immediately=False):
        self.next = 0
        self.store = {}
        self.history = {}
        self.alive_set = set()
        self.query = []
        if store_immediately:
            for c in initial_query:
                self.add(c, self.new())
        else:
            for c in initial_query:
                self.add_to_query(self.new(), c)

    def wakeup(self, condition):
        """Adds constraints to the query, if
            - condition is True
            - OR condition is callable, and applying it to the constraint yields True
        """
        if isinstance(condition, bool) and condition:
            for i, c in self.store.items():
                self.add_to_query(i, c)

        elif callable(condition):
            for i, c in self.store.items():
                if condition(i, c):
                    self.add_to_query(i, c)

    def new(self):
        """Returns a fresh id for a new constraint"""
        i = self.next
        self.alive_set.add(i)
        self.next += 1
        return i

    def add(self, c, i):
        """Adds a new constraint with the given id"""
        self.store[i] = c
        return i

    def add_to_query(self, i, c):
        """Adds an id-constraint-pair to the query"""
        self.query.append((i, c))

    def kill(self, i):
        """Removes the constraint with the given id from the store"""
        if i in self.store:
            del self.store[i]
        self.alive_set.remove(i)

    def alive(self, i):
        """Checks, whether the constraint with the given id is still alive"""
        return i in self.alive_set

    def in_history(self, rule_id, *constraint_ids):
        """Checks, whether the rule with the given id has been
        called with the given sequence of constraint ids.
        """
        return rule_id in self.history and \
               constraint_ids in self.history[rule_id]

    def to_history(self, rule_id, *constraint_ids):
        """Adds a history entry with the given rule-id and sequence of constraint ids."""
        if rule_id in self.history:
            self.history[rule_id].add(constraint_ids)
        else:
            self.history[rule_id] = set((constraint_ids), )

    def __iter__(self):
        """Iterate over the stored id-constraint pairs"""
        return ((i, c) for i, c in self.store.items())

    def constraints(self):
        """Iterate over the stored constraints (without ids for output purposes)"""
        return (c for c in self.store.values())

    def __eq__(self, other):
        return isinstance(other, CHRState) and \
            self.query == other.query and \
            self.next == other.next and \
            self.store == other.store and \
            self.history == other.history
