from rich.traceback import install; install(show_locals=True)
from rich.console import Console; Print = Console().print

import eel
from settings import respond, save_chat, read_all, remove_emojis, get_data

#import base64
#import requests
#import json
#import os

# Initialize Eel with the 'web' directory
eel.init('web')

@eel.expose()
def start_conversation():
	'''
	Start the conversation by reading personality and memory files, if available,
	and preparing the assistant's initial response.
	'''
	# Read all files into one string for initial conversation setup
	combined_data = read_all(files=['personality.txt', 'memory.txt'])
	return combined_data

@eel.expose()
def handle_user_input(assistant_reply):
    '''
	Commands that the user can use
	'''

    allowed_commands = ['echo', 'mkdir', 'touch', 'cd']
    pass


# allow user to upload images:
'''
@eel.expose()
def encode_image_to_data_uri(path, mime_type='image/png'):
	with open(path, 'rb') as f:
		b64 = base64.b64encode(f.read()).decode('utf-8')
	return f'data:{mime_type};base64,{b64}'
#image_data_uri = encode_image_to_data_uri('path/to/image.png')  # replace with your image path and correct mime type
'''



# Start the Eel server, serving the 'index.html' file
eel.start('index.html', size=(800, 800), mode='edge')