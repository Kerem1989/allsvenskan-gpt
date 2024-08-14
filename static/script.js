function submitPrompt() {
    const inputBox = document.getElementById('userInput');
    const chatBox = document.getElementById('chat-box');
    const userText = inputBox.value.trim();

    if (userText) {
        // Lägg till användarens meddelande i chatten
        chatBox.innerHTML += `<div class='user-message'>Användare: ${userText}</div>`;

        // Lägg till en pulserande text för PatentGPT:s svar
        chatBox.innerHTML += `<div class='bot-message pulsing'>PatentGPT tänker...</div>`;

        // Skicka användarens input till servern och hämta GPT:s svar
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({prompt: userText})
        })
            .then(response => response.json())
            .then(data => {
                // Ersätt den pulserande texten med det faktiska svaret
                const botMessage = chatBox.querySelector('.bot-message.pulsing');
                botMessage.textContent = `PatentGPT: ${data.response}`;
                botMessage.classList.remove('pulsing');
                adjustMessageBoxWidth(botMessage); // Call the function to adjust width
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(error => {
                // Hantera fel och visa ett felmeddelande
                const botMessage = chatBox.querySelector('.bot-message.pulsing');
                botMessage.textContent = `PatentGPT: Ett fel inträffade: ${error.message}`;
                botMessage.classList.remove('pulsing');
            });

        // Töm användarens inputfält
        inputBox.value = '';
    }
}

function adjustMessageBoxWidth(messageElement) {
    // Get the content width of the message
    const contentWidth = messageElement.scrollWidth;

    // Set the message box width to content width with a minimum and maximum
    messageElement.style.width = Math.max(300, Math.min(contentWidth, 600)) + 'px';
}
