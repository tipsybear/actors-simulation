# &nbsp; Node


## assign( )

```python
# create node
node = Node.create(cpus=4, memory=16)

# start processing a new task
node.assign(task=mytask)

```

Instance method to start processing a task.

### Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | -----------------------------------------------------
task | Task  |  | An instance of `Task` to start processing

### Return

Type | Description
---- | ----------------------
None | No result


## create( )

```python
# create a new node
node = Node.create(cpus=4, memory=16)
```

A factory method to return a new instance of a Node object.

### Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | -----------------------------------------------------
cpus     | Int  | 1       | Number of CPUs for this node
memory     | Int  | 1       | Gigabytes of memory for this node

### Return

Type | Description
---- | ----------------------
Node | Instance of the Node class


## send( )

```python
# create node
node_1 = Node.create(cpus=4, memory=16)

# send message from node_1 to another node with an ID of 12
node_1.send(recipient=12, size=100)
```

Instance method to send a message to another node.

### Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | -----------------------------------------------------
recipient | Int  |  | ID of the node recipient
size | Int  | 10 | Size of message
async | bool  | False | Whether this is a asynchronous message send operation

### Return

Type | Description
---- | ----------------------
Boolean | Success of the operation


## work( )

```python
# create node
node = Node.create(cpus=4, memory=16)

# start processing a new task
node.work(duration=100)

```

Instance method to start an arbitrary work phase for the given duration.

### Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | -----------------------------------------------------
duration | Int  |  | A abstract unit for measuring work to be performed

### Return

Type | Description
---- | ----------------------
None | No result










## cpus

```python
# print total number of CPUs
node = Node.create(cpus=4, memory=16)
print node.cpus
>>> 4

```
Read only instance property to return the number of CPUs configured for the Node instance.

### Return

Type | Description
---- | ----------------------
Int | Number of CPUs for this node


## id

```python
# print id for a given node
node = Node.create(cpus=4, memory=16)
print node.id
>>> 42
```

Read only instance property to return the ID of the given node.  This can be used as a Node address as all nodes in a cluster will have a unique ID.

### Return

Type | Description
---- | ----------------------
Int | Unique identifier for this node.


## idle_cpus

```python
# print number of available CPUs
node = Node.create(cpus=4, memory=16)
print node.idle_cpus
>>> 4

```
Read only instance property to return the number of CPUs not reserved by current tasking.

### Return

Type | Description
---- | ----------------------
Int | Number of CPUs not reserved by current tasking


## idle_memory

```python
# print amount of idle node memory
node = Node.create(cpus=4, memory=16)
print node.idle_memory
>>> 16

```
Read only instance property to return the total Gigabytes of memory that have not been reserved by current tasking.

### Return

Type | Description
---- | ----------------------
Int | Gigabytes of memory that have not been reserved by current tasking.


## memory

```python
# print total amount of node memory
node = Node.create(cpus=4, memory=16)
print node.memory
>>> 16

```
Read only instance property to return the total Gigabytes of memory configured for the Node instance.

### Return

Type | Description
---- | ----------------------
Int | Gigabytes of memory for this node


## rack

```python
cluster = Cluster.create(racks=3)
node = Node.create(cpus=4, memory=12)

cluster.add(node)
rack = node.rack
```

Read only instance property to return the `Rack` instance this node resides on.

### Return

Type | Description
---- | ----------------------
Rack | An instance of `Rack` which this node has been assigned to.
