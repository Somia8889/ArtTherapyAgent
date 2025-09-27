import json
from ..apimodel import APIModel

from typing import Dict, List, Optional
from langchain.prompts import ChatPromptTemplate


class Start:
    """
    Relationship-building Agent for Art Therapy System
    """

    def __init__(self, api_key, api_url, model):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.llm = APIModel(self.api_key, self.api_url, self.model)
        self.transcript = []
        self.trust_established = False
        self.requirement = None
        self.personality = None

    def agent_say(self, user_input):
        history_text = "\n".join(
            [f"{turn['role']}: {turn['text']}" for turn in self.transcript]
        )

        if not user_input:  # first message
            prompt = (
                "You are an art therapy assistant. Your goal is to build trust with the user.\n"
                "Start with a short, warm greeting. Emphasize that art therapy is not about artistic skills, "
                "but about expressing emotions and experiences.\n"
                "Then gently ask the user: 'What would you like to achieve through this session?'\n"
                "You may provide some examples to guide them, such as: "
                "relieving stress, exploring emotions, gaining self-understanding, or simply relaxing."
            )
            reply = self.llm.chat(prompt=prompt, temperature=0.7, max_tokens=512)
            self.transcript.append({"role": "agent", "text": reply})
        else:
            prompt = (
                f"Here is the conversation so far:\n{history_text}\n\n"
                "Continue the conversation in a short, warm, empathetic tone.\n"
                "Goals:\n"
                "1. Help the user feel safe and willing to share.\n"
                "2. Encourage the user to express their needs or goals.\n"
                "3. If the user still seems unsure, reassure them.\n"
                "4. If their needs are clear, you may suggest moving forward.\n"
            )
            reply = self.llm.chat(prompt=prompt, temperature=0.7, max_tokens=512)

        return reply

    def converse(self, user_input):
        self.transcript.append({"role": "user", "text": user_input})
        reply = self.agent_say(user_input)
        self.transcript.append({"role": "agent", "text": reply})
        return reply

    # def check_ready(self, user_input: str) -> bool:
    #     """
    #     Use LLM to decide if the user is ready to begin drawing
    #     """
    #     prompt = (
    #         "You are analyzing a user's response in an art therapy session.\n"
    #         "Determine if the user seems ready to begin a drawing activity.\n"
    #         "Criteria for readiness: The user expresses trust, willingness, or a clear goal for the session.\n\n"
    #         f"User input: \"{user_input}\"\n\n"
    #         "Return only one word: true or false."
    #     )

    #     response = self.llm.chat(prompt=prompt, temperature=0.7, max_tokens=32).strip().lower()

    #     if "true" in response:
    #         self.trust_established = True
    #         return True
    #     else:
    #         self.trust_established = False
    #         return False

    # 建议的 check_ready 优化
    def check_ready(self, user_input: str) -> bool:
        """
        Use LLM to decide if the user is ready to begin drawing.
        """
        if not user_input: # Handle the initial call where user_input is None
            return False

        prompt = (
            "You are an analyzer for an art therapy session. Your task is to determine if the user is ready to start a drawing activity based on their last message.\n"
            "Criteria for readiness: The user expresses a clear goal, shows willingness, or gives explicit consent to proceed (e.g., 'I'm ready', 'Okay', 'Let's start').\n\n"
            f"User's last message: \"{user_input}\"\n\n"
            "Based on this, should the session proceed to the drawing phase? Respond with a single JSON object containing one key 'ready' with a boolean value (true or false)."
            "Example: {\"ready\": true}"
        )

        # In a real scenario, you would add a loop or error handling for JSON parsing
        try:
            response_str = self.llm.chat(prompt=prompt, temperature=0.0, max_tokens=32).strip()
            response_json = json.loads(response_str)
            
            if response_json.get("ready", False):
                self.trust_established = True
                return True
            else:
                self.trust_established = False
                return False
        except (json.JSONDecodeError, AttributeError):
            # If parsing fails, fall back to a safer default (not ready)
            self.trust_established = False
            return False

    def summarize(self):
        history_text = "\n".join(
            [f"{turn['role']}: {turn['text']}" for turn in self.transcript]
        )

        prompt = (
            "Read the following conversation between a therapist and a user.\n"
            "Provide a JSON summary with two fields:\n"
            "- personality: a short description of the user's personality or communication style\n"
            "- requirement: the user's need or goal for art therapy\n\n"
            f"Conversation:\n{history_text}\n\n"
            # "Return strictly in JSON format."
            "Respond with ONLY the JSON object and nothing else. Example response: {\"personality\": \"direct\", \"requirement\": \"relieve stress\"}"
        )

        return self.llm.chat(prompt=prompt, temperature=0.7, max_tokens=256)
