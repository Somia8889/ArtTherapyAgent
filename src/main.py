# from .apimodel import APIModel
# from .agents.start import Start

# if __name__ == "__main__":
#     api_key = 'sh xxx'
#     api_url = 'https://api.v3.cm/v1'

#     # chat_model = "gpt-4.1-mini"
#     chat_model = "gpt-4.1-nano"

#     start_agent = Start(api_key, api_url, chat_model)

#     # 3. 开始对话
#     print("Agent:", start_agent.agent_say(None))
#     user_input = None
#     while not start_agent.check_ready(user_input):
#         user_input = input("You: ")
#         reply = start_agent.converse(user_input)
#         print("Agent:", reply)

#     # 4. 总结
#     print("\n--- Summary ---")
#     summary = start_agent.summarize()
#     print(summary)

# main.py
import json
from .apimodel import APIModel

# Import all agents
from .agents.start import Start
from .agents.task_designer import TaskDesignAgent
from .agents.works_analyzer import WorksAnalysisAgent
from .agents.questioner import ExploratoryQuestioningAgent
from .agents.emotion_analyzer import EmotionAnalysisAgent
from .agents.suggester import SuggestionAgent

class AgentState:
    """Defines the states of the therapy session."""
    START = 1
    TASK_DESIGN = 2
    ANALYSIS = 3
    QUESTIONING = 4
    SUGGESTION = 5
    END = 6

def print_agent_reply(message: str):
    """Utility function for formatted agent output."""
    print(f"\n🎨 Agent: {message}")

def get_user_input() -> str:
    """Utility function for formatted user input."""
    return input("👤 You: ")

if __name__ == "__main__":
    api_key = 'sk-xxxxx' # 请替换为你的 API Key
    api_url = 'https://api.v3.cm/v1' # 请替换为你的 API URL
    chat_model = "gpt-4.1-nano"

    # --- Session Context ---
    # This dictionary holds all information for the entire session
    session_context = {
        "full_transcript": [],
        "user_summary": None,
        "task_instruction": None,
        "analysis_result": None,
        "emotions": [],
    }

    current_state = AgentState.START

    # --- Main State Machine Loop ---
    while current_state != AgentState.END:

        # --- Phase 1: Relationship Building ---
        if current_state == AgentState.START:
            print("--- Phase 1: Relationship Building ---")
            agent = Start(api_key, api_url, chat_model)
            
            reply = agent.agent_say(None)
            print_agent_reply(reply)
            session_context["full_transcript"].append(f"Agent: {reply}")

            while True:
                user_input = get_user_input()
                session_context["full_transcript"].append(f"You: {user_input}")
                
                if agent.check_ready(user_input):
                    reply = agent.converse(user_input) # Get final reply before breaking
                    print_agent_reply(reply)
                    session_context["full_transcript"].append(f"Agent: {reply}")
                    break
                
                reply = agent.converse(user_input)
                print_agent_reply(reply)
                # The converse method already appends to the agent's internal transcript,
                # but we need it in the global context too.
                session_context["full_transcript"][-1] = f"You: {user_input}" # Overwrite last user input to avoid duplication
                session_context["full_transcript"].append(f"Agent: {reply}")

            summary_str = agent.summarize()
            session_context["user_summary"] = json.loads(summary_str)
            print(f"[Summary Generated: {session_context['user_summary']}]")
            current_state = AgentState.TASK_DESIGN

        # --- Phase 2: Task Design ---
        elif current_state == AgentState.TASK_DESIGN:
            print("\n--- Phase 2: Task Design ---")
            agent = TaskDesignAgent(api_key, api_url, chat_model, session_context["user_summary"])
            task = agent.generate_task()
            session_context["task_instruction"] = task
            print_agent_reply(task)
            session_context["full_transcript"].append(f"Agent: {task}")
            current_state = AgentState.ANALYSIS

        # --- Phase 3: Artwork Analysis ---
        elif current_state == AgentState.ANALYSIS:
            print("\n--- Phase 3: Artwork Analysis ---")
            print_agent_reply("Please take your time with the drawing. When you're ready, you can either describe it to me or provide a local image path (e.g., C:/Users/Me/drawing.png).")
            user_drawing_input = get_user_input()
            session_context["full_transcript"].append(f"You: {user_drawing_input}")
            
            agent = WorksAnalysisAgent(api_key, api_url, chat_model)
            analysis = agent.analyze(user_drawing_input, session_context["task_instruction"])
            session_context["analysis_result"] = analysis
            print_agent_reply(analysis)
            session_context["full_transcript"].append(f"Agent: {analysis}")
            current_state = AgentState.QUESTIONING

        # --- Phase 4: Exploratory Questioning (Loop) ---
        elif current_state == AgentState.QUESTIONING:
            print("\n--- Phase 4: Deepening Exploration ---")
            # This is a sub-loop for conversation
            while True:
                history_str = "\n".join(session_context["full_transcript"])
                
                # First, check if we should exit the loop and give a suggestion
                router = EmotionAnalysisAgent(api_key, api_url, chat_model)
                route_decision = router.analyze_and_route(history_str)
                session_context["emotions"] = route_decision["emotions"]
                print(f"[Emotion Analysis: {route_decision}]")

                next_step = route_decision.get("next_step")
                
                if next_step == "give_suggestion":
                    current_state = AgentState.SUGGESTION
                    break # Exit the questioning sub-loop

                elif next_step == "new_drawing":
                    print_agent_reply("It seems we've explored this drawing fully. To look at things from a different angle, let's start a new one.")
                    # 清理上一个画作的上下文，为新画作做准备
                    session_context["analysis_result"] = None
                    current_state = AgentState.TASK_DESIGN # 切换状态回到任务设计
                    break # Exit the questioning sub-loop
                
                # 默认行为: continue_questioning
                else: 
                    questioner = ExploratoryQuestioningAgent(api_key, api_url, chat_model)
                    question = questioner.ask(session_context["analysis_result"], history_str)
                    print_agent_reply(question)
                    session_context["full_transcript"].append(f"Agent: {question}")
                    
                    user_answer = get_user_input()
                    session_context["full_transcript"].append(f"You: {user_answer}")

        # --- Phase 5: Suggestion & Closing ---
        elif current_state == AgentState.SUGGESTION:
            print("\n--- Phase 5: Insight & Suggestion ---")
            history_str = "\n".join(session_context["full_transcript"])
            agent = SuggestionAgent(api_key, api_url, chat_model)
            
            suggestion = agent.suggest(history_str, session_context["emotions"])
            print_agent_reply(suggestion)
            session_context["full_transcript"].append(f"Agent: {suggestion}")

            print_agent_reply("How does that sound to you?")
            user_feedback = get_user_input()
            
            if agent.check_feedback(user_feedback):
                print_agent_reply("I'm glad to hear that. Thank you for sharing your time and creativity with me today. Take care.")
            else:
                # In a more complex system, this could loop back to questioning
                print_agent_reply("Thank you for your feedback. It's important that we find what works for you. Let's hold that thought for now. Thank you for your openness today.")
            
            current_state = AgentState.END

    print("\n--- Session Ended ---")