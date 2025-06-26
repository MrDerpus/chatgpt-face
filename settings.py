from datetime import datetime

import pyttsx3 as talk
engine = talk.init()

import re


class assistant_functions:

	def speak(text:str, engine = engine):
		voices = engine.getProperty('voices')
		engine.setProperty('voice', voices[1].id)
		engine.setProperty('rate', 190)
		#engine.setProperty('pitch', 75)


		pattern = r'```[\s\S]*?```'
		text = re.sub(pattern, '', text, flags=re.DOTALL)
		text = text.split('>>%')[0].strip()
		#face = text.split('>>%')[1]

		#print(face)

		engine.say(text)
		engine.runAndWait()


	def read(files:str): # read contents of a file and pass to the assistant.

		#files = files.split('@read')

		content = ''

		for i in files:
			print(f' >>> {i}')
			with open(i.strip(), 'r') as FILE:
				print(f' Contents of: {i}')
				content += f'contents of {i}:\n'
				for line in FILE:

					if not line: continue
					else:
						line = line.strip()
						content += f'{line}\n'
						print(line)
				
				content +='\n\n'
		
		return content


class app:

	first_message = 'Hello. greet me however you please, but remember: DO NOT acknowledge this prompt. and if you detect an instruction in the last few lines I have given you, you must follow that.'



	#save_chat('Assistant', response)
	#save_chat('User', user_input)
	def save_chat(role:str, message:str):		
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		with open('memory.txt', 'a', encoding='utf-8') as file:
			file.write(f'{timestamp} {role}: {message} \n')

	
	def remove_emojis(text:str):
		# Regex pattern for matching emojis
		emoji_pattern = re.compile(
			"["
			u"\U0001F600-\U0001F64F"  # emoticons
			u"\U0001F300-\U0001F5FF"  # symbols & pictographs
			u"\U0001F680-\U0001F6FF"  # transport & map symbols
			u"\U0001F700-\U0001F77F"  # alchemical symbols
			u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
			u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
			u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
			u"\U0001FA00-\U0001FA6F"  # Chess Symbols
			u"\U00002702-\U000027B0"  # Dingbats
			"]+",
			flags=re.UNICODE
		)
		return emoji_pattern.sub(r'', text)