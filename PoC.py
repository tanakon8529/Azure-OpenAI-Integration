import os
from dotenv import load_dotenv
import utils
import requests

# Add OpenAI import. (Add code here)
from openai import AzureOpenAI


def main(): 
        
    try:     
        load_dotenv()
        utils.initLogFile()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_model = os.getenv("AZURE_OAI_MODEL")
        
        # Define Azure OpenAI client (Add code here)
        client = AzureOpenAI(
            base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_model}",
            api_key=azure_oai_key,
            api_version="2023-12-01-preview"
        )

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
                function_map[command](client, azure_oai_model)
            elif command.strip().lower() == 'quit':
                print('Exiting program...')
                break
            else :
                print("Invalid input. Please enter number 1, 2, 3, 4, or 5.")

    except Exception as ex:
        print(ex)

# Task 1: Validate PoC
def function1(aiClient, aiModel):
    inputText = utils.getPromptInput("Task 1: Validate PoC", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model. (Add code here)
    messages = [
        {"role": "system", "content": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."},
        {"role": "user", "content": inputText}
    ]
    
    # Define argument list (Add code here)
    apiParams = {
        "model": aiModel,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.5
    }
    
    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection. (Add code here)
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create(**apiParams)
    
    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return response

# Task 2: Company chatbot
def function2(aiClient, aiModel):
    inputText = utils.getPromptInput("Task 2: Company chatbot", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model. (Add code here)
    messages = [
        {"role": "system", "content": "You are a bilingual (English and Spanish) helpful company chatbot. Provide responses in both English and Spanish, each ending with 'Hope that helps! Thanks for using Contoso, Ltd.'"},
        {"role": "user", "content": inputText}
    ]
    
    # Define argument list (Add code here)
    apiParams = {
        "model": aiModel,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.5
    }

    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection. (Add code here)
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create(**apiParams)
    

    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return response

# Task 3: Developer tasks
def function3(aiClient, aiModel):
    inputText = utils.getPromptInput("Task 3: Developer tasks", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model. (Add code here)
    pathAllFiles = "C:/files/"
    # Get all file names in the directory
    nameFiles = [file for file in os.listdir(pathAllFiles) if os.path.isfile(os.path.join(pathAllFiles, file))]
    # Check for specific file names in inputText
    for file in nameFiles:
        if file in inputText:
            inputText = open(os.path.join(pathAllFiles, file), encoding="utf8").read()
            break
    
    # Define system message based on the task
    system_message = ""
    if "legacyCode.py" in inputText:
        system_message = "You are a software engineer. Add comments and generate documentation for the legacy code."
    elif "fibonacci.py" in inputText:
        system_message = "You are a software engineer. Generate five unit tests for the function in the provided code."

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": inputText}
    ]

    # Define argument list (Add code here)
    apiParams = {
        "model": aiModel,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.5
    }
    
    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection. (Add code here)
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create(**apiParams)

    
    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return response 

# Task 4: Use company data
def function4(aiClient, aiModel):
    inputText = utils.getPromptInput("Task 4: Use company data", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model. (Add code here)
    search_endpoint = os.getenv("SEARCH_ENDPOINT")
    search_key = os.getenv("SEARCH_KEY")
    search_index = os.getenv("SEARCH_INDEX")
    
    # Perform the search query
    search_query = {
        "search": inputText,
        "searchMode": "any",
        "queryType": "simple",
        "top": 5  # Adjust the number of results as needed
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": search_key
    }

    search_url = f"{search_endpoint}/indexes/{search_index}/docs/search?api-version=2021-04-30-Preview"
    
    response = requests.post(search_url, headers=headers, json=search_query)
    search_results = response.json()
    
    # Extract relevant search results
    search_snippets = [result["content"] for result in search_results["value"]]
    search_content = "\n\n".join(search_snippets)
    
    # Build messages for OpenAI with search results included
    messages = [
        {"role": "system", "content": "You are a helpful travel agent."},
        {"role": "user", "content": f"{inputText}\n\nSearch Results:\n{search_content}"}
    ]

    # Define connection and argument list (Add code here)
    apiParams = {
        "model": aiModel,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.5
    }
    
    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection. Will be the same as function1 (Add code here)
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create(**apiParams)

    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return

# Call main function. Do not modify.
if __name__ == '__main__': 
    main()
