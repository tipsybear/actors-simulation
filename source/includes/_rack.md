# &nbsp; Rack

The `Rack` class represents a physical enclosure for `Node` objects.  Racks may be connected to other racks and can be added to clusters.

Racks also encapsulate the idea of bandwidth and latency as the manifestation of the physical network.  Latency is actually the base latency plus a function of the available bandwidth.

There is also a link_latency to model the traffic delay to go across racks.  For the time being we will assume all racks are connected to a smart switch such that latency from any rack to any rack is the same.

## add( )

```python
# adds a node to an existing rack
myrack = Rack(racks=3)
node = Node.create(cpus=4, memory=16)
myrack.add(node)
```

An instance method to add one or more nodes to the existing rack.

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
# create a new rack
rack = Rack.create(capacity=128, base_latency=10)
```

A factory method to return a new instance of a `Rack` object.

Parameter | Type | Default | Description
--------- | ---- | ------- | -----------------------------------------------------
capacity     | Int  | 128       | Amount of nodes this rack can hold
base_latency     | Int  | 10       | Underlying latency associated with network traffic assuming all available bandwidth.
egress_latency     | Int  | 10       | Additional latency associated with network traffic destined for another rack.


## filter( )

```python
# removes a node from an existing rack
myrack = Rack(racks=3)
node = Node.create(cpus=4, memory=16)
myrack.add(node)

nodes = myrack.filter(lambda n: return n.cpus > 2)
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
node = myrack.first(lambda n: return n.idle_cpus > 1 and n.idle_memory > 0)
```

An instance method to return the first node that satisfies a test function.  This method could be used when assigning a task to the first available node.

The default test function/lambda returns the first node added to the rack.

### Named Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | ----------------------
test  | Function | lambda n: return True    | A function to test for inclusion in the result

### Return

Type | Description
---- | ----------------------
Node | The rack's first `Node` instance that matches criteria


## promulgate( )

```python
# something goes here
pass
```

**looking for a better name**

An instance method to reserve bandwidth for a network operation.  The amount of bandwidth reserved will automatically be freed after the traffic has "cleared" the network.

### Named Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | ----------------------
size      | Int | None    | The amount of bandwidth to use

### Return

Type | Description
---- | ----------------------
None | No result


## remove( )

```python
# removes a node from an existing rack
myrack = Rack(racks=3)
node = Node.create(cpus=4, memory=16)
myrack.add(node)
...
myrack.remove(node)
```

An instance method to remove one or more nodes from the existing rack.  

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



## base_latency

```python
cluster = Cluster.create(racks=3)
node = Node.create(cpus=4, memory=12)

cluster.add(node)
print node.rack.base_latency
```

Read only instance property to return the underlying latency for traffic within the Rack.

### Return

Type | Description
---- | ----------------------
Int | Delay associated with network traffic assuming all available bandwidth


## egress_latency

```python
cluster = Cluster.create(racks=3)
node = Node.create(cpus=4, memory=12)

cluster.add(node)
print node.rack.egress_latency
```

Read only instance property to return the additional delay for traffic leaving the Rack.

### Return

Type | Description
---- | ----------------------
Int | Delay associated with network traffic leaving the current rack for another


## latency

```python
cluster = Cluster.create(racks=3)
node = Node.create(cpus=4, memory=12)

cluster.add(node)
print node.rack.latency

```
Read only instance property to return the rack's network latency.  This value is derived from the base_latency plus a function of the available bandwidth.

### Return

Type | Description
---- | ----------------------
Int | Computed delay associated with network traffic
