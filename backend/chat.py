import os
import json
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

#processes message for handeling in sports_api
def chat_process(message: str) -> dict:
    
    #scan message for nba names
    process_msg = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=100,
                                messages=[{"role": "user", "content": f"Extract any nba player name or nba team name from the user's message: {message}"}])
    return json.loads(process_msg.content[0].text.strip())

