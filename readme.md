
# Ollama Chat Interface with Streamlit

This Python application provides a chat interface powered by the LLaMA model, utilizing Streamlit for the user interface. The application makes API calls to a local server hosting the model, allowing users to interact with the AI in real-time.

## Features

- **Real-time Text Streaming**: Text from the AI is streamed word-by-word with a delay to simulate real-time typing.
- **Session Management**: Previous chat messages are preserved in the session, allowing for continuous interaction.
- **Error Handling**: Proper error handling for API responses and potential errors in communication.

## Prerequisites

Before you can run this application, make sure you have the following installed:
- Python 3.10+
- Streamlit
- for intermidate.py
    - Requests library
    - [Ollama](https://ollama.com/download) 
- for simple.py
- ollama library

You can install the required Python libraries using the following command:

```bash
pip install streamlit requests
```

## Usage

To run the application:

1. Ensure that the local `Ollama` server is up and running on `http://localhost:11434/.
2. Ensure that the `model` you are trying to use as been downloaded. (the default is phi3)
### Start the Streamlit application 

start a terminal in the root directory of the application and run: 

```bash
streamlit run intermediate.py
```
# Variant Using ollama Library
This variant simplifies the setup by using the ollama library, which abstracts the API interactions.

## Usage
No Server Setup Required: The ollama library handles interactions with the model directly, so there's no need for manual server setup.

### Start the Streamlit application 

start a terminal in the root directory of the application and run: 

```bash
streamlit run simple.py
```


## Functionality
- **Chat Function:** This variant uses the ollama.chat method to directly obtain responses based on user input.
- **Error Handling:** Enhanced error handling to provide specific messages if the model is not found or if other errors occur.

## How It Works

- **Initialization**: The application sets up the Streamlit interface and initializes session state.
- **User Interaction**: Users can enter prompts through a chat input. These prompts are then sent to the LLaMA model server.
- **Streaming API**: The server returns responses in a streaming fashion, which are then displayed word-by-word on the interface.
- **Session Persistence**: All messages (both user and assistant) are stored in the session state, allowing the chat history to be displayed throughout the session.

## Code Structure

- `main()`: The main function that initializes the Streamlit interface and manages session states and chat interactions.
- `chat(messages)`: Handles sending user messages to the Ollama API and processes the streaming responses.
- `show_msgs()`: Displays the chat history stored in the session state.
- `response_generator(msg_content)`: A generator function that simulates real-time text streaming by introducing delays between words.

## Troubleshooting

If you encounter issues with the API connectivity:
- Check if the server hosting the LLaMA model is running and accessible.
- Verify the API endpoint and the request structure.
- Ensure error handling is capturing and displaying exceptions properly.
- Check Ollama documentation for help downloading the server and models. 

For further help, please refer to the Streamlit, Ollama and Requests library documentation.
