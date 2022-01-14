const message = document.getElementById('message')
const send = document.getElementById('send')
const chat = document.getElementById('chat')

const socket = io('actichat.herokuapp.com');

window.addEventListener('beforeunload', (e) => {
    socket.disconnect()
    // Cancel the event
    e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
    // Chrome requires returnValue to be set
    e.returnValue = '';
});

socket.on('connect', () => {
    socket.emit('client_connect', {code: chat.dataset.code})
    console.log('connected to server')
});

send.onclick = () => {
    console.log('clicked')
    if(message.value != ''){
        const readName = chat.dataset.name
        const readCode = chat.dataset.code
        data = {
            message: message.value,
            name: readName,
            code: readCode,
        }
        socket.emit('message', data)
        message.value = ''
        console.log('sent message')
    } 
};

message.addEventListener('keyup', (event) => {
    if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        send.click();
    }
});

// adjust scroll height when on bottom
function updateScroll(){
    let scrollDist = Math.abs(chat.offsetHeight + chat.scrollTop-chat.scrollHeight);
    chat.scrollTop = chat.scrollHeight;
}

let offset = false
socket.on('message', (data) => {
    console.log({data})
    if(data.code == chat.dataset.code){
        const messageDiv = document.createElement('div');
        const messageSender = document.createElement('span')
        const messageText = document.createElement('span');
        const messageTime = document.createElement('span');
        
        messageTime.innerText = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
        messageSender.innerText = data.name
        messageText.innerText = data.message
        
        messageDiv.className = " p-2 border-gray-800 border-y-2"
        if (offset){
            messageDiv.classList.add('bg-secondary');
        }
        offset = !offset;

        messageTime.className = "text-gray-700 mx-2 text-xl"
        messageSender.className = "text-tertiary mx-2 text-xl"
        messageText.className = "text-info mx-2 text-xl"

        messageDiv.appendChild(messageTime)
        messageDiv.appendChild(messageSender)
        messageDiv.appendChild(messageText)
        chat.appendChild(messageDiv)
        updateScroll()
    }

});