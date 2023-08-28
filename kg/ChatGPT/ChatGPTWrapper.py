import openai


class ChatGPTWrapper:
    def __init__(self):
        openai.api_key = ""

    def create_debunk(self, statement):
        querry = "Write a short debunk for: " + str(statement) + (". Do not repeat debunk or any other sections like "
                                                                  "introduction, just the text")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fact-checking journalist."},
                {"role": "user",
                 "content": querry},
            ]
        )
        return response['choices'][0]["message"]["content"]
