import streamlit as st
# from trasformers import pipe    
from dotenv import  load_dotenv
import os
from openai import OpenAI
import replicate

# Load enviourment variables
load_dotenv()

REPLICATE_KEY = os.getenv('REPLICATE_API_TOKENS')
OPENAI_KEY = os.getenv('OPENAI_API_TOKENS')

def generate_lyrics(prompt):
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a music lyrics writer and your task is to write lyrics of music under 30 words based on user's prompt. Just return the lyrics and nothing else"},
        {"role": "user", "content":prompt}
    ],
    temperature=0.7,
    max_tokens=50,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    output = response.choices[0].message.content
    cleaned_output = output.replace("\n"," ")
    formatted_lyrics = f"♪ {cleaned_output} ♪"
    return formatted_lyrics

# Main Streamlit app
def main():
    st.title("Music Generation with GPT-NEO")
    st.write("Enter a prompt to generate music lyrics:")
    prompt = st.text_area("Prompt")
    duration = st.slider("Duration", min_value=1, max_value=10, value=5, step=1)

    if st.button("Generate Music"):
        lyrics = generate_lyrics(prompt)
        generate_lyrics_out = lyrics
        st.write("Generated Lyrics:")
        st.write(generate_lyrics_out)
        st.write("Generating music... (This might take a while)")

        # Call your replication API here and handle the response
        input = {}
        
        replicate_client = replicate.Client(api_token=REPLICATE_KEY)
        output = replicate_client.run(
            "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787",
            input={
                "prompt":generate_lyrics_out,
                "text_temp":0.7,
                "output_full":False,
                "waveform_temp":0.7

            }
        )
        print(output)
        music_url = output['audio_out']
        music_path_or_url = music_url

        # Replace the following line with your actual music URL or path
        # music_path_or_url = "https://example.com/music.mp3"
        print(music_path_or_url)

        st.audio(music_path_or_url)

if __name__ == "__main__":
    main()

