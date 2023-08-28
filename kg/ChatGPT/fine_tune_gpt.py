import pandas as pd
import json
import openai
import os

openai.api_key = ""

def create_file():
    dataset = pd.read_csv('train_entries_smaller.csv')
    for index, row in dataset.iterrows():
        print(row['statement'])
        query = "Write a short debunk for: " + row['statement'] + (". Do not repeat debunk or any other sections like "
                                                                   "introduction, just the text")
        dic = {
            "messages": [
                {"role": "system", "content": "You are a fact-checking journalist"},
                {"role": "user", "content": query},
                {"role": "assistant", "content": row["full_explanation"]},
            ]
        }
        with open('data.json', 'a+') as json_file:
            json_file.write(json.dumps(dic) + "\n")

if __name__ == "__main__":
    '''response = openai.File.create(
        file=open("data.json", "rb"),
        purpose='fine-tune'
    )
    print(response)'''
    #response = openai.FineTuningJob.create(training_file="file-EB83voM7l9NOLxIMvmi2rBIu", model="gpt-3.5-turbo")
    #print(response)
    #print(openai.FineTuningJob.list(limit=10))
    response = openai.FineTuningJob.retrieve("ftjob-RAsIi4VAufG1CQkmZsXTsAtF")
    print(response)

    dataset = pd.read_csv('test_entries.csv')
    print(dataset.head(2))
    result = pd.DataFrame(columns=['id', 'statement', 'debunk'])
    for index, row in dataset.iterrows():
        print(row['statement'])
        querry = "Write a short debunk for: " + row['statement'] + (". Do not repeat debunk or any other sections like "
                                                                    "introduction, just the text")
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal::7qjy86na",
            messages=[
                {"role": "system", "content": "You are a fact-checking journalist."},
                {"role": "user",
                 "content": querry},
            ]
        )

        entry = {
            'id': row['id'],
            'statement': row['statement'],
            'debunk': response['choices'][0]["message"]["content"]
        }

        result = pd.concat([result, pd.DataFrame([entry])], ignore_index=True)
    result.to_csv('initial_debunks_fine_tune.csv')

