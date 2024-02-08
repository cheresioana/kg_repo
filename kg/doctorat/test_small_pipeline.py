import openai
from transformers import pipeline

from constanst import OPENAI_API_KEY

'''
This represents a small example of the pipeline I want to implement

1. Find some examples for ChatGPT to understand what I need
2. Define a test set
3. Obtain the pattern using ChatGPT
4. Verify the pattern using NLI / textual entailment

End result -> from unstructured text the model should be able to find common patterns for disinformation statements to identify trends and patterns. 
'''


if __name__ == '__main__':
    #define 3 examples
    #these examples are used to give openAI model some context
    statements1 = [
        'EU is subject to American domination',
        'When the US orders, the EU complies',
        'The EU and its member states are US vassals',
        'The US is pushing Europe into the abyss',
        'European states are vassals of the US',
        'The West fights with Russia through Ukraine'
    ]
    result1 = 'EU is dominated by USA'

    statements2 = [
        'The EU wants to push Moldova to a confrontation with Russia',
        'The EU is obsessed with anti-Russian sanctions',
        'The EU wants to destroy Russia and its sovereignty',
        "The EU is interested in the long-term war in Ukraine because of its anti-Russian position"
    ]
    result2 = 'EU wants to destroy Russia'

    statements3 = [
        'Ukraine is a Soviet invention',
        'Ukraine does not exist, it is part of Russia',
        'Ukraine does not exist, it is a Polish fake',
        'Ukraine does not exist as a state, it is a colony of the US Democratic Party',
        "Ukraine is a Nazi state, dangerous to Russia's existence",
    ]

    result3 = 'Ukraine is not a state'

    #prepare the query for the OpenAI model
    query = "Find the common simple pattern for some of the following statements" + ' ,'.join(statements1) + "It must be a simple sentence"

    past_examples = [
            {"role": "system", "content": "You are a journalist."},
            {"role": "user", "content": query},
            {"role": "assistant", "content": "" + result1},
            {"role": "user", "content": "Find the common pattern for some of the following statements" + ' ,'.join(statements2)},
            {"role": "assistant", "content": "" + result2},
            {"role": "user",
             "content": "Find the common pattern for some of the following statements" + ' ,'.join(statements3)},
            {"role": "assistant", "content": "" + result3}
    ]

    #initiate the NLI / text entailment model
    nli_pipe = pipeline("text-classification",model="sileod/deberta-v3-base-tasksource-nli")
    make_input = lambda x: [dict(text=prem,text_pair=hyp) for prem,hyp in x]

    # define 1 test
    statements4 = [
        'Zelenski has ties with the Nazis',
        'Zelenskyy is only a marketing operation, a Jewish face for a Nazi regime',
        'Zelenski makes laws to extend the war with Russia'
    ]

    # ask the openAI model to generate a pattern
    current_message = past_examples
    current_message.append({"role": "user", "content": "Find the common pattern for some of the following statements" + ' ,'.join(statements4)})
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=current_message
    )
    #print the pattern generated
    print("Test1 on sentece set:\n" + '\n'.join(statements4) + "\n\n")
    print("Open AI model generated pattern: "+ response["choices"][0]["message"]["content"] )
    #print(response)
    #verify the generated patern with textual entailment
    final_response = response["choices"][0]["message"]["content"]
    for statement in statements4:
        print(f'For the premise {statement} the hypothesis can be infered {final_response}')
        result = nli_pipe(make_input([(statement, final_response)]))  # list of (premise,hypothesis)
        print(result)


    #define 1 more test set

    statements5 = [
        'Romania is an American colony in which censorship is imposed',
        'EU forces Romania to give up its constitution and sovereignty',
        "The shooting of the bear Arthur shows that Romania is a western colony",
        'Romania is a colony of the EU'
    ]

    # ask the openAI model to generate a pattern
    current_message = past_examples
    current_message.append({"role": "user",
                            "content": "Find the common pattern for some of the following statements" + ' ,'.join(
                                statements5)})
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=current_message
    )
    print("\n\nTest2 on  sentence set:\n" + '\n'.join(statements5) + "\n\n")
    print("Open AI model generated pattern: " + response["choices"][0]["message"]["content"])
    #print(response)
    # verify the generated patern with textual entailment
    final_response = response["choices"][0]["message"]["content"]
    for statement in statements5:
        print(f'For the premise {statement} the hypothesis can be infered {final_response}')
        result = nli_pipe(make_input([(statement, final_response)]))  # list of (premise,hypothesis)
        print(result)