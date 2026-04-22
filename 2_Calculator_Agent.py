'''
Here is the Hello World of agents. 
Just sufficient to express most of the key elements.
It is a calculator, that takes in word problems and solves them.
'''

import anthropic
import math
import os
import sys

# source your anthropic API key from an environment variable on your machine
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_KEY"])

# Tool definition: what the model can call
# Each tool in the list has a name, textual description for reasoning, and input specification
tools = [
    {
        "name": "calculator",
        "description": (
            "Evaluate a mathematical expression. Use this for any numeric "
            "computation. Supports Python math syntax and the math module."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "e.g. 'math.pi * 7.3**2' or 'round(4/3 *. math.pi * 7.3**3, 4)'",
                }
            },
            "required": ["expression"],
        },
    }
]

# Tool implementation...what actually runs
def run_calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# System prompt: tell the agent what it is and how to act
system = (
    "You are a math assistant. Use the calculator tool for each computation. "
    "Show your reasoning step by step, then state a clear final answer."
)

# Format all the components into something callable

def run_agent(question: str) -> str:
    # this is the agent's tiny, in-house memory sytem
    # gets extended each time
    messages = [{"role": "user", "content": question}]

    # Here is a backstop for loops that don't reach a graceful stopping point
    for _ in range(10):
        # Send the system prompt, tool descriptions, and messages to an LLM
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens = 1024,
            system=system,
            tools=tools,
            messages=messages,
        )
        
        # Add the response to the memory
        messages.append({"role": "assistant", "content": response.content})

        # one case: we are done
        if response.stop_reason == "end_turn":
            return next(b.text for b in response.content if b.type == "text")
        
        # another case: a tool is called
        if response.stop_reason == "tool_use":
            tool_results = [] # set up storage for tool results
            for block in response.content:
                if block.type == "tool_use": # note, we don't have to reason over which tool to call; we only have one for now
                    result = run_calculator(block.input["expression"])
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            # add tool-call results to the message list...
            messages.append({"role": "user", "content": tool_results})
                    
if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    print(run_agent(question))

# usage hint
# python 2_Calculator_Agent.py "What is the surface area of a sphere with radius 5?"


