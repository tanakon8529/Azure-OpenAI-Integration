import os
from dotenv import load_dotenv
import utils

# Add OpenAI import.
from openai import AzureOpenAI


def main(): 
        
    try:    
        utils.initLogFile() 

        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_model = os.getenv("AZURE_OAI_MODEL")
        azure_search_endpoint = os.getenv("SEARCH_ENDPOINT")
        azure_search_key = os.getenv("SEARCH_KEY")
        azure_search_index = os.getenv("SEARCH_INDEX")
        extra_body={
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": azure_search_endpoint,
                        "key": azure_search_key,
                        "indexName": azure_search_index
                    }
                }
            ]
        }

        function_map = {
            "1": function1,
            "2": function2,
            "3": function3,
            "4": function4
        }

        while True:
            print('1: Validate PoC\n' +
                  '2: Company chatbot\n' +
                  '3: Developer tasks\n' +
                  '4: Use company data\n' +
                  '\'quit\' to exit the program\n')
            command = input('Enter a number:')
            if command.strip() in function_map:
                if function_map[command] == function4:
                    clientSearch = AzureOpenAI(
                        base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_model}/extensions",
                        api_key=azure_oai_key,
                        api_version="2023-12-01-preview")
                    function_map[command](clientSearch, azure_oai_model, extension_config=extra_body)
                else:
                    client = AzureOpenAI(
                        base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_model}",
                        api_key=azure_oai_key,
                        api_version="2023-12-01-preview")
                    function_map[command](client, azure_oai_model)
            elif command.strip().lower() == 'quit':
                print('Exiting program...')
                break
            else :
                print("Invalid input. Please enter number 1, 2, 3, 4, or 5.")

    except Exception as ex:
        print(ex)

# Task 1: Validate PoC
def function1(aiClient, aiModel, **kwargs):
    inputText = utils.getPromptInput("Task 1: Validate PoC", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model.
    messages=[
        {"role": "system", "content": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."},
        {"role": "user", "content": inputText}
    ]
    

    # Define argument list
    apiParams = {
        "model": aiModel,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.5
    }


    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection.
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create(**apiParams)

    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return response

# Task 2: Company chatbot
def function2(aiClient, aiModel, **kwargs):
    inputText = utils.getPromptInput("Task 2: Company chatbot", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model
    messages = [
        {"role": "system", "content": "You are a bilingual (English and Spanish) helpful company chatbot. Provide responses in both English and Spanish, each ending with 'Hope that helps! Thanks for using Contoso, Ltd.'"},
        {"role": "user", "content": inputText}
    ]
    
    # Define argument list
    apiParams = {
        "model": aiModel,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.5
    }

    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection
    response = aiClient.chat.completions.create(**apiParams)
    print("Response: ", response)
    response_text = response.choices[0].message.content

    utils.writeLog("Response:\n", str(response))
    print("Response: " + response_text + "\n")
    return response

# Task 3: Developer tasks
def function3(aiClient, aiModel, **kwargs):
    # Dynamic input to choose file
    ser_input = input('\nEnter a prompt: 1 for fibonacci.py, 2 for legacyCode.py: ')
    if ser_input == '1':
        file = open(file="C:/files/fibonacci.py", encoding="utf8").read()
    elif ser_input == '2':
        file = open(file="C:/files/legacyCode.py", encoding="utf8").read()
    else:
        print("Invalid input. Please try again.")
        return

    # Use the read file content as user input for the AI model
    inputText = file

    # Build messages to send to Azure OpenAI model
    messages = [
        {"role": "system", "content": "You are a software engineer helping with documentation and add comments to the code."},
        {"role": "user", "content": inputText}
    ]

    # Define argument list
    apiParams = {
        "model": aiModel,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.5
    }
    
    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection
    response = aiClient.chat.completions.create(**apiParams)
    
    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return response

def function4(aiClient, aiModel, **kwargs):
    extra_body = kwargs.get("extension_config")
    inputText = utils.getPromptInput("Task 4: Use company data", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model
    messages = [
        {"role": "system", "content": "You are a helpful travel agent."},
        {"role": "user", "content": inputText}
    ]

    # Define connection and argument list
    apiParams = {
        "model": aiModel,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.5,
        "extra_body": extra_body
    }

    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection
    response = aiClient.chat.completions.create(**apiParams)
    
    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return

# Call main function. Do not modify.
if __name__ == '__main__': 
    main()
