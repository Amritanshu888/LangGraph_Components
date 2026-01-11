# State Schema With DataClasses
# When we define a LangGraph StateGraph, we use a state schema.

# The state schema represents the structure and types of data that our graph will use.

# All nodes are expected to communicate with that schema.

# LangGraph offers flexibility in how you define your state schema, accommodating various Python types and validation approaches!

# we can use the TypedDict class from python's typing module.

# It allows you to specify keys and their corresponding value types.

# But, note that these are type hints.

# They can be used by static type checkers (like mypy) or IDEs to catch potential type-related errors before the code is run.

# But they are not enforced at runtime!

## Tab 1
from typing_extensions import TypedDict
from typing import Literal

class TypedDictState(TypedDict):
    name:str
    game:Literal["cricket","badminton"]

## Tab 2
def play_game(state:TypedDictState):
    print("---Play Game node has been called--")
    return {"name":state['name'] + " want to play "}

def cricket(state:TypedDictState):
    print("-- Cricket node has been called--")
    return {"name":state["name"] + " cricket","game":"cricket"}

def badminton(state:TypedDictState):
    print("-- badminton node has been called--")
    return {"name":state["name"] + " badminton","game":"badminton"}

## Tab 3
import random
def decide_play(state:TypedDictState)->Literal["cricket","badminton"]:
    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:
        return "cricket"
    else:
        return "badminton"
    
## Tab 4
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

builder=StateGraph(TypedDictState)
builder.add_node("playgame",play_game)
builder.add_node("cricket",cricket)
builder.add_node("badminton",badminton)

## Flow of the graph

builder.add_edge(START,"playgame")
builder.add_conditional_edges("playgame",decide_play)
builder.add_edge("cricket",END)
builder.add_edge("badminton",END)

# Add
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

## Tab 5
graph.invoke({"name":"Krish"})

## Tab 6
graph.invoke({"name":123})

## Tab 7
### Pydantic (Python )
# Dataclasses
# Python's dataclasses provide another way to define structured data.

# Dataclasses offer a concise syntax for creating classes that are primarily used to store data.

### DataClasses

from dataclasses import dataclass

@dataclass
class DataClassState:
    name:str
    game:Literal["badminton","cricket"]

## Tab 8
def play_game(state:DataClassState):
    print("---Play Game node has been called--")
    return {"name":state.name + " want to play "}

def cricket(state:DataClassState):
    print("-- Cricket node has been called--")
    return {"name":state.name + " cricket","game":"cricket"}

def badminton(state:DataClassState):
    print("-- badminton node has been called--")
    return {"name":state.name + " badminton","game":"badminton"}

## Tab 9
import random
def decide_play(state:DataClassState)->Literal["cricket","badminton"]:
    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:
        return "cricket"
    else:
        return "badminton"

## Tab 10
builder=StateGraph(DataClassState)
builder.add_node("playgame",play_game)
builder.add_node("cricket",cricket)
builder.add_node("badminton",badminton)

## Flow of the graph

builder.add_edge(START,"playgame")
builder.add_conditional_edges("playgame",decide_play)
builder.add_edge("cricket",END)
builder.add_edge("badminton",END)

# Add
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

## Tab 11
graph.invoke(DataClassState(name="KRish",game="cricket"))

## Tab 12
graph.invoke(DataClassState(name="KRish",game="cricket"))