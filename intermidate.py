import streamlit as st
import requests
import json
import time
import os

model = "llama3"  

def response_generator(msg_content):
    lines = msg_content.split('\n')
    for line in lines:
        words = line.split()
        for word in words:
            yield word + " "
            time.sleep(0.1)
        yield "\n"

def show_msgs():
    for msg in st.session_state.messages:
        role = msg["role"]
        with st.chat_message(role):
            st.write(msg["content"])

def chat(messages):
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={"model": model, "messages": messages, "stream": True},
        )
        response.raise_for_status()
        output = ""
        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done", False):
                return {"role": "assistant", "content": output}
            output += body.get("message", {}).get("content", "")
    except Exception as e:
        return {"role": "assistant", "content": str(e)}

def format_messages_for_summary(messages):
    # Create a single string from all the chat messages
    return '\n'.join(f"{msg['role']}: {msg['content']}" for msg in messages)


def summary(messages):
    sysmessage = "summarize this conversation in 3 words. No symbols or punctuation:\n\n\n"
    combined = sysmessage + messages
    api_message = [{"role": "user", "content": combined}]
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={"model": model, "messages": api_message, "stream": True},
        )
        response.raise_for_status()
        output = ""
        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done", False):
                return output
            # This will append only the content from each message, if available.
            output += body.get("message", {}).get("content", "")
    except Exception as e:
        return str(e)

def save_chat():
    if not os.path.exists('./Intermediate-Chats'):
        os.makedirs('./Intermediate-Chats')
    if st.session_state['messages']:
        formatted_messages = format_messages_for_summary(st.session_state['messages'])
        chat_summary = summary(formatted_messages)
        filename = f'./Intermediate-Chats/{chat_summary}.txt'
        with open(filename, 'w') as f:
            for message in st.session_state['messages']:
                # Replace actual newline characters with a placeholder
                encoded_content = message['content'].replace('\n', '\\n')
                f.write(f"{message['role']}: {encoded_content}\n")
        st.session_state['messages'].clear()
    else:
        st.warning("No chat messages to save.")

def load_saved_chats():
    chat_dir = './Intermediate-Chats'
    if os.path.exists(chat_dir):
        # Get all files in the directory
        files = os.listdir(chat_dir)
        # Sort files by modification time, most recent first
        files.sort(key=lambda x: os.path.getmtime(os.path.join(chat_dir, x)), reverse=True)
        for file_name in files:
            display_name = file_name[:-4] if file_name.endswith('.txt') else file_name  # Remove '.txt' from display
            if st.sidebar.button(display_name):
                st.session_state['show_chats'] = False  # Make sure this is a Boolean False, not string 'False'
                st.session_state['is_loaded'] = True
                load_chat(f"./Intermediate-Chats/{file_name}")
                # show_msgs()

def format_chatlog(chatlog):
    # Formats the chat log for downloading
    return "\n".join(f"{msg['role']}: {msg['content']}" for msg in chatlog)

def load_chat(file_path):
    # Clear the existing messages in the session state
    st.session_state['messages'].clear()  # Using clear() to explicitly empty the list
    show_msgs()
    # Read and process the file to extract messages and populate the session state
    with open(file_path, 'r') as file:
        for line in file.readlines():
            role, content = line.strip().split(': ', 1)
            # Decode the placeholder back to actual newline characters
            decoded_content = content.replace('\\n', '\n')
            st.session_state['messages'].append({'role': role, 'content': decoded_content})

def main():
    st.title("LLaMA Chat Interface")
    user_input = st.chat_input("Enter your prompt:", key="1")
    if 'show' not in st.session_state:
        st.session_state['show'] = 'True'
    if 'show_chats' not in st.session_state:
        st.session_state['show_chats'] = 'False'
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    show_msgs()
    if user_input:
        with st.chat_message("user",):
                st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        combined = "\\n".join(msg["content"] for msg in st.session_state.messages if msg["role"] == "user")
        messages = [{"role": "user", "content": combined}]
        response = chat(messages)
        st.session_state.messages.append(response)
        with st.chat_message("assistant"):
            st.write_stream(response_generator(response["content"]))    
    elif st.session_state['messages'] is None:
        st.info("Enter a prompt or load chat above to start the conversation")
    chatlog = format_chatlog(st.session_state['messages'])
    st.sidebar.download_button(
        label="Download Chat Log",
        data=chatlog,
        file_name="chat_log.txt",
        mime="text/plain"
    )
    for i in range(5):
        st.sidebar.write("")
    if st.sidebar.button("Save Chat"):
        save_chat()

    
    # Show/Hide chats toggle
    if st.sidebar.checkbox("Show/hide chat history", value=st.session_state['show_chats']):
        st.sidebar.title("Previous Chats")
        load_saved_chats()
        
    for i in range(3):
        st.sidebar.write(" ")


if __name__ == "__main__":
    main()
