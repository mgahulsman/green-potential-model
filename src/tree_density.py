def tree_density(tree_data, area="WIJK"):
    n_trees = tree_data.value_counts(area)
    return n_trees  # Divided bij the surface ofcours
