'''
Here is the Hello World of agents. 
Just sufficient to express most of the key elements.
It is a calculator, that takes in word problems and solves them.
'''

import anthropic
import math
import sys

client = anthropic.Anthropic()

# Tool definition: what the model can call
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

# Format all this into something callable

def run_agent(question: str) -> str:
    # this is the agent's tiny, in-house memory sytem
    # gets extended each time
    messages = [{"role": "user", "content": question}]
    while True:
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens = 1024,
            system=system,
            tools=tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason == "end_turn":
            return next(b.text for b in respponse.content if b.type == "Test")
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = run_calculator(block.input["expression"])
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use"id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})
                    
if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    print(run_agent(question))




