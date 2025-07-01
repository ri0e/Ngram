function output(text){
    const messageArea = document.getElementById('output');
    messageArea.textContent = text;
}

function displayMessage(status, message){
    const messageArea = document.getElementById('message-area');

    messageArea.className = '';
    messageArea.textContent = '';
    messageArea.style.display = 'none';

    messageArea.classList.add(status);
    messageArea.innerHTML = status + ':<br>' + message;

    messageArea.style.display = 'block';
    messageArea.style.opacity = '1';

    setTimeout(() => {
        messageArea.style.opacity = '0';
        setTimeout(() => {
            messageArea.style.display = 'none';
        }, 500);
    }, 5000);
}

document.addEventListener('DOMContentLoaded', function() {
    const generation = document.getElementById('generation');

    if (!generation) {
        return;
    }
    
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
            displayMessage('success', 'Successfully generated the text.');
        }

        catch(error){
            console.error('Fetch error:', error);
            displayMessage('error', error);
        }
    });
});