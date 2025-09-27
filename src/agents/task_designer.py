# agents/task_designer.py

import json
from ..apimodel import APIModel

class TaskDesignAgent:
    """
    Designs a suitable drawing task for the user based on initial information.
    """
    def __init__(self, api_key, api_url, model, user_summary: dict):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.llm = APIModel(self.api_key, self.api_url, self.model)
        self.user_summary = user_summary
        self.task_prompt = None

    def generate_task(self) -> str:
        """
        Generates a drawing task instruction based on user's personality and requirements.
        """
        # Safely extract personality and requirement from the summary
        personality = self.user_summary.get("personality", "not specified")
        requirement = self.user_summary.get("requirement", "not specified")

        prompt = (
            "You are an art therapist designing a drawing task for a user.\n"
            "Your goal is to propose a task that is gentle, non-threatening, and relevant to the user's needs.\n"
            "Here is a summary of the user:\n"
            f"- Personality/Communication Style: {personality}\n"
            f"- Stated Goal/Requirement: {requirement}\n\n"
            "Based on this information, choose one type of drawing task:\n"
            "1.  **Free Drawing:** If the user is hesitant, shy, or their goal is simply 'relaxation'. This is the safest option.\n"
            "2.  **Thematic Drawing:** If the user has a specific goal (e.g., 'relieve stress', 'understand my emotions'). The theme should relate to their goal.\n"
            "3.  **Symbolic Drawing:** If the user is more expressive and their goal is abstract (e.g., 'gain self-understanding'). Suggest drawing a symbol for their feelings.\n\n"
            "Now, generate a short, encouraging instruction for the user. Start by acknowledging their goal, then present the task clearly. "
            "Keep it to one or two sentences.\n"
            "Example for 'relieve stress': 'Thank you for sharing that. To help with releasing some stress, how about you try drawing a place where you feel completely safe and calm?'\n"
            "Example for 'relaxation': 'That's a great goal. Let's start with something simple. Just take a piece of paper and let your hand move freely with any color you like. There's no right or wrong way to do it.'"
        )
        
        task_instruction = self.llm.chat(prompt=prompt, temperature=0.8, max_tokens=512)
        self.task_prompt = task_instruction
        return self.task_prompt