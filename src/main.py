from apimodel import APIModel
from agents.start import Start

if __name__ == "__main__":
    api_key = 'sk-xxx'
    api_url = 'https://api.v3.cm/'

    chat_model = "gpt-4.1-mini"

    start_agent = Start(api_key, api_url, chat_model)

    # 3. 开始对话
    print("Agent:", start_agent.agent_say(None))
    user_input = None
    while not start_agent.check_ready(user_input):
        user_input = input("You: ")
        reply = start_agent.converse(user_input)
        print("Agent:", reply)

    # 4. 总结
    print("\n--- Summary ---")
    summary = start_agent.summarize()
    print(summary)
