from dotenv import load_dotenv
load_dotenv()

from llm import ask_llm
from sports_api import get_player_stats, get_team_stats
from prompt_builder import build_prompt

def main():

    title = "BasketChat - Your Own Basketball Betting Advisor!"
    print(title)
    print("Hello, \n How can I assist your basketball inquiries?")

    while True:
        user_input = ("Ask anything ('exit' to end session): ").strip()

        if user_input.lower is "exit":
            break

        #build prompt from user input
        stats = ""
        stats += get_player_stats(user_input)
        stats += get_team_stats(user_input)

        AI_prompt = build_prompt(user_input, stats)
        AI_response = ask_llm(AI_prompt)

        print(f"Advice: {AI_response}")

if __name__ == "__main__":
    main()
