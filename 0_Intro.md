### Fundamentals

A standard ML model is a function. You hand it inputs, it returns outputs, it's done. No memory of what happened before, no ability to affect the (local) world, no decisions about what to do next.

An agent is a model that runs in a loop. And, crucially, its ouptuts *change the inputs it receivews on the enxt iteration*. That feedback cycle is the crux of it.

### The Core Loop

Every agent cycles through:

1. **Observe** - percieve the current state of the world (text, tool outputs, memory, context)
2. **Reason** - decide what to do next
3. **Act** - take an action that changes the world
4. **Repeat or Stop** - the world's new state becomes the next observation

Think of it like an active exploration that never stops. The model isn't just predicting and quitting. Rather, it is deciding what needs to be generated next, then updating on the basis of that output (plus the previous outputs(s)).

### Tools Are How Agents Touch the World

On their own, LLMs are stateless text transformers...text in -> text out. Tools are what give them reach. A tool is any callable function: a web search, code executory, a database query, a file writer, and API call.

When an agent "uses a tool," it is generating structured text that a surrounding system interprets and executes. The reult comes back into context, and the agent reasons over it.

Architecturally, the key to understanding is that the smarts live in the model, and the agency lives in the scaffolding around it.

### Memory is an Underrated and Hard Problem

LLMs have a context window -- a fixed-size working memory. Agents exted this in various ways:

- **In-context memory**: the conversation/scratchpad itself
- **External retrieval**: vector stores, databases
- **State written to the world**: files, databases the agents modifies

Each memory types has different precision/recall tradeoffs. The hard part is that the agent must decide when and how and what to store.

### Planning and Combinatorial Explosion

Single-step agents are reliable but weak. Multi-step agents are powerful, but fragile.

It each step has, say, a 90% success probability, then five sequntial steps gives you ~59% end-to-end success. By ten steps you're down to ~35%. This is why planning strategies matter. ReAct, chain-of-thought with tool use, tree-of-thought, and others are essentially different strategies for managing this combinatorial explosion.

### Where Agents Make Sense

Agents are worth the complexity in general when tasks are:

- Long Horizon: too many steps for a single model call
- Contigent: later sptes depend on what earlier steps discovered
- World-touching: requires reading/writing to external systems

### A Note on Intelligence

Agents aren't smarter than teh underlying model. They're the same model, called repeatedly, with more context, plus tool access. Model quality compounds across steps as noted above. A model that's 80% reliable at each step versus 90% makes a large difference by step 10.