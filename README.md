# Guess The Person Game

This is a Streamlit-based web application that generates a character name and description using Google's Generative AI model. The user has to guess the character's name based on the description provided.

## Features

- Generates a character name and description from a specified field.
- Allows users to guess the character's name.
- Keeps track of attempts and score.
- Provides game settings to adjust the maximum number of attempts.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/character-guessing-game.git
    cd character-guessing-game
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set your Google AI Studio API key:
    ```bash
    export GEMINI_API_KEY=your_api_key
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run guesstheperson.py
    ```

## Usage

1. Open the app in your browser.
2. Enter a field for the character (e.g., Sports, Technology, Art).
3. Start the game and guess the character's name based on the description provided.
4. Adjust the game settings using the sidebar.

## Dependencies

- `os`
- `random`
- `re`
- `google.generativeai`
- `streamlit`
- `streamlit_extras`

## License

This project is licensed under the MIT License.
