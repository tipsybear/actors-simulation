# &nbsp; Action

**This class is still in discussion/definition phase.  It may be removed in favor of something else.**

## create( )

```python
# create a new task
a = Action.create(work=200)
node.assign(t)
```

A factory method to return a new instance of the Action class.  Actions are only useful when added to a `Task` instance.



### Arguments

Parameter | Type | Default | Description
--------- | ---- | ------- | -----------------------------------------------------
work     | Int  |        | Arbitrary unit of work

### Return

Type | Description
---- | ----------------------
Action | Instance of the Action class
