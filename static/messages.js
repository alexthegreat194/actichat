const message = document.getElementById('message')
    const send = document.getElementById('send')
    const chat = document.getElementById('chat')

    const socket = io()

    socket.on('connect', () => {
        console.log('connected to server')
        socket.emit('hello', 'Hello server!')
    });

    send.onclick = () => {
        console.log('clicked')
        if(message.value != ''){
            socket.emit('message', message.value)
            message.value = ''
            console.log('sent message')
        } 
    };


    socket.on('message', (data) => {
        console.log({data})

        const messageDiv = document.createElement('div');
        const messageSender = document.createElement('h5')
        const messageText = document.createElement('h1');
        const messageTime = document.createElement('h5');

        messageDiv.className = "max-w-1/3 flex flex-col items-end mx-10"

        messageSender.className = "text-sm "
        messageSender.innerText = "Person" // to be determined

        messageText.className = "bg-gray-300 p-2 text-xl rounded w-min"
        messageText.innerText = data

        messageTime.className = "text-sm"
        messageTime.innerText = "Now" // to be determined

        messageDiv.appendChild(messageSender)
        messageDiv.appendChild(messageText)
        messageDiv.appendChild(messageTime)
        chat.appendChild(messageDiv)
    });