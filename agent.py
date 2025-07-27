from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain.memory import ConversationBufferMemory
import os
import json
import re

load_dotenv()

# Helper Function To Maintain Memory In Non Continouns Environment
USED_QUESTIONS_FILE = "used_questions.json"

def load_used_questions():
    if not os.path.exists(USED_QUESTIONS_FILE):
        return set()
    with open(USED_QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_used_questions(used_questions):
    with open(USED_QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(used_questions), f, ensure_ascii=False, indent=2)

# Mian Function
def generateTweet():
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    model = InferenceClient(model="mistralai/Mixtral-8x7B-Instruct-v0.1", token=api_token)

    prompt = PromptTemplate(
        input_variables=["used_words_str"],
        template=(
            """
            You are a quiz generator for Arabic learners.

            Avoid using any of the following Arabic words: {used_words_str}

            Generate ONE multiple-choice quiz question and output it strictly as a **JSON array of one object** in the following format:

            [
            {{
                "question": "What does the word \\"___\\" mean?",
                "options": ["English Word", "English Word", "English Word", "English Word"]
            }}
            ]

            Rules:
            - The Arabic word must be a noun or verb (like an object, animal, place or work).
            - All four options must be reasonable and distinct (not obvious).
            - The Arabic word should be intermediate level hard.
            - Do NOT explain or translate anything.
            - DO NOT include any text outside the JSON array.
            """
        )
    )

    used_words = load_used_questions()
    used_words_str = ", ".join(sorted(used_words)) if used_words else "None"

    formatted_prompt = prompt.format(used_words_str=used_words_str)

    response = model.chat.completions.create(
        messages=[{"role": "user", "content": formatted_prompt}],
        max_tokens=100,
        temperature=0.7
    )

    tweet = response.choices[0].message.content

    try:
        question_json = json.loads(tweet)
        question_text = question_json[0]["question"]

        # Extract the Arabic word using regex
        match = re.search(r'What does the word ["\'](.*?)["\'] mean\?', question_text)
        arabic_word = match.group(1).strip() if match else None

        if arabic_word:
            print(arabic_word)
            used_words.add(arabic_word)
            save_used_questions(used_words)
        else:
            print("Arabic word not found in question:", question_text)

    except Exception as e:
        print("Error parsing or saving:", e)

    return tweet