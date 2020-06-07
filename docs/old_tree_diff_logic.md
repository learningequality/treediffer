

## Old tree diff logic based on counts

We can use a flatlist approach to easily compute the list of nodes that were added,
deleted, and moved by processing a list of `(parent_node_id, node_id)` tuples,
treating them as labelled edges in a graph, each edge labelled by its `content_id`.

For each content id in the union(oldtree, newtree), we select the edges with that
label and look at the counts of the `node_id` among the `(parent_node_id, node_id)` edges:
  - newCount = # of times content id is in oldtree
  - oldCount = # of times content id is in newtree
  - node_id_diff = union(new node ids, old node ids) - intersection(new node ids, old node ids)


```
 oldCount = newCount  | oldCount > newCount                    | oldCount < newCount
-----------------------------------------------------------------------------------------------------
 All nodes in         | (oldCount - newCount)                  | (newCount - oldCount)
 node_id_diff         | have been deleted,                     | have been added,
 have moved (1)       |                                        |
                      | (newCount - len(node_intersection))    | (newCount - len(node_intersection))
                      | have moved (2)                         | have moved (3)
```



 - `(1)` Questions:
    - how do you know which moved to which? -- assuming all identical, just choose arbitrary matching
    - how to detect case when node sort order changed but parent_id and node_id stay the same
 - `(2)` or stayed unchanged? what is node_intersection?
 - `(3)` ?
 
 
 
