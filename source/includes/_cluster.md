
# Object Model

For lack of a better name, the cluster framework provides the basic objects representing physical compute resources and underlying technologies such as the nodes, racks, and network.

The available classes are:

- cluster
- rack
- node
- task

# &nbsp; Cluster

The Cluster class represents a collection of nodes running on top of subordinate network resources.

## add( )

```python
# adds a node to an existing cluster
mycluster = Cluster(racks=3)
node = Node.create(cpus=4, memory=16)
mycluster.add(node)
```

An instance method to add one or more nodes to the existing cluster.

### Named Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | ----------------------
node      | Node | None    | A single Node object
nodes     | list | [ ]     | A list of Node objects

### Return

Type | Description
---- | ----------------------
Boolean | Success of the operation


## create( )

```python
# create a new cluster
mycluster = Cluster(racks=3)
```

A factory method to return a new instance of a Cluster object.

Parameter | Type | Default | Description
--------- | ---- | ------- | -----------------------------------------------------
racks     | Int  | 1       | The number of physical racks available to the cluster

## filter( )

```python
# removes a node from an existing cluster
mycluster = Cluster(racks=3)
node = Node.create(cpus=4, memory=16)
mycluster.add(node)

nodes = mycluster.filter(lambda n: return n.cpus > 2)
```

An instance method to query for specific nodes.

It is uncertain at this time as to whether we will need this method implemented.

### Named Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | ----------------------
test  | Function | None    | A function to test for inclusion in the result

### Return

Type | Description
---- | ----------------------
list | An array of `Node` objects that satisfy the criteria function.


## first( )

```python
# find the first node that matches criteria
node = mycluster.first(lambda n: return n.idle_cpus > 1 and n.idle_memory > 0)
```

An instance method to return the first node that satisfies a test function.  This method could be used when assigning a task to the first available node.

The default test function/lambda returns the first node added to the cluster.

### Named Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | ----------------------
test  | Function | lambda n: return True    | A function to test for inclusion in the result

### Return

Type | Description
---- | ----------------------
Node | The cluster's first `Node` instance that matches criteria


## remove( )

```python
# removes a node from an existing cluster
mycluster = Cluster(racks=3)
node = Node.create(cpus=4, memory=16)
mycluster.add(node)
...
mycluster.remove(node)
```

An instance method to remove one or more nodes from the existing cluster.  

It is uncertain at this time as to whether we will need this method implemented.

### Named Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | ----------------------
node      | Node | None    | A single Node object
nodes     | list | []      | A list of Node objects

### Return

Type | Description
---- | ----------------------
Boolean | Success of the operation
