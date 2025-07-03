function output(text){
    const messageArea = document.getElementById('output');
    messageArea.textContent = text;
}

function displayMessage(status, message){
    const messageArea = document.getElementsByClassName('message-area')[0];

    messageArea.className = 'message-area';
    messageArea.textContent = '';
    messageArea.style.display = 'none';

    messageArea.classList.add(status);
    const symbol = status === 'success' ? '✔' : (status === 'error' ? 'X' : '');
    messageArea.innerHTML = `<p style = "font-size: 1em">${symbol} <span style = "font-size: 0.5em">${message}</span></p>`;

    messageArea.style.display = 'block';
    messageArea.style.opacity = '1';

    messageArea.addEventListener('click', function(){
        messageArea.style.opacity = '0';
        messageArea.style.display = 'none';
        return;
    });

    setTimeout(() => {
        messageArea.style.opacity = '0';
        messageArea.style.display = 'none';
    }, 7000);
}

document.addEventListener('DOMContentLoaded', function() {
    const generation = document.getElementById('generation');
    generation.addEventListener('submit', async function(event){
        console.log('DEBUG: Submit event caught by formsContainer!');
        const form = event.target.closest('.intercept');

        if (!form) {
            return;
        }

        event.preventDefault();
        
        const formAction = form.action;
        const formData = new FormData(form);

        try{
            const response = await fetch(formAction, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                displayMessage('error', errorText);
            }

            const data = await response.json();

            if(!data.next_word){
                 displayMessage(data.status, data.message);
                 return;
            }

            output(data.next_word);
            displayMessage('success', 'Text generated successfully.');
        }

        catch(error){
            console.error('Fetch error:', error);
            displayMessage('error', error);
        }
    });
});