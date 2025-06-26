from rich.traceback import install; install(show_locals=True)
from rich.console import Console; Print = Console().print



from settings import app, assistant_functions

import openai # type: ignore



Print('Initialising...')

# Set your API key directly on the openai module
openai.api_key = "ENTER OPEN AI  API KEY HERE."


tokens:int  = 2048
temp:float  = 0.7
colour:str  = '#aa00bb'
content:str =  ''

Print('Reading personality file...')
with open('personality.txt', encoding='utf-8') as FILE:
	for line in FILE:
		content += f'{line.strip()} '

content += '\nThis is now our entire chat history:\n'

Print('Reading memory file...')
with open('memory.txt', encoding='utf-8') as FILE:
	for line in FILE:
		content += f'{line.strip()} '



# set up and first response

messages = [{"role": "system", "content": content}]
messages.append({"role": "user", "content": app.first_message})

response = openai.ChatCompletion.create(
	model="gpt-4o-mini", messages=messages,
	max_tokens=tokens,   temperature=temp
)
reply = response.choices[0].message.content
messages.append({"role": "assistant", "content": reply})
Print(f'\nAssistant: \n{reply}\n', style=colour)
app.save_chat('Assistant', reply)
reply = app.remove_emojis(reply)
assistant_functions.speak(reply)







while(True):
	user_input = input('\nYou:\n').strip()

	if(len(user_input) == 0): continue

	# Commands
	if(user_input[0] == '@'):
		

		# Handle commands here if you need to
		# For example, if @quit, break the loop
		#line = line.replace(',', '')
		line = user_input[1:].split()

		#@read file-here.txt
		if(len(line) == 2):
			command  = line[0]
			argument = line[1:]


			match command:
				case 'read':
					contents = assistant_functions.read(argument)
					user_input = contents
					#app.save_chat('User-action', f'{user_input}\n{contents}')
					#messages.append({"role": "user", "content": contents})


		if(len(line) == 3):
			command  = line[0]
			variable = line[1]
			argument = line[2]
			match command:
				case 'set':
					print(f' Changing {variable} value from {eval(variable)} to {argument}')
					match variable:
						case 'tokens': tokens = int(argument)
						case 'temp':   temp   = float(argument)
						case 'colour': colour = str(argument)
					continue







	# ChatGPT
	# User message
	app.save_chat('User', user_input)
	messages.append({"role": "user", "content": user_input})





	# Call the ChatCompletion endpoint directly
	response = openai.ChatCompletion.create(
		model="gpt-4o-mini", messages=messages,
		max_tokens=tokens,   temperature=temp
	)

	reply = str(response.choices[0].message.content).strip()
	Print(f'\nAssistant: \n{reply}\n', style=colour)
	messages.append({"role": "assistant", "content": reply})

	app.save_chat('Assistant', reply)
	reply = app.remove_emojis(reply)
	assistant_functions.speak(reply)
