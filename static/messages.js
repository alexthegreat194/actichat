const message = document.getElementById('message')
const send = document.getElementById('send')
const chat = document.getElementById('chat')

const socket = io();

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


socket.on('message', (data) => {
    console.log({data})
    if(data.code == chat.dataset.code){
        const messageDiv = document.createElement('div');
        const messageSender = document.createElement('h5')
        const messageText = document.createElement('h1');
        const messageTime = document.createElement('h5');

        messageDiv.className = "max-w-1/3 flex flex-col items-end mx-10"

        messageSender.className = "text-sm "
        messageSender.innerText = data.name

        messageText.className = "bg-gray-300 p-2 text-xl rounded w-min"
        messageText.innerText = data.message

        messageTime.className = "text-sm"
        messageTime.innerText = new Date().toLocaleTimeString()

        messageDiv.appendChild(messageSender)
        messageDiv.appendChild(messageText)
        messageDiv.appendChild(messageTime)
        chat.appendChild(messageDiv)
    }

});