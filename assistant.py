"""
In this lab, we're going to use the wonderful Gradio package for building quick UIs,
and we're also going to use the popular PyPDF PDF reader. You can get guides to these packages by asking
ChatGPT or Claude, and you find all open-source packages on the repository https://pypi.org
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr

from constants import AI

load_dotenv(override=True)
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_URL = AI["PERPLEXITY"]["BASE_URL"]
PERPLEXITY_MODEL = AI["PERPLEXITY"]["MODEL"]

openai = OpenAI(api_key=PERPLEXITY_KEY, base_url=PERPLEXITY_URL)

reader = PdfReader("me/profile.pdf")
profile = ""

for page in reader.pages:
    profile += page.extract_text()

# print(profile)

with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

with open("me/personal.txt", "r", encoding="utf-8") as f:
    personal = f.read()

with open("me/instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

name = "Sudeep Pirangi"
assistant = "Babu"

system_prompt = f"Your name is {assistant}. You are acting as {name}'s assistant and he is your boss. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile and personal life which you can use to answer questions. \
{instructions}. If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{profile}\n\n## Personal Life:\n{personal}\n\n"
system_prompt += f"With this context, please chat with the user staying in your character as {assistant} who is {name}'s assistant."


def chat(message, history):
    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": message}]
    )
    response = openai.chat.completions.create(model=PERPLEXITY_MODEL, messages=messages)
    return response.choices[0].message.content


gr.ChatInterface(chat, type="messages").launch()
