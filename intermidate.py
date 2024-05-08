import streamlit as st
import requests
import json
import time

#####################################
#                                   #
# This app is for those who         #
# are running an ollama instance    #
# locally or on your network.       #
# There is Currently no memory of   #
# chat                              #
#####################################

model = "phi3"  

def response_generator(msg_content):
    lines = msg_content.split('\n')  # Split the content into lines to preserve paragraph breaks.
    for line in lines:
        words = line.split()  # Split the line into words to introduce a delay for each word.
        for word in words:
            yield word + " "
            time.sleep(0.1)
        yield "\n"  # After finishing a line, yield a newline character to preserve paragraph breaks.

def show_msgs():
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            # For assistant messages, use the custom avatar
            with st.chat_message("assistant"):
                st.write(msg["content"])
        else:
            # For user messages, display as usual
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

def chat(messages):
    try:
        r = requests.post(
            "http://localhost:11434/api/chat", #modify this field if you are running a networked instance of ollama 
            json={"model": model, "messages": messages, "stream": True},
        )
        r.raise_for_status()
        output = ""
        for line in r.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done") is False:
                message = body.get("message", "")
                content = message.get("content", "")
                output += content
            if body.get("done", False):
                message["content"] = output
                return message
    except Exception as e:
        return {"content": str(e)}

def main():
    st.title("LLaMA Chat Interface")
    user_input = st.chat_input("Enter your prompt:", key="1")
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    show_msgs()
    if user_input:
            with st.chat_message("user",):
                st.write(user_input)
            messages = [{"role": "user", "content": user_input}]
            #TODO This works when using the library but not with the server with requests. Dunno why
            # messages = "\n".join(msg["content"] for msg in st.session_state.messages)
            # response = chat(messages)
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = chat(messages)
            st.session_state.messages.append({"role": "assistant", "content": (response.get("content", "")), })
            # st.chat_message("bot").write(response.get("content", ""))
            with st.chat_message("assistant"):
                st.write_stream(response_generator(response.get("content", "")))    
    else:
        st.info("Enter a prompt above to start the conversation")

if __name__ == "__main__":
    main()