To execute, run ``python3 main.py``. To generate diagrams for *k*-flimsy numbers and Maple code to determine the asymptotics of *n*-bit *k*-flimsy numbers, run ``python3 main.py k``.

To use this software, you should add your PDAs and CFGs and operations to the ``main.py`` file. See ``pda_factory.py`` for a list of pre-built PDAs.

To build a PDA, call the constructor ``PDA(states, alphabet, stack_alphabet, start_state, start_stack, transitions)`` where ``states``, ``alphabet``, and ``stack_alphabet`` are iterable structures (preferably sets) containing strings. Note that ``alphabet`` should contain the empty string, but ``stack_alphabet`` should not. The string ``start_state`` must be a member of ``states``, and ``start_stack`` should be a string of length 1 that is a member of ``stack_alphabet``.
Lastly, ``transitions`` is a dictionary mapping `(current_state, read_symbol, stack_top)` to a list of pairs of the form `(next_state, new_stack_top)`.

To build a *k*-flimsy PDA, use `pda_factory.create_flimsy_pda(k)`. To build a *k*-equal PDA, use `pda_factory.create_k_equal_pda(k)`.

To convert a PDA ``pda`` into a CFG, use the function ``pda.to_CFG()``.

To print a PDA ``pda`` as a graphviz file, use ``print_array_to_file(pda.output_gv(), filename)``.

To print a CFG ``cfg`` to text, use ``print_array(cfg.to_string_array())``.

To test whether or not a PDA ``pda`` accepts an input ``x``, use ``pda.accepts(x)``.

To generate the first ``n`` terms (in increasing order length) generated by a CFG ``cfg``, use ``cfg.generate(n)``.

To generate Maple code for determining the asymptotics of an unambiguous CFL (generated by an unambiguous CFG ``cfg``), use ``print_array_to_file(cfg.to_Maple(), filename)``.
