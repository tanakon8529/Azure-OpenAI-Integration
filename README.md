
# Azure-OpenAI-Integration

## Description
This repository is designed to showcase the integration of Azure OpenAI models with Azure Cognitive Search. It demonstrates a variety of functionalities, including validating concepts, developing a chatbot, aiding developers, and using specific company data for enhanced operations.

## Setup and Installation

### Requirements
- Python
- `dotenv`: For loading environment variables.
- `openai`: For interacting with Azure OpenAI services.

### Installation

Install the required packages using pip:

```bash
pip install python-dotenv openai
```

### Azure Setup
1. **Azure OpenAI Deployment:**
   - Ensure you have an Azure account and have set up an Azure OpenAI instance.
   - Navigate to the Azure portal and deploy your model, recording your endpoint, API key, and model name.

2. **Azure Cognitive Search:**
   - Set up Azure Cognitive Search in your Azure portal.
   - Create an index and upload the data you plan to use.
   - Ensure the search service is configured to accept connections from your application.

### Configuration
Create a `.env` file in the root directory of your project and update it with your Azure credentials and settings:

```plaintext
AZURE_OAI_ENDPOINT='Your Azure OpenAI Endpoint'
AZURE_OAI_KEY='Your Azure OpenAI Key'
AZURE_OAI_MODEL='Your Model Identifier'
SEARCH_ENDPOINT='Your Azure Search Endpoint'
SEARCH_KEY='Your Azure Search API Key'
SEARCH_INDEX='Your Search Index Name'
```

### Sample Files
Create the following sample files within a `samples` directory:

- `sample-text.txt`: Contains text prompts used by the chat functions.
- `fibonacci.py`: Python script for Fibonacci sequence logic.
- `legacyCode.py`: Python script containing older code for refactoring or documentation.

### Data for Azure Cognitive Search
To use company data with the prompt as a travel agent:
- Upload relevant data, such as travel packages, customer reviews, or destination information to your Azure Search service.
- Ensure the data is indexed properly to facilitate efficient search queries that the OpenAI model can utilize.
