function submitPrompt() {
    const inputBox = document.getElementById('userInput');
    const chatBox = document.getElementById('chat-box');
    const loadingBubble = document.getElementById('loading-bubble');
    const userText = inputBox.value.trim();

    if (userText) {
        chatBox.innerHTML += `<div class='user-message'>Användare: ${userText}</div>`;
        inputBox.value = '';

        // Visa pulserande bubbla
        loadingBubble.classList.remove('hidden');

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
                    chatBox.innerHTML += `<div class='bot-message'>AllsvenskanGPT: ${data.error}</div>`;
                } else {
                    chatBox.innerHTML += `<div class='bot-message'>AllsvenskanGPT: ${data.response}</div>`;
                }
                chatBox.scrollTop = chatBox.scrollHeight;

                // Dölj pulserande bubbla
                loadingBubble.classList.add('hidden');
            })
            .catch(error => {
                chatBox.innerHTML += `<div class='bot-message'>AllsvenskaGPT: Ett fel inträffade: ${error.message}</div>`;

                // Dölj pulserande bubbla
                loadingBubble.classList.add('hidden');
            });
    }
}
