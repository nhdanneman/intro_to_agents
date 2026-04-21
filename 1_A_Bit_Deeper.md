### The Central Architecture: A Growing History/Conversation

An agent isn't a special object or type. Rather, it's a list of messages that keeps growing, plus a loop that decides when to stop.

Every message has a role (`system`, `user`, `assistant`, `tool`) and content. The model sees the entire list on every call. The "memory" between steps is literally just this list.

```
messages = [
    {role: "systems",      content: "You are a research assistant..."},
    {role: "user",         content: "What were GDP growth rates in SEA in 2023?"},
    {role: "assistant",    content: <tool_call: web_search("GDP growth SEA 2023")>},
    {role: "tool",         content: "Thailand: 1.9%, Vietnam: 5.0%..."},
    {role: "assistant",    content: "Based on the data..."}
]
```

### How Tool Calling Works

The model never executes anything. Rather, it generates text that desscribes an action, and the surrounding agentic scaffolding executes it. 

1. You register tools by giving the model their signatures: name, description, parameters with types
2. The model responds wtih either: plain text (done) or a structured tool-call request
3. Your code detects the tool-call, runs the actual function, appends the result as a `tool` message
4. Call the model again with teh updated list

### The Loop, Again

Grokking this is really central. Agents are loops.

```
initialize messages with system prompt + user request

loop:
    response = call_model(messages)

    if response is a final answer:
        return response
    
    if response contains tool calls:
        for each tool_call in response:
            result = execute(tool_call)
            append result to messages
        continue loop
```

Every agentic framework is a (potentially very sophisticated!) variation on this loop.

### System Prompt: The Main Control Surface for the Agent

The system prompt sets:
- Identify and goal: what this agent is for
- Tool inventory: what tools exist and when to use each
- Reasoning style: should it think step by step?
- Behavioral constraints: what is should and should not do
- Output format: how final answers should be structured

Poorly written systems prompts are a core reason for agents to behave erratically.

### The Stopping Problem

Agents need some method for knowing when they are done looping. There are three common options, often combined.

1. Model decides: returns a final answer instead of a tool call
2. Max steps: hard cap on loop iterations (safety first!)
3. External check: your code inspects the response for specific structure

A common failure mode is unnecessary loop iterations. Agents re-verifying things again, or fetching data via tool-calls it already fetched previously. These are a sure sign of poorly-constructed stopping methods.

