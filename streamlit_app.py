import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("CodeBot")
st.write(
    "Hi I am CodeBot a personalized code helper for devs looking to skyrocket progress"
)

SYSTEM_PROMPT = ("You are a helpful assistant that gives people code based on what they ask for."
                 "You answer the questions with both code and explanations of the code."
                 "If they need help learning JavaScript you will give them the url to the Bro Code Youtube channel."
                 "If they need help learning python you will give them the url to the Bro Code Youtube channel."
                 "If they ask for good videos to learn coding give them the url for the Bro Code Youtube channel."
                 "If they ask for fun projects to try for coding give them a concise but smart answer."
                 "Bro code is always a good source of information if they ask."
                 "Because you are a coding assistant you only answer code related questions. Any other questions you will politely refuse."
                 )
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
   st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.write("Powerd by OPENAI")