from langchain_openai import ChatOpenAI
import base64
import os


class APIModel:

    def __init__(self, api_key, api_url, model):
        if api_url:
            self.llm = ChatOpenAI(model=model, api_key=api_key, base_url=api_url)
        else:
            self.llm = ChatOpenAI(model=model, api_key=api_key)

    def chat(self, prompt, temperature, max_tokens):
        return self.llm.with_config(
            {"configurable": {"temperature": temperature, "max_tokens": max_tokens}}
        ).invoke(prompt).content

    def understand(self, prompt, image, temperature, max_tokens):
        if os.path.exists(image):
            with open(image, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            image_input = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
        else:
            # assume it's a remote url
            image_input = {"type": "image_url", "image_url": {"url": image}}

        inputs = [
            {"type": "text", "text": prompt},
            image_input,
        ]

        response = self.llm.with_config(
            {"configurable": {"temperature": temperature, "max_tokens": max_tokens}}
        ).invoke(inputs)

        return response.content
