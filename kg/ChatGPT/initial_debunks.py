import pandas as pd
import openai

if __name__=="__main__":
    dataset = pd.read_csv('test_entries.csv')
    print(dataset.head(2))
    result = pd.DataFrame(columns=['id', 'statement', 'debunk'])
    for index, row in dataset.iterrows():
        print(row['statement'])
        querry = "Write a short debunk for: " + row['statement'] + (". Do not repeat debunk or any other sections like "
                                                                    "introduction, just the text")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fact-checking journalist."},
                {"role": "user",
                 "content": querry},
            ]
        )

        entry = {
            'id': row['id'],
            'statement' : row['statement'],
            'debunk': response['choices'][0]["message"]["content"]
        }

        result = pd.concat([result, pd.DataFrame([entry])], ignore_index=True)
    result.to_csv('initial_debunks.csv')
