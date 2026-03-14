from dotenv import load_dotenv
load_dotenv()

from chat import chat_process
from llm import ask_llm
from sports_api import get_player_stats, get_team_info, get_matchup
from prompt_builder import build_prompt

def main():

    title = "BasketChat - Your Own Basketball Betting Advisor!"
    print(title)
    print("Hello, \n How can I assist your basketball inquiries?")

    while True:
        user_input = input("Ask anything ('exit' to end session): ").strip()

        if user_input.lower() == "exit":
            break

        #build prompt from user input
        stats = ""
        names = chat_process(user_input)
        if names.get("player"):
            player_stats, player_team = get_player_stats(names["player"])
            stats += player_stats
            if player_team:
                stats += get_matchup(player_team)
        if names.get("team"):
            stats += get_team_info(names["team"])
            stats += get_matchup(names["team"])
        
        AI_prompt = build_prompt(user_input, stats)
        AI_response = ask_llm(AI_prompt)

        print(f"Advice: {AI_response}")

if __name__ == "__main__":
    main()
