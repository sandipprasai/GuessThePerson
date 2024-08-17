import os
import random
import re
import google.generativeai as genai
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# We Set our API key from Google AI Studio
os.environ["GEMINI_API_KEY"] = "your_api_key"

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def generate_prompt(field):
    return f"Tell me about a random figure from the field of {field}. Provide their name and a brief but specific description without explicitly mentioning the name in the description. Format the response as 'Name: [character name]\nDescription: [character description]'."

def generate_character(field):
    """Generates a character name and description using the Gemini model."""
    chat_session = model.start_chat()
    prompt = generate_prompt(field)
    response = chat_session.send_message(prompt)
    name, description = response.text.split('\n', 1)
    return name.split(': ')[1], description.split(': ')[1]

def normalize_name(name):
    """Normalize a name by removing non-alphanumeric characters and converting to lowercase."""
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())

def initialize_session_state():
    if "character_name" not in st.session_state:
        st.session_state.character_name = ""
    if "character_description" not in st.session_state:
        st.session_state.character_description = ""
    if "normalized_name" not in st.session_state:
        st.session_state.normalized_name = ""
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "max_attempts" not in st.session_state:
        st.session_state.max_attempts = 3
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_field" not in st.session_state:
        st.session_state.current_field = ""
    if "game_started" not in st.session_state:
        st.session_state.game_started = False

def reset_game():
    st.session_state.character_name = ""
    st.session_state.character_description = ""
    st.session_state.normalized_name = ""
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.game_started = False

# Streamlit app
st.set_page_config(page_title="Character Guessing Game", page_icon="🎭")

colored_header(
    label="Guess The Person :)",
    description="Guess the person name based on the description!",
    color_name="blue-70",
)

initialize_session_state()

add_vertical_space(2)

# Sidebar for game settings
with st.sidebar:
    st.header("Game Settings")
    st.session_state.max_attempts = st.slider("Maximum Attempts", min_value=1, max_value=10, value=st.session_state.max_attempts)
    
    if st.button("Change Field"):
        st.session_state.current_field = ""
        reset_game()

# Field input (only if not set)
if not st.session_state.current_field:
    st.session_state.current_field = st.text_input("Enter a field for the character (e.g., Sports, Technology, Art):", key="field_input")
    if st.button("Set Field", key="set_field"):
        if st.session_state.current_field:
            st.success(f"Field set to: {st.session_state.current_field}")
            st.rerun()
        else:
            st.warning("Please enter a field before setting it.")

elif not st.session_state.game_started:
    if st.button("Start Game", key="start_game"):
        st.session_state.character_name, st.session_state.character_description = generate_character(st.session_state.current_field)
        st.session_state.normalized_name = normalize_name(st.session_state.character_name)
        st.session_state.game_started = True
        st.rerun()

if st.session_state.game_started:
    # Display current field and character description
    st.markdown(f"**Current Field:** {st.session_state.current_field}")
    st.markdown(f"**Character Description:**\n{st.session_state.character_description}")

    add_vertical_space(1)

    # Display attempts and score
    st.markdown(f"**Attempts:** {st.session_state.attempts}/{st.session_state.max_attempts}")
    st.markdown(f"**Score:** {st.session_state.score}")

    add_vertical_space(1)

    # User input
    user_guess = st.text_input("Who is this person?", key="user_guess")

    # Check answer
    if user_guess and not st.session_state.game_over:
        st.session_state.attempts += 1
        normalized_guess = normalize_name(user_guess)
        if normalized_guess == st.session_state.normalized_name:
            st.success(f"🎉 Correct! The answer is indeed {st.session_state.character_name}.")
            st.session_state.score += st.session_state.max_attempts - st.session_state.attempts + 1
            st.session_state.game_over = True
        elif st.session_state.attempts >= st.session_state.max_attempts:
            st.error(f"❌ Game over! The correct answer was: {st.session_state.character_name}")
            st.session_state.game_over = True
        else:
            st.warning(f"❓ Incorrect. You have {st.session_state.max_attempts - st.session_state.attempts} attempts left.")

    # Button to start a new game
    if st.button("New Game", key="new_game"):
        reset_game()
        st.rerun()

# Add some styling
st.markdown(
    """
    <style>
    .stButton>button {
        color: #ffffff;
        background-color: #4CAF50;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
