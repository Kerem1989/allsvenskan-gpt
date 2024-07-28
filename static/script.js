function submitPrompt() {
    const inputBox = document.getElementById('userInput');
    const chatBox = document.getElementById('chat-box');
    const introText = document.getElementById('intro-text');
    const userText = inputBox.value;

    if (userText) {
        if (introText) {
            introText.remove(); // Tar bort introduktionstexten vid första meddelandet
        }
        chatBox.innerHTML += `<div class='user-message'>Användare: ${userText}</div>`;
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: userText })
        })
            .then(response => response.json())
            .then(data => {
                chatBox.innerHTML += `<div class='bot-message'>PatentGPT: ${data}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        inputBox.value = '';
    }
}
