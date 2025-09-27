# agents/suggester.py

from ..apimodel import APIModel

class SuggestionAgent:
    """
    Provides gentle, actionable suggestions or insights based on the session.
    """
    def __init__(self, api_key, api_url, model):
        self.llm = APIModel(api_key, api_url, model)

    def suggest(self, conversation_history: str, emotions: list) -> str:
        """
        Generates a concluding suggestion.

        Args:
            conversation_history: The full transcript of the session.
            emotions: The list of identified emotions from the EmotionAnalysisAgent.

        Returns:
            A supportive and constructive suggestion.
        """
        emotions_str = ", ".join(emotions)
        prompt = (
            "You are an art therapist providing a concluding thought for a session. Your goal is to empower the user, not to solve their problems. "
            "Your tone should be warm, validating, and encouraging.\n\n"
            "**Identified Emotions:** {emotions_str}\n"
            "**Conversation Transcript:**\n"
            f"{conversation_history}\n\n"
            "**Your Task:**\n"
            "Based on the entire conversation, provide a brief, actionable, and gentle suggestion. Focus on one of three areas:\n"
            "1.  **Emotional Acknowledgment:** Validate the user's feelings. (e.g., 'It's completely understandable to feel {emotion}. Your drawing powerfully expressed that.')\n"
            "2.  **Perspective Shift:** Offer a new way to think about their situation. (e.g., 'I wonder what it would be like to add a source of light to the dark cloud in your drawing, perhaps in a future session or just in your mind.')\n"
            "3.  **Mindful Practice:** Suggest a small, simple daily practice. (e.g., 'When you feel that sense of being overwhelmed, perhaps you could take a moment to sketch a small symbol of safety, just as you did with the house today.')\n\n"
            "Combine these elements into a short, supportive paragraph. End by thanking the user for their trust and openness."
        )
        
        suggestion = self.llm.chat(prompt=prompt, temperature=0.8, max_tokens=1024)
        return suggestion
    
    def check_feedback(self, user_feedback: str) -> bool:
        """
        Checks if the user's feedback on the suggestion is positive.
        """
        prompt = (
            "Analyze the user's feedback to a suggestion. "
            f"User feedback: '{user_feedback}'. "
            "If the sentiment is positive, appreciative, or indicates the suggestion was helpful (e.g., 'Thank you', 'That helps', 'I'll try that'), return 'true'. "
            "Otherwise, return 'false'."
        )
        response = self.llm.chat(prompt=prompt, temperature=0.0, max_tokens=10).strip().lower()
        return "true" in response