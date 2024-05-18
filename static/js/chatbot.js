function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function createMessageElement(content, type) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = content;

    const messageTime = document.createElement('div');
    messageTime.classList.add('message-time');
    messageTime.textContent = getCurrentTime();

    messageElement.appendChild(messageContent);
    messageElement.appendChild(messageTime);

    return messageElement;
}

async function sendMessage() {
    const chatBody = document.getElementById('chatBody');
    const userInput = document.getElementById('userInput');
    const userMessage = userInput.value.trim();

    if (userMessage) {
        const userMessageElement = createMessageElement(userMessage, 'sent');
        chatBody.appendChild(userMessageElement);

        chatBody.scrollTop = chatBody.scrollHeight;

        userInput.value = '';

        const systemMessage = await sendMessageToBackend(userMessage);
        console.log(systemMessage)
        const systemMessageElement = createMessageElement(systemMessage, 'received');
        chatBody.appendChild(systemMessageElement);
        chatBody.scrollTop = chatBody.scrollHeight;

    }
}

async function sendMessageToBackend(userMessage) {
    try {
        const response = await fetch('http://127.0.0.1:8000/question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        return result.message;
    } catch (error) {
        console.error('Error sending message to backend:', error);
    }
}

