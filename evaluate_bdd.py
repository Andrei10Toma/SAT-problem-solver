def test_bdd(bdd_tree_node):
    if bdd_tree_node.left is None or bdd_tree_node.right is None:
        if bdd_tree_node.data == 1:
            return True
        return False
    if test_bdd(bdd_tree_node.left) is True:
        return True
    if test_bdd(bdd_tree_node.right) is True:
        return True
    return False
