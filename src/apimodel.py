# from langchain_openai import ChatOpenAI
# import base64
# import os


# class APIModel:

#     def __init__(self, api_key, api_url, model):
#         if api_url:
#             self.llm = ChatOpenAI(model=model, api_key=api_key, base_url=api_url)
#         else:
#             self.llm = ChatOpenAI(model=model, api_key=api_key)

#     def chat(self, prompt, temperature, max_tokens):
#         return self.llm.with_config(
#             {"configurable": {"temperature": temperature, "max_tokens": max_tokens}}
#         ).invoke(prompt).content

#     def understand(self, prompt, image, temperature, max_tokens):
#         if os.path.exists(image):
#             with open(image, "rb") as f:
#                 b64 = base64.b64encode(f.read()).decode("utf-8")
#             image_input = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
#         else:
#             # assume it's a remote url
#             image_input = {"type": "image_url", "image_url": {"url": image}}

#         inputs = [
#             {"type": "text", "text": prompt},
#             image_input,
#         ]

#         response = self.llm.with_config(
#             {"configurable": {"temperature": temperature, "max_tokens": max_tokens}}
#         ).invoke(inputs)

#         return response.content

# src/apimodel.py (修正版)

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage # <<<< 1. 引入 HumanMessage
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
            try:
                with open(image, "rb") as f:
                    b64_content = base64.b64encode(f.read()).decode("utf-8")
                image_url = f"data:image/png;base64,{b64_content}"
            except Exception as e:
                print(f"Error reading or encoding local image: {e}")
                return "I'm sorry, I had trouble reading the image file."
        else:
            # 假设是远程 URL
            image_url = image

        # <<<< 2. 构造符合 LangChain 格式的单一 HumanMessage
        # 将文本和图片都作为 content 列表的一部分
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                },
            ]
        )

        # <<<< 3. 调用 invoke 时传递这个单一的 message 对象
        response = self.llm.with_config(
            {"configurable": {"temperature": temperature, "max_tokens": max_tokens}}
        ).invoke([message])

        return response.content