from typing import List

EMPTY_STRING = ''


class PDA:
    """Pushdown Automata (accepting on empty stack only)"""
    def __init__(self, states, alphabet, stack_alphabet, start_state, start_stack, transitions):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.start_state = start_state
        self.start_stack = start_stack # assume string of length 1
        self.transitions = transitions # here the top of the stack is on the RIGHT of the stack_after string
        # TODO: eliminate unreachable/useless states, symbols, and transitions
        # TODO: make type/length assertions

    @staticmethod
    def from_json(filename):
        import json
        try:
            f = open(filename, 'r')
            obj = json.load(f)
            f.close()
            states = obj.states
            alphabet = obj.alphabet
            stack_alphabet = obj.stack_alphabet
            start_state = obj.start_state
            start_stack = obj.start_stack
            transitions = obj.transitions
            return PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)
        except Exception as exception:
            print("ERROR: could not load", filename, "as PDA.", exception)


    def export_to_json(self, filename):
        import json
        f = open(filename, 'w')
        json.dump(self, f)
        f.close()

    'Converts PDA into CFG using Hopcroft & Ullman "triple" production'
    def to_CFG(self):
        from CFG import CFG
        cfg = CFG()
        cfg.init_variables(self)
        cfg.add_to_alphabet(self.alphabet)
        cfg.init_productions()
        cfg.populate_productions(self)
        cfg.simplify()
        return cfg

    'Simulates PDA on an input x; determines whether or not PDA accepts'
    def accepts(self, x):  # boolean: does this PDA accept input x?
        return self._accepts_(self.start_state, self.start_stack, x)

    def _accepts_(self, current_state, current_stack, x):  # takes current stack as string with top as right
        # TODO: handle infinite epsilon loops
        if current_stack == EMPTY_STRING:
            return len(x) == 0

        if len(x) > 0:
            key = (current_state, x[0], current_stack[0])
            if key in self.transitions:
                next_steps = self.transitions[key]
                for (new_state, new_stack) in next_steps:
                    if self._accepts_(new_state, new_stack+current_stack[1:], x[1:]):
                        return True

        key = (current_state, EMPTY_STRING, current_stack[0])
        if key in self.transitions:
            next_epsilon_steps = self.transitions[key]
            for (new_state, new_stack) in next_epsilon_steps:
                if self._accepts_(new_state, new_stack+current_stack[1:], x):
                    return True

        return False

    def simplify(self):
        # TODO: remove unreachable states
        # TODO: remove unproductive states
        # TODO: remove transitions to/from removed states
        # TODO: simplify alphabet, stack_alphabet
        return

    def to_string_array(self):
        output = ["Input alphabet: " + str(self.alphabet),
                  "Stack alphabet: " + str(self.stack_alphabet),
                  "Start state: " + str(self.start_state),
                  "Start stack: " + str(self.start_stack),
                  "States: " + str(self.states),
                  "Transitions:"]
        temp = []
        for (a, b) in self.transitions.items():
            temp.append("\t" + str(a) + " -> " + str(b))
        temp.sort()
        output.extend(temp)
        return output

    'Outputs PDA as a .gv file, to be printed by dot'
    def output_gv (self):
        output = ['digraph G {']
        output.append('\t"" [shape=none];') # Transition to start state
        for state in self.states:
            output.append('\t"' + str(state) + '";')

        output.append('\t') # a space for the sake of readability

        output.append('\t"" -> "' + str(self.start_state) + '" [label="&epsilon;, &epsilon;/' + str(self.start_stack) + '"];')

        for from_state in self.states:
            for to_state in self.states:
                conditions = []
                for read_symbol in self.alphabet:
                    for stack_top in self.stack_alphabet:
                        if (from_state, read_symbol, stack_top) in self.transitions:
                            for (a,new_stack_top) in self.transitions[(from_state, read_symbol, stack_top)]:
                                if a == to_state:
                                    conditions.append((read_symbol, stack_top, new_stack_top))
                if len(conditions) > 0:
                    build_string = '\t"' + str(from_state) + '" -> "' + str(to_state) + '" [label="'
                    for (read_symbol, stack_top, new_stack_top) in conditions:
                        if read_symbol == EMPTY_STRING:
                            read_symbol = "&epsilon;"
                        if new_stack_top == EMPTY_STRING:
                            new_stack_top = "&epsilon;"
                        build_string += str(read_symbol)+', '+str(stack_top)+'/'+str(new_stack_top)+'\\n'
                    build_string = build_string[:-2] + '"];'  # strip off the last \n and replace with "];
                    output.append(build_string)

        output.append('}')
        return output