# agents/questioner.py

from ..apimodel import APIModel

class ExploratoryQuestioningAgent:
    """
    Asks open-ended questions based on the artwork analysis to guide user narration.
    """
    def __init__(self, api_key, api_url, model):
        self.llm = APIModel(api_key, api_url, model)
        
    def ask(self, analysis_result: str, conversation_history: str) -> str:
        """
        Generates a single, open-ended question.

        Args:
            analysis_result: The analysis text from the WorksAnalysisAgent.
            conversation_history: The transcript of the conversation so far.

        Returns:
            A single question as a string.
        """
        prompt = (
            "You are an art therapist. Your role is to ask a gentle, open-ended question to help a user explore their artwork and feelings. "
            "You have the initial analysis of their artwork and the conversation history.\n\n"
            "**Analysis of the Artwork:**\n"
            f"{analysis_result}\n\n"
            "**Conversation History:**\n"
            f"{conversation_history}\n\n"
            "**Your Task:**\n"
            "Based on the analysis and avoiding questions already asked, formulate ONE insightful, open-ended question. "
            "Focus on a specific part of the analysis (a color, a shape, a symbol).\n"
            "Do NOT ask multiple questions. Do NOT make statements. Just ask the question.\n"
            "Good examples: 'What does that empty space on the left mean to you?', 'Can you tell me more about the story behind that small figure?', 'How did it feel to use the color red in this way?'"
        )
        
        question = self.llm.chat(prompt=prompt, temperature=0.8, max_tokens=256)
        return question