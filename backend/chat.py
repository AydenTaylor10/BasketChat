import os
import json
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

#processes message for handeling in sports_api
def chat_process(message: str) -> dict:
    
    #scan message for nba names
    process_msg = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=100,
                                messages=[{"role": "user", "content": f"""Extract any NBA player name and team name from this message. Respond ONLY with a JSON object, no explanation, no markdown:
{{"player": "name or null", "team": "name or null"}} {message}"""}])
    return json.loads(process_msg.content[0].text.strip())

