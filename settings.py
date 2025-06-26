from rich.traceback import install; install(show_locals=True)
from rich.console import Console; Print = Console().print

import eel
from datetime import datetime
import openai
import edge_tts
import asyncio
import pygame
import os
import threading
import re

# Initialize pygame mixer
pygame.mixer.init()

# Set your OpenAI API key here
openai.api_key = 'ENTER OPEN AI  API KEY HERE!'

def read_all():
	# Read all content from personality.txt and memory.txt and combine them into one string.
	combined_content = ''
	# Read from personality.txt
	try:
		with open('personality.txt', 'r', encoding='utf-8') as personality_file:
			combined_content += personality_file.read() + '\n'
	except FileNotFoundError:
		print('personality.txt not found.')
	# Read from memory.txt
	try:
		with open('memory.txt', 'r', encoding='utf-8') as memory_file:
			combined_content += memory_file.read() + '\n'
	except FileNotFoundError:
		print('memory.txt not found.')
	return combined_content




@eel.expose()
def save_chat(role, message):
	# Save the conversation to a memory file.
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	with open('memory.txt', 'a', encoding='utf-8') as file:
		file.write(f'{timestamp} {role}: {message}\n')




@eel.expose()
# Get data from webpage.
def get_data(data): return data

@eel.expose()
def respond(user_input):
	'''
	Generate a response from the assistant using OpenAI's ChatCompletion.
	Launch text-to-speech in a background thread so that the text is returned immediately.
	'''
	content = read_all()
	try:
		uinput   = user_input.strip()
		command  = uinput.split(' ')[0].strip()
		argument = []
		#line = ''
		

		# Custom commands
		if(command == '@read'):
			argument = uinput.split(' ')[1:]
			contents = ''
		
			for i in argument:
				file = i.strip()
				with open(file, 'r') as File:
					contents += f'This is the file contents of: {file}\n'
					for line in File:
						if not line: continue
						line = line.strip()
						contents += f'{line}\n'

				user_input = contents.strip()

		Print(f'{command=} {argument=} {user_input=}')



		# send output
		messages = [
			{'role': 'system', 'content': content},
			{'role': 'user', 'content': user_input}
		]
		response = openai.ChatCompletion.create(
			model='gpt-4o-mini', messages=messages,
			max_tokens=2048,     temperature=0.5
		)
		assistant_reply = response.choices[0].message['content'].strip()
		save_chat('User', user_input)
		save_chat('Assistant', assistant_reply)

		# Launch TTS in a background thread so that the reply is returned immediately
		threading.Thread(target=lambda: asyncio.run(text_to_speech(assistant_reply)), daemon=True).start()
		return [assistant_reply, user_input]
	
	except Exception as e: return f'Error: {str(e)}'




@eel.expose()
def remove_emojis(text):
	#Remove emojis from text using a regular expression.
	emoji_pattern = re.compile(
		'['  # Match emojis and symbols
		u'\U0001F600-\U0001F64F'  # Emoticons
		u'\U0001F300-\U0001F5FF'  # Symbols & Pictographs
		u'\U0001F680-\U0001F6FF'  # Transport & Map Symbols
		u'\U0001F700-\U0001F77F'  # Alchemical Symbols
		u'\U0001F800-\U0001F8FF'  # Supplemental Arrows-C
		u'\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
		u'\U0001FA00-\U0001FA6F'  # Chess Symbols
		u'\U00002702-\U000027B0'  # Dingbats
		']',
		flags=re.UNICODE
	)
	return emoji_pattern.sub(r'', text)

async def text_to_speech(input_text):
	# Generate speech from text using edge_tts and play the audio.

	input_text = remove_emojis(input_text)
	text = input_text.split('>>%')[0].strip()  # Clean up the text before generating speech
	output_file = 'output.mp3'

	# Generate the speech and save it to the output file
	tts = edge_tts.Communicate(text, 'en-US-AvaNeural')
	await tts.save(output_file)

	# Play the generated MP3 file
	pygame.mixer.music.load(output_file)
	pygame.mixer.music.play()

	# Wait until the music is finished
	while(pygame.mixer.music.get_busy()):
		pygame.time.Clock().tick(10)

	# After playing, stop the music and ensure the file is released
	pygame.mixer.music.stop()
	pygame.mixer.music.unload()

	# Delete the output file after it is done playing
	if(os.path.exists(output_file)):
		os.remove(output_file)