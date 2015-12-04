# &nbsp; Task

## execute( )

Kicks off processing of queued actions?

**TBD**

## queue( )

```python
# TBD
pass
```

An instance method to add an Action to the task.

### Named Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | ----------------------
action      | Node | None    | A single Node object

### Return

Type | Description
---- | ----------------------
None | No result


## create( )

```python
# create a new task
t = Task.create(work=200, cpus=1, memory=1)
node.assign(t)
```

A factory method to return a new instance of the Task class.

### Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | -----------------------------------------------------
cpus     | Int  | 1       | Number of available CPUs this task desires
memory     | Int  | 1       | Gigabytes of available memory this task desires

### Return

Type | Description
---- | ----------------------
Task | Instance of the Task class
