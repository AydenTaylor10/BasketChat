import os
from anthropic import Anthropic

#key required***
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

AIPrompt = """You are a basketball analytics assistant that helps users think through 
sports betting decisions. You provide data-driven insights based on player stats, team 
performance, matchups, and trends.

Always be clear that your insights are for informational and entertainment purposes only, 
and are not financial advice. Be analytical, balanced, and highlight both supporting and 
opposing factors for any bet. Never tell the user to definitively place or avoid a bet."""

def ask_llm(prompt: str) -> str:
    #Send a prompt to Claude and return the response
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=AIPrompt,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text
