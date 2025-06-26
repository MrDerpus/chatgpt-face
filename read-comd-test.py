user_input = '@read reqs.txt'

uinput   = user_input.strip()
command  = uinput.split(' ')[0].strip()
argument = []
line = ''

print(f'{user_input=} {command=} {argument=}')

# Custom commands
if(command == '@read'):
	argument = uinput.split(' ')[1:]
		
	for i in argument:
		file = argument[i].strip()
		with open(file, 'r') as read:
			line += f'This is the file contents of: {file}'
			for line in read:
				if not line: continue
				line += '\n'

				user_input = line.strip()

	print(0)
print(f'{command=} {argument=} {user_input=}')