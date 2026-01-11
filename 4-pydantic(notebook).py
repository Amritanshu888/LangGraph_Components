## Tab 1
# Pydantic Data Validation
from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel

## Tab 2
class State(BaseModel):
    name:str

## Tab 3
## node function
def example_node(state:State):
    return {"name":"Hello"}

## Tab 4
## stateGraph
builder=StateGraph(State)
builder.add_node("example_node",example_node)

builder.add_edge(START,"example_node")
builder.add_edge("example_node",END)

graph=builder.compile()

## Tab 5
graph.invoke({"name":123})
## This will throw a validation error
  