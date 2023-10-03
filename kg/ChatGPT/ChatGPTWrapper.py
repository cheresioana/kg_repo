import openai


class ChatGPTWrapper:
    def __init__(self):
        openai.api_key = "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"

    def create_debunk(self, statement):
        querry = "Write a short debunk for: " + str(statement)
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal::7tW4uzOE",
            messages=[
                {"role": "system", "content": "You are a fact-checking journalist."},
                {"role": "user",
                 "content": querry},
            ]
        )
        return response['choices'][0]["message"]["content"]
