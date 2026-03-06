document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const userMessage = userInput.value.trim();
        if (userMessage === '') return;

        // Display user's message
        appendMessage(userMessage, 'user-message');
        userInput.value = '';

        // Display a loading indicator
        const loadingIndicator = appendMessage('...', 'bot-message');

        try {
            // Send message to the backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();

            // Remove loading indicator
            loadingIndicator.remove();

            if (data.error) {
                appendMessage(`Error: ${data.error}`, 'bot-message');
            } else {
                appendMessage(data.response, 'bot-message');
            }

        } catch (error) {
            // Remove loading indicator and show error
            loadingIndicator.remove();
            appendMessage('Error: Could not connect to the server.', 'bot-message');
            console.error('Fetch error:', error);
        }
    });

    function appendMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
        return messageElement;
    }
});
