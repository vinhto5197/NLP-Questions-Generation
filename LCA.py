
def lca_len(l1, l2):
    count = 0
    while count < len(l1) and count < len(l2) and l1[count] == l2[count]:
        count += 1
    return count


def findLCA(ptree, t1, t2):
    leaf = ptree.leaves()
    idx1 = leaf.index(t1)
    idx2 = leaf.index(t2)

    l1 = ptree.leaf_treeposition(idx1)
    l2 = ptree.leaf_treeposition(idx2)

    lca_length = lca_len(l1, l2)
    return ptree[l1[:lca_length]]
