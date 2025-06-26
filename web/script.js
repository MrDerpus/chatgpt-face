// Function to handle sending a message
document.getElementById('send').addEventListener('click', async () => {
	const userInputElement   = document.getElementById('user-input');
	const chatHistoryElement = document.getElementById('chat-history');
	const userInput = userInputElement.value.trim();

	// If the input is empty, don't send anything
	if(!userInput) { return; }

	//const get_data = await eel.get_data(userInput)(); // Send to python

	// Clear the input field
	userInputElement.value = "";

	// Append user message to chat history and save it
	chatHistoryElement.value += `\n\nYou: ${userInput}`;
	//eel.save_chat("User", userInput)();


	// Call the Python 'respond' function and wait for a response
	const result = await eel.respond(userInput)();

	const response = result[0];
	//console.log(outcomes)
	

	// Remove the facial parameter sequence from the response for display
	const cleanedResponse = response.split(">>%")[0].trim();

	// Append assistant's cleaned response to chat history and save it
	chatHistoryElement.value += `\n\nAva: ${cleanedResponse}`;
	//eel.save_chat("Assistant", cleanedResponse)();

	// Parse the facial features from the full response (which still includes the parameters)
	const faceData = parseFaceData(response);

	// Update the face based on the extracted facial feature data
	updateFace(faceData);

	// Trigger text-to-speech using the full response (which internally ignores the facial parameters)
	//playTextToSpeech(response);
});

// Function to parse facial feature data from the response string
function parseFaceData(response)
{
	// Updated regex: all four groups capture any text (not including commas)
	const faceDataRegex = />>%\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+)/;
	const match = response.match(faceDataRegex);

	if(match)
	{
		return {
			eyebrows: match[1].trim(),
			eyes:     match[2].trim(),
			mouth:    match[3].trim(),
			blush:    match[4].trim()
		};
	}

	// Default facial features if no match is found
	return {
		eyebrows: "normal-eyebrows1.png",
		eyes: "normal-eyes.png",
		mouth: "smile1-mouth.png",
		blush: "blush0.png"
	};
}

// Function to update the facial features based on the extracted face data
function updateFace(faceData)
{
	document.getElementById("eyebrows").src = "gpt-face/" + faceData.eyebrows;
	document.getElementById("eyes").src     = "gpt-face/" + faceData.eyes;
	document.getElementById("mouth").src    = "gpt-face/" + faceData.mouth;
	document.getElementById("blush").src    = "gpt-face/" + faceData.blush;
}

// Function to handle text-to-speech by calling the exposed Python function
/*function playTextToSpeech(response)
{ eel.text_to_speech(response)(); }*/

function get_data(data)
{
	eel.get_data(data)();
}