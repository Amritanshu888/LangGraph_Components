# Chain Using LangGraph
# In this section we will see how we can build a simple chain using Langgraph that uses 4 important concepts

# How to use chat messages as our graph state
# How to use chat models in graph nodes
# How to bind tools to our LLM in chat models
# How to execute the tools call in our graph nodes

## Tab 1
from dotenv import load_dotenv
load_dotenv()

import os
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

# How to use chat messages as our graph state
# Messages
# We can use messages which can be used to capture different roles within a conversation. LangChain has various message types including HumanMessage, AIMessage, SystemMessage and ToolMessage. These represent a message from the user, from chat model, for the chat model to instruct behavior, and from a tool call.

# Every message have these important components.

# content - content of the message
# name - Specify the name of author
# response_metadata - optionally, a dict of metadata (e.g., often populated by model provider for AIMessages)

## Tab 2
from langchain_core.messages import AIMessage,HumanMessage
from pprint import pprint

messages=[AIMessage(content=f"Please tell me how can I help",name="LLMModel")]
messages.append(HumanMessage(content=f"I want to learn coding",name="Krish"))
messages.append(AIMessage(content=f"Which programming language you want to learn",name="LLMModel"))
messages.append(HumanMessage(content=f"I want to learn python programming language",name="Krish"))

for message in messages:
    message.pretty_print()

## Tab 3
# Chat Models
# We can use the sequence of message as input with the chatmodels using LLM's and OPENAI.

from langchain_groq import ChatGroq
llm=ChatGroq(model="qwen-qwq-32b")
result=llm.invoke(messages)

## Tab 4
result.response_metadata

## Tab 5
# Tools
# Tools can be integrated with the LLM models to interact with external systems. External systems can be API's, third party tools.

# Whenever a query is asked the model can choose to call the tool and this query is based on the natural language input and this will return an output that matches the tool's schema

def add(a:int,b:int)-> int:
    """ Add a and b
    Args:
        a (int): first int
        b (int): second int

    Returns:
        int
    """
    return a+b

## Tab 6
llm

## Tab 7
### Binding tool with llm

llm_with_tools=llm.bind_tools([add])

tool_call=llm_with_tools.invoke([HumanMessage(content=f"What is 2 plus 2",name="Krish")])

## Tab 8
tool_call.tool_calls

## Tab 9
# Using messages as state
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage

class State(TypedDict):
    message:list[AnyMessage]

# Reducers
# Now, we have a minor problem!

# As we discussed, each node will return a new value for our state key messages.

# But, this new value will override the prior messages value.

# As our graph runs, we want to append messages to our messages state key.

# We can use reducer functions to address this.

# Reducers allow us to specify how state updates are performed.

# If no reducer function is specified, then it is assumed that updates to the key should override it as we saw before.

# But, to append messages, we can use the pre-built add_messages reducer.

# This ensures that any messages are appended to the existing list of messages.

# We simply need to annotate our messages key with the add_messages reducer function as metadata. 

## Tab 10
from langgraph.graph.message import add_messages
from typing import Annotated
class State(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

## Tab 11
# Reducers with add_messages
initial_messages=[AIMessage(content=f"Please tell me how can I help",name="LLMModel")]
initial_messages.append(HumanMessage(content=f"I want to learn coding",name="Krish"))
initial_messages

## Tab 12
ai_message=AIMessage(content=f"Which programming language you want to learn",name="LLMModel")
ai_message

## Tab 13
### Reducers add_messages is to append instead of override
add_messages(initial_messages,ai_message)

## Tab 14
## chatbot node functionality
def llm_tool(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

## Tab 15
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
builder=StateGraph(State)

builder.add_node("llm_tool",llm_tool)

builder.add_edge(START,"llm_tool")
builder.add_edge("llm_tool",END)

graph=builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

## Tab 16
## invocation

messages=graph.invoke({"messages":"What is 2 plus 2"})

for message in messages["messages"]:
    message.pretty_print()

## Tab 17
tools=[add]

## Tab 18
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


builder=StateGraph(State)

## Add nodes

builder.add_node("llm_tool",llm_tool)
builder.add_node("tools",ToolNode(tools))

## Add Edge
builder.add_edge(START,"llm_tool")
builder.add_conditional_edges(
    "llm_tool",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition
)
builder.add_edge("tools",END)


graph_builder = builder.compile()

## Tab 19
display(Image(graph.get_graph().draw_mermaid_png()))

## Tab 20
## invocation

messages=graph.invoke({"messages":"What is 2 plus 2"})

for message in messages["messages"]:
    message.pretty_print()

## Tab 21
messages=graph.invoke({"messages":"What Machine Learning"})

for message in messages["messages"]:
    message.pretty_print()
