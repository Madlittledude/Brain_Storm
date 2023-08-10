import streamlit as st
import openai
import os
# Set up the page layout
st.set_page_config(page_title="Brain Storm", page_icon="pixel_pencil.png", layout='wide')

# Function to display chat messages
def display_chat_message(role, content,avatar):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

def display_intro():
    st.title("Welcome to Your Session with Brain Storm :lightning:")
    st.write("Here's how it can assist you:")
    st.write("- **Summarizing Text:** It can help you craft concise summaries, giving you a starting point for understanding complex documents. Simply copy and paste the text into the chatbox.")
    st.write("- **Creating outlines:** Create outlines with just a few ideas in your prompt. The more detailed you are, the better the response.")
    st.write("- **Brainstorming and Organizing Thoughts:** It will help you layout, shape, and explore ideas.")
    st.write("- **Structuring Unstructured Text:** It guides you in organizing chaotic text.")
    st.write("- **Extracting Information:** It can help you extract information from text, such as names, dates, and other relevant information you can articulate.")
    st.write("Brain Storm can help you form the question you need to solve your problem."
    st.write("Remember, it is not a factbook; think of this tool as a springboard for your ideas and a way to initiate work product.")
    st.write(":heart: Max")

daniel = "https://raw.githubusercontent.com/Madlittledude/Brain_Storm/main/madlittledude_flipped.png"
padty = "https://raw.githubusercontent.com/Madlittledude/Brain_Storm/main/madlittledudette_flipped.png"
def display_chat_interface():

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        avatar = padty if message["role"] == "assistant" else daniel
        display_chat_message(message["role"], message["content"],avatar)

    # User input
    prompt = st.chat_input("Start thinking with your fingers...get your thoughts out")
    if prompt:
        # Set the state to indicate the user has sent their first message
        st.session_state.first_message_sent = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt,daniel)

        with st.chat_message("assistant",avatar=padty):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=([
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]),
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# Initialization logic
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": ("You are Brain Storm the virtual train of thought assistant at a municipal law firm." 
                    "Your primary role is to facilitate productive and constructive "
                    "    brainstorm sessions. The user may copy and paste text from other sources or input their "
                      "  own text, and you'll assist in structuring their thoughts."
                    "Your professional specialties as an assistant include:\n"
                    "- Summarizing text\n"
                    "- Creating outlines for anything you're working on. Just have them give you some points to follow\n"
                    "- Understanding and articulating the construction of ideas in text\n"
                    "- Brainstorming and organizing thoughts\n"
                    "- Structuring unstructured text\n"
                    "- Extracting information from text\n"
                    "You need to be a comforting tool, so it will help to gain an understanding of the user's writing and work style. )
                    }]



if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent = False

openai.api_key = os.environ["OPENAI_API_KEY"]

# Display logic
if not st.session_state.first_message_sent:
    display_intro()

display_chat_interface()






