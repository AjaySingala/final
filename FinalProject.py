import streamlit as st
from openai import OpenAI
# Import the required module for text to speech conversion.
from gtts import gTTS

key = "sk-proj-1B9XOQHXAgdCBJtyRYqJT3BlbkFJMr7l4qQgUfJzHxyibjuk"
client = OpenAI(api_key="sk-proj-1B9XOQHXAgdCBJtyRYqJT3BlbkFJMr7l4qQgUfJzHxyibjuk")

st.set_page_config(layout="wide")
st.header("Ajay's Translate and Text-to-Speech Demo")
#st.write("------------------------------------------------------------------")
st.write("#### Instructions: ")
st.write('''
- Enter text to be translated.
- Select the language to translate the text to.
- Click on the 'Translate' button to translate the text.
- Play the generated audio file to listen to the translated text.
''')
st.write("------------------------------------------------------------------")

left_column, right_column = st.columns([.50,.50])

def translate(prompt):
    # Make the API call
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.3,
        max_tokens=60,
    )
    return response.choices[0].text.strip()

def save_play_audio(filename, result):
	try:
		# Saving the converted audio in a mp3 file.
		result.save(filename)
		
		# Playback the audio.
		st.text("Play the audio to hear the translated text:")
		st.audio(filename, format="audio/mpeg", loop=False)
	except:
		st.text(f"Error playing audio file {filename}")

def prepare_for_translate(sentence, translate_language):

	language_codes = {"French": "fr", "Spanish": "es", "German": "de", "English": "en", "Hindi": "hi"}
	
	with right_column:
		try:
			filename = f"AjaySingala_{translate_language}.mp3"
			# First: translate.
			st.text(f"You entered {sentence}")
			st.text(f"In {translate_language}, it would be:")
			translation_prompt = f"Translate '{sentence}' into {translate_language}."
			translation = translate(translation_prompt)
			st.success(translation)
			
			# Second: convert to speech.
			language = language_codes[translate_language]
			result = gTTS(text=translation, lang=language, slow=False)
		except:
			st.text("Unable to translate the given text. Please retry.")

		save_play_audio(filename, result)

def main():
	# Create the UI to accept a sentence and translate to French or Spanish.

	with left_column:
		sentence = st.text_input("Enter text to be translated: ")

		# Dropdown to select Language to translate to.
		translate_language = st.selectbox("Translate text into: ",
							 ['French', 'Spanish', 'German', 'English', 'Hindi'])
	 
		# print the selected language.
		st.write("You selected: ", translate_language)

		if(st.button("Translate")):
			if(sentence.strip() == ""):
				st.text("Please enter a text to translate.")
			else:
				prepare_for_translate(sentence, translate_language)
			
if __name__ == "__main__":
	main()
	