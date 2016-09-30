from operators.initialisation import generate_ind_tree
from algorithm.parameters import params
from representation.tree import Tree
from collections import deque
from random import randint


def mapper(genome, tree):
    """
    Wheel for mapping. Calls the correct mapper for a given input. Checks
    the params dict to ensure the correct type of individual is being created.

    If a genome is passed in with no tree, all tree-related information is
    generated. If a tree is passed in with no genome, the genome is
    sequenced from the tree. If neither is passed in, a new randomly
    generated individaul is generated.

    :param genome: Genome of an individual.
    :param tree: Tree of an individual.
    :return: All components necessary for a fully mapped individual.
    """

    phenotype, nodes, invalid, depth, used_codons = None, None, None, None, \
        None

    if genome:
        # We have a genome and need to map an individual from that genome.
        
        genome = list(genome)
        # This is a fast way of creating a new unique copy of the genome
        # (prevents cross-contamination of information between individuals).

        if not tree:
            # We have a genome but no tree. We need to map an individual
            # from the genome and generate all tree-related info.
            
            if params['GENOME_OPERATIONS']:
                # Can generate tree information faster using
                # algorithm.mapper.map_ind_from_genome() if we don't need to
                # store the whole tree.
                phenotype, genome, tree, nodes, invalid, depth, \
                    used_codons = map_ind_from_genome(genome)
            
            else:
                # Build the tree using algorithm.mapper.map_tree_from_genome().
                phenotype, genome, tree, nodes, invalid, depth, \
                    used_codons = map_tree_from_genome(genome)

    else:
        # We do not have a genome.

        if tree:
            # We have a tree but need to generate a genome from the
            # fully mapped tree.
            genome = tree.build_genome([])

            # Generate genome tail.
            used_codons = len(genome)
            genome = genome + [randint(0, params['CODON_SIZE']) for _ in
                               range(int(used_codons / 2))]

        else:
            # We have neither a genome nor a tree. We need to generate a new
            # random individual.

            if params['GENOME_INIT']:
                # We need to initialise a new individual from a randomly
                # generated genome.

                # Generate a random genome
                genome = [randint(0, params['CODON_SIZE']) for _ in
                          range(params['GENOME_LENGTH'])]

                if params['GENOME_OPERATIONS']:
                    # Initialise a new individual from a randomly generated
                    # genome without generating a tree. Faster.
                                        
                    # Map the genome to all parameters needed for an
                    # individual.
                    phenotype, genome, tree, nodes, invalid, \
                        depth, used_codons = map_ind_from_genome(list(genome))

                else:
                    # Initialise a new individual from a randomly generated
                    # genome by mapping using the tree class.
                    
                    # Map the genome to all parameters needed for an
                    # individual.
                    phenotype, genome, tree, nodes, invalid, \
                        depth, used_codons = map_tree_from_genome(list(genome))

            else:
                # We need to initialise a new individual from a randomly
                # generated tree.
                ind = generate_ind_tree(params['MAX_TREE_DEPTH'], "random")

                # Extract all parameters needed for an individual.
                phenotype, genome, tree, nodes, invalid, depth, \
                    used_codons = ind.phenotype, ind.genome, ind.tree, \
                    ind.nodes, ind.invalid, ind.depth, ind.used_codons

    if not phenotype and not invalid:
        # If we have no phenotype we need to ensure that the solution is not
        # invalid, as invalid solutions have a "None" phenotype.
        phenotype = tree.get_output()

    if not used_codons:
        # The number of used codons is the length of the genome.
        used_codons = len(genome)

    if invalid is None:
        # Need to ensure that invalid is None and not False. Can't say "if
        # not invalid" as that will catch when invalid is False.
        invalid = tree.check_expansion()

    if not depth and not nodes:
        # Need to get the depth of the tree and and its number of nodes.
        depth, nodes = tree.get_tree_info(tree)
        depth += 1

    return phenotype, genome, tree, nodes, invalid, depth, used_codons


def map_ind_from_genome(genome):
    """
    A fast genotype to phenotype mapping process. Map input via rules to
    output. Does not require the recursive tree class, but still calculates
    tree information, e.g. number of nodes and maximum depth.
    
    :param genome: A genome to be mapped.
    :return: Output in the form of a phenotype string ('None' if invalid),
             Genome,
             None (this is reserved for the derivation tree),
             The number of nodes in the derivation,
             A boolean flag for whether or not the individual is invalid,
             The maximum depth of any node in the tree, and
             The number of used codons.
    """

    from utilities.helper_methods import python_filter
    
    # Create local variables to avoide multiple dictionary lookups
    max_tree_depth, max_wraps = params['MAX_TREE_DEPTH'], params['MAX_WRAPS']
    nt_symbol, bnf_grammar = params['BNF_GRAMMAR'].NT, params['BNF_GRAMMAR']

    n_input = len(genome)

    # Depth, max_depth, and nodes start from 1 to account for starting root
    # Initialise number of wraps at -1 (since
    used_input, current_depth, max_depth, nodes, wraps = 0, 1, 1, 1, -1
    
    # Initialise output as empty deque list (deque is a list-like container
    # with fast appends and pops on either end).
    output = deque()
    
    # Initialise the list of unexpanded non-terminals with the start rule.
    unexpanded_symbols = deque([(bnf_grammar.start_rule, 1)])
    
    while (wraps < max_wraps) and \
            unexpanded_symbols and \
            (max_depth <= max_tree_depth):
        # While there are unexpanded non-terminals, and we are below our
        # wrapping limit, and we haven't breached our maximum tree depth, we
        # can continue to map the genome.
        
        if used_input % n_input == 0 and \
                        used_input > 0 and \
                any([i[0][1] == nt_symbol for i in unexpanded_symbols]):
            # If we have reached the end of the genome and unexpanded
            # non-terminals remain, then we need to wrap back to the start
            # of the genome again. Can break the while loop.
            wraps += 1

        # Expand a production from the list of unexpanded non-terminals.
        current_item = unexpanded_symbols.popleft()
        current_symbol, current_depth = current_item[0], current_item[1]
        
        if max_depth < current_depth:
            # Set the new maximum depth.
            max_depth = current_depth

        # Set output if it is a terminal.
        if current_symbol[1] != nt_symbol:
            output.append(current_symbol[0])
        
        else:
            # Current item is a new non-terminal. Find associated production
            # choices.
            production_choices = bnf_grammar.rules[current_symbol[0]]
            
            # Select a production based on the next available codon in the
            # genome.
            # TODO store the length of production choices to avoid len call?
            current_production = genome[used_input % n_input] % \
                len(production_choices)
            
            # Use an input
            used_input += 1
            
            # TODO: Derviation order is left to right(depth-first). Is a
            # list comprehension faster? (Only if the loop for counting NT for
            # each production can be avoided, by using a lookup instead.
            
            # Initialise children as empty deque list.
            children = deque()
            nt_count = 0
            
            for prod in production_choices[current_production]:
                # iterate over all elements of chosen production rule.
                
                child = [prod, current_depth + 1]
                
                # Extendleft reverses the order, thus reverse adding.
                children.appendleft(child)
                # TODO store number of NT to avoid counting and simply do
                # lookup instead?
                if child[0][1] == nt_symbol:
                    nt_count += 1
            
            # Add the new children to the list of unexpanded symbols.
            unexpanded_symbols.extendleft(children)

            if nt_count > 0:
                nodes += nt_count
            else:
                nodes += 1

    # Generate phenotype string.
    output = "".join(output)

    if len(unexpanded_symbols) > 0:
        # All non-terminals have not been completely expanded, invalid
        # solution.
        
        return None, genome, None, nodes, True, max_depth, used_input

    if bnf_grammar.python_mode:
        # Grammar contains python code

        output = python_filter(output)

    return output, genome, None, nodes, False, max_depth, used_input


def map_tree_from_genome(genome):
    """
    Maps a full tree from a given genome.
    
    :param genome: A genome to be mapped.
    :return: All components necessary for a fully mapped individual.
    """

    # Initialise an instance of the tree class
    tree = Tree(str(params['BNF_GRAMMAR'].start_rule[0]),
                None, depth_limit=params['MAX_TREE_DEPTH'])
    
    # Map tree from the given genome
    used_codons, nodes, depth, max_depth, invalid = \
        genome_tree_map(tree, genome, 0, 0, 0, 0)
    
    if invalid:
        # Return "None" phenotype if invalid
        return None, genome, tree, nodes, invalid, max_depth, \
           used_codons
    else:
        # Build phenotype and return
        return tree.get_output(), genome, tree, nodes, invalid, max_depth, \
           used_codons


def genome_tree_map(tree, genome, index, depth, max_depth, nodes,
                    invalid=False):
    """
    Recursive function which builds a tree using production choices from a
    given genome. Not guaranteed to terminate.
    
    :param tree: An instance of the representation.tree.Tree class.
    :param genome: A full genome.
    :param index: The index of the current location on the genome.
    :param depth: The current depth in the tree.
    :param max_depth: The maximum overall depth in the tree so far.
    :param nodes: The total number of nodes in the tree thus far.
    :param invalid: A boolean flag indicating whether or not the individual
    is invalid.
    :return: index, the index of the current location on the genome,
             nodes, the total number of nodes in the tree thus far,
             depth, the current depth in the tree,
             max_depth, the maximum overall depth in the tree,
             invalid, a boolean flag indicating whether or not the
             individual is invalid.
    """
    
    if not invalid and index < len(genome) and \
        max_depth <= params['MAX_TREE_DEPTH']:
        # If the solution is not invalid thus far, and if we still have
        # remaining codons in the genome, and if we have not exceeded our
        # maximum depth, then we can continue to map the tree.
        # TODO: Enable wrapping for genome_tree_map.
        
        # Increment and set number of nodes and current depth.
        nodes += 1
        depth += 1
        tree.id, tree.depth = nodes, depth

        # Find all production choices that can be made by the current root
        # non-terminal.
        productions = params['BNF_GRAMMAR'].rules[tree.root]
        
        # Set the current codon value from the genome.
        tree.codon = genome[index % len(genome)]
        
        # Select the index of the correct production from the list.
        selection = tree.codon % len(productions)
        
        # Set the chosen production
        chosen_prod = productions[selection]

        # Increment the index
        index += 1
        
        # Initialise an empty list of children.
        tree.children = []

        for i in range(len(chosen_prod)):
            # Add children to the derivation tree by creating a new instance
            # of the representation.tree.Tree class for each child.
            
            symbol = chosen_prod[i]
            
            if symbol[1] == "T":
                # Append the child to the parent node. Child is a terminal, do
                # not recurse.
                tree.children.append(Tree(symbol[0], tree))

            elif symbol[1] == "NT":
                # Append the child to the parent node.
                tree.children.append(Tree(symbol[0], tree))
                
                # Recurse by calling the function again to map the next
                # non-terminal from the genome.
                index, nodes, d, max_depth, invalid = \
                    genome_tree_map(tree.children[-1], genome,
                                    index, depth, max_depth, nodes,
                                    invalid=invalid)
    
    else:
        # Mapping incomplete, solution is invalid.
        return index, nodes, depth, max_depth, True

    # Find all non-terminals in the chosen production choice.
    NT_kids = [kid for kid in tree.children if kid.root in
               params['BNF_GRAMMAR'].non_terminals]
    
    if not NT_kids:
        # There are no non-terminals in the chosen production choice, the
        # branch terminates here.
        depth += 1
        nodes += 1

    if not invalid:
        # The solution is valid thus far.
        
        if (depth > max_depth):
            # Set the new maximum depth.
            max_depth = depth
        
        if max_depth > params['MAX_TREE_DEPTH']:
            # If our maximum depth exceeds the limit, the solution is invalid.
            invalid = True
    
    return index, nodes, depth, max_depth, invalid
