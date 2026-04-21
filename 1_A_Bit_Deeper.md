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

