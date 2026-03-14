def build_prompt(user_message: str, stats_context: str) -> str:

    #builds a prompt
    if stats_context:
        f"""The user is asking about a basketball betting decision. 
Here is relevant stats data pulled from a live sports API:
 
{stats_context}
 
Using the stats above as context, answer the following question:
{user_message}"""
    
    else:
        return f"""The user is asking about a basketball betting decision.
No specific player or team stats were detected in their question, 
so answer using your general basketball knowledge.
 
Question: {user_message}"""