## Tab 1
# Implementing simple Chatbot Using LangGraph
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

## Reducers
from typing import Annotated
from langgraph.graph.message import add_messages

## Tab 2
class State(TypedDict):
    messages:Annotated[list,add_messages]

## Tab 3
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

## Tab 4
from langchain_openai import ChatOpenAI
llm=ChatOpenAI(model="gpt-4o")
llm.invoke("Hello")

## Tab 5
from langchain_groq import ChatGroq

llm_groq=ChatGroq(model="qwen-qwq-32b")
llm_groq.invoke("Hey I am Krish and i like to play cricket")

## Tab 6
# We Will start With Creating Nodes
from langgraph.checkpoint.memory import MemorySaver
memory=MemorySaver()
def superbot(state:State):
    return {"messages":[llm_groq.invoke(state['messages'])]}

## Tab 7
graph=StateGraph(State)

## node
graph.add_node("SuperBot",superbot)
## Edges

graph.add_edge(START,"SuperBot")
graph.add_edge("SuperBot",END)


graph_builder=graph.compile(checkpointer=memory)


## Display
from IPython.display import Image, display
display(Image(graph_builder.get_graph().draw_mermaid_png()))

## Tab 8
## Invocation

config = {"configurable": {"thread_id": "1"}}

graph_builder.invoke({'messages':"Hi,My name is Krish And I like cricket"},config)

# Streaming
# Methods: .stream() and astream()

# These methods are sync and async methods for streaming back results.
# Additional parameters in streaming modes for graph state

# values : This streams the full state of the graph after each node is called.
# updates : This streams updates to the state of the graph after each node is called.

## Tab 9
# Streaming The Responses With Stream Method
# Create a thread
config = {"configurable": {"thread_id": "3"}}

for chunk in graph_builder.stream({'messages':"Hi,My name is Krish And I like cricket"},config,stream_mode="updates"):
    print(chunk)

## Tab 10
for chunk in graph_builder.stream({'messages':"I also like football"},config,stream_mode="values"):
    print(chunk)

## Tab 11
for chunk in graph_builder.stream({'messages':"I also like football "},config,stream_mode="updates"):
    print(chunk)

## Tab 12
for chunk in graph_builder.stream({'messages':"I Love sports "},config,stream_mode="values"):
    print(chunk)

# Streaming The Responses With astream Method
# Streaming tokens We often want to stream more than graph state.

# In particular, with chat model calls it is common to stream the tokens as they are generated.

# We can do this using the .astream_events method, which streams back events as they happen inside nodes!

# Each event is a dict with a few keys:

# event: This is the type of event that is being emitted.
# name: This is the name of event.
# data: This is the data associated with the event.
# metadata: Containslanggraph_node, the node emitting the event.    

## Tab 13
config = {"configurable": {"thread_id": "3"}}

async for event in graph_builder.astream_events({"messages":["Hi My name is Krish and I like to play cricket"]},config,version="v2"):
    print(event)

    