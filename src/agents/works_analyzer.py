# agents/works_analyzer.py

import os
from ..apimodel import APIModel

class WorksAnalysisAgent:
    """
    Analyzes the user's artwork (image or description).
    """
    def __init__(self, api_key, api_url, model):
        self.llm = APIModel(api_key, api_url, model)

    def analyze(self, user_input: str, task_instruction: str) -> str:
        """
        Analyzes the artwork and returns a textual summary of observations.
        
        Args:
            user_input: The user's description of the drawing or a file path to the image.
            task_instruction: The original task given to the user for context.

        Returns:
            A string containing the analysis.
        """
        
        prompt = (
            "You are an art therapist providing an initial analysis of a user's artwork. Your tone should be gentle, curious, and non-judgmental. "
            "Your goal is to open up a conversation, not to provide a definitive diagnosis.\n\n"
            "Here was the instruction given to the user:\n"
            f"'{task_instruction}'\n\n"
            "Based on the user's artwork, provide observations. Structure your analysis into two parts:\n"
            "1.  **Objective Observations:** Describe what you see in terms of colors, shapes, composition, objects, and use of space. (e.g., 'I notice a small house in the corner and a large, dark cloud covering most of the sky.')\n"
            "2.  **Potential Symbolic Meanings:** Gently suggest possible feelings or ideas that these elements *might* represent, using tentative language. (e.g., 'Sometimes, houses can represent a sense of self or security. The large cloud might suggest a feeling of being overwhelmed.')\n\n"
            "Keep the analysis concise (3-5 sentences) to encourage the user to share their own perspective."
        )

        # 检查输入是图片路径还是文本描述
        # (这是一个简化的检查，实际应用中可能需要更复杂的逻辑)
        if os.path.exists(user_input) and user_input.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("[Analyzing image from path...]")
            analysis = self.llm.understand(prompt=prompt, image=user_input, temperature=0.7, max_tokens=1024)
        else:
            print("[Analyzing text description...]")
            # 如果是文本，将其作为分析内容
            full_prompt = f"{prompt}\n\nHere is the user's description of their artwork:\n\"{user_input}\""
            analysis = self.llm.chat(prompt=full_prompt, temperature=0.7, max_tokens=1024)
            
        return analysis