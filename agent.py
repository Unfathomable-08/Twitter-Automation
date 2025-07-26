from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain.memory import ConversationBufferMemory
import os
import json

load_dotenv()

def generateTweet():
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    model = InferenceClient(model="mistralai/Mixtral-8x7B-Instruct-v0.1", token=api_token)

    prompt = PromptTemplate(
        input_variables=[],
        template=(
            """
            You are a quiz generator for Arabic learners.

            Generate ONE multiple-choice quiz question and output it strictly as a **JSON array of one object** in the following format:

            [
            {{
                "question": "What does the word \\"___\\" mean?",
                "options": ["English Word", "English Word", "English Word", "English Word"]
            }}
            ]

            Rules:
            - The Arabic word must be a common noun (like an object, animal, or place).
            - All four options must be reasonable and distinct (not obvious).
            - Do NOT explain or translate anything.
            - DO NOT include any text outside the JSON array.
            """
        )
    )

    formatted_prompt = prompt.format()

    response = model.chat.completions.create(
        messages=[{"role": "user", "content": formatted_prompt}],
        max_tokens=100, 
        temperature=0.7
        )

    tweet = response.choices[0].message.content
    
    return tweet