import openai

'''response =  openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

print(response)'''

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a fact-checking journalist."},
        {"role": "user",
         "content": "Write a short debunk for: Ukraine will be annexed to Poland, in order to be part "
                    "of NATO and the EU. Do not repeat debunk or any other sections like introduction, just the text"},
    ]
)

print(response)
