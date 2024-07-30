function submitPrompt() {
    const inputBox = document.getElementById('userInput');
    const chatBox = document.getElementById('chat-box');
    const userText = inputBox.value.trim();

    if (userText) {
        chatBox.innerHTML += `<div class='user-message'>Användare: ${userText}</div>`;

        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({prompt: userText})
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    chatBox.innerHTML += `<div class='bot-message'>PatentGPT: ${data.error}</div>`;
                } else {
                    chatBox.innerHTML += `<div class='bot-message'>PatentGPT: ${data.response}</div>`;
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(error => {
                chatBox.innerHTML += `<div class='bot-message'>PatentGPT: Ett fel inträffade: ${error.message}</div>`;
            });

        inputBox.value = '';
    }
}
