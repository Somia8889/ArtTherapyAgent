# agents/emotion_analyzer.py

import json
from ..apimodel import APIModel

class EmotionAnalysisAgent:
    """
    Analyzes the user's narrative to identify emotions and decide the next step.
    This acts as a router.
    """
    def __init__(self, api_key, api_url, model):
        self.llm = APIModel(api_key, api_url, model)

    def analyze_and_route(self, conversation_history: str) -> dict:
        """
        Analyzes the conversation and returns a structured decision.

        Args:
            conversation_history: The full transcript of the session.

        Returns:
            A dictionary with 'emotions' and 'next_step'.
        """
        prompt = (
            "You are a psychological analyst and router in an art therapy session. "
            "Your task is to read the entire conversation transcript and determine the user's emotional state and the conversational depth.\n\n"
            "**Conversation Transcript:**\n"
            f"{conversation_history}\n\n"
            "**Your Analysis & Decision:**\n"
            "1.  **Identify Emotions:** List the primary emotions expressed by the user (e.g., anxiety, joy, confusion, relief, sadness, ambivalence).\n"
            "2.  **Decide the Next Step:** Based on the depth of the user's self-exploration, choose one of the following actions:\n"
            "    - 'continue_questioning': If the user's story is still unfolding and more details could be explored.\n"
            "    - 'give_suggestion': If the user has expressed a clear emotional challenge or insight, and the conversation has reached a point where a concluding thought or gentle advice would be helpful.\n"
            "    - 'new_drawing': If the current topic seems exhausted or the user feels stuck, and a new creative task might be beneficial (use this sparingly).\n\n"
            "Provide your output in a strict JSON format with two keys: 'emotions' (a list of strings) and 'next_step' (a single string).\n"
            "Example: {\"emotions\": [\"anxious\", \"conflicted\"], \"next_step\": \"continue_questioning\"}"
        )

        # Loop to ensure valid JSON is returned
        for _ in range(3): # Try up to 3 times
            try:
                response_str = self.llm.chat(prompt=prompt, temperature=0.2, max_tokens=512)
                decision = json.loads(response_str)
                if "emotions" in decision and "next_step" in decision:
                    return decision
            except (json.JSONDecodeError, TypeError):
                continue # If parsing fails, retry
        
        # Fallback if JSON fails after retries
        return {"emotions": ["unknown"], "next_step": "continue_questioning"}