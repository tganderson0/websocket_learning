
var minus = document.querySelector('.minus'),
    plus = document.querySelector('.plus'),
    value = document.querySelector('.value'),
    users = document.querySelector('.users'),
    chat = document.querySelector('#chat_input'),
    send = document.querySelector('#send_message'),
    messageWindow = document.querySelector('#messages'),
    registration = document.querySelector('#registration'),
    registerButton = document.querySelector('#registration_button'),
    registerWindow = document.querySelector('.register'),
    username = '',
    websocket = new WebSocket("ws://127.0.0.1:6789/");

minus.onclick = function (event) {
        websocket.send(JSON.stringify({action: 'minus'}));
}

plus.onclick = function (event) {
	websocket.send(JSON.stringify({action: 'plus'}));
}

websocket.onmessage = function (event) {
        data = JSON.parse(event.data);
        switch (data.type) {
        	case 'state':
                	value.textContent = data.value;
                        break;
                case 'users':
                        users.textContent = (
                            data.count.toString() + " user" +
                            (data.count == 1 ? "" : "s"));
                        break;
                
		case 'message':
			let message = document.createElement('p');
			message.textContent = data.message;
			messageWindow.insertBefore(message, messageWindow.firstChild);
			break;
		default:
                	console.error(
                            "unsupported event", data);
                }
};

send.onclick = function (event) {
	if (chat.value !== ''){
		let text = chat.value;
		chat.value = '';
		websocket.send(JSON.stringify({action: 'message', message: text, username: username}));
	}
}

registerButton.onclick = function (event) {
	if (registration.value != ''){
		username = registration.value;
		registration.value = 'registered!'
		websocket.send(JSON.stringify({action: 'register', username: username}))
		registerWindow.innerHTML = `<p>Registered: ${username}</p>`;
	}
}
