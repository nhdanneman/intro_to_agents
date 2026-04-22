'''
Here is a research agent.
It features a server-side tool that we declare, but Anthropic executes.
'''

import anthropic
import os
import sys

# source your anthropic API key from an environment variable on your machine
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_KEY"])

# Server-side tool: Anthropic runs this, not our machine
# Don't need to define and describe, just declare.
tools = [
    {"type": "web_search_20260209", "name": "web_search"}
]

# There's no tool implementation section
# We are just pointing at a tool Anthropic will run

# System prompt: tell the agent what it is and how to act
system = (
    "You are a research assistant. Search the web from multiple angles "
    "to find current, accurate information. Cite your sources."
)

def research(question: str) -> str:
    # storage, much like before
    messages = [{"role": "user", "content": question}]
    print(f"Question: {question}\n")

    while True:
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens = 4096,
            system=system,
            tools=tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        for block in response.content:
            if hasattr(block, "type") and block.type == "server_tool_use":
                query = block.input.get("query", "") if isinstance(block.input, dict) else ""
                print(f"[Searching] {query}")

        if response.stop_reason == "end_turn":
            text_blocks = [b.text for b in response.content if b.type == "text"]
            # This return pulls together all the returned text of the summary.
            return "\n\n".join(text_blocks) if text_blocks else ""

        # pause_turn = server hit its iteration limit; max_tokens = response was cut off.
        # Either way, append a user message — the model forbids consecutive assistant turns. Just a gotcha.
        messages.append({"role": "user", "content": "Please continue."})
        continue
    

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input ("Research question: ")
    print(f"\n{research(question)}")


# usage hint
# python 4_Research_Agent.py "upsets in march madness 2026"
