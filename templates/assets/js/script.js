const chatbot = document.getElementById('chatbot');
const chats = document.getElementById("chats");
const input_box = document.querySelector('.chat-input');
const bg_logo = document.querySelector('.bg-logo');

var converter = new showdown.Converter({
    tables: true
});


window.addEventListener('load', () => {
    setTimeout(() => {
        chatbot.classList.add('loaded');
        setTimeout(() => {
            if (chats.innerHTML.trim() !== '') {
                chatbot.classList.add('new');
                const firstChat = chats.querySelector('.message.bot');
                if (firstChat && total_messages < 2) {
                    const firstChatLogo = firstChat.querySelector('img');
                    const rect = firstChatLogo.getBoundingClientRect();
                    const translateX = rect.left - bg_logo.offsetLeft;
                    const translateY = rect.top - bg_logo.offsetTop;
                    bg_logo.style.transform = `translate(${translateX - 30}px, ${translateY - 70}px) scale(.44)`;
                }

                setTimeout(() => {
                    window.scrollBy(0, document.body.scrollHeight * 1000000);
                }, 400)
            }
        }, 1000)
    }, 2000);
});

document.getElementById('menu-btn').addEventListener('click', () => {
    document.getElementById('menu').classList.toggle('show');
})

function submitData() {
    const total_messages = chats.querySelectorAll('.message').length;
    const userMessage = input_box.value;

    if (userMessage.trim() !== '') {
        chatbot.classList.add('new');
        const message = document.createElement('div');
        const botResponse = document.createElement('div');

        message.classList.add('message', 'user');
        botResponse.classList.add('message', 'bot', 'no-code');
        message.innerHTML = converter.makeHtml(userMessage);

        if (chats.innerHTML.trim() === '') {
            botResponse.innerHTML = '<img style="opacity:0" src=\'/assets/icons/r_logo.png\'/>\n<p>Loading ... </p>';
        } else {
            botResponse.innerHTML = '<img src=\'/assets/icons/r_logo.png\'/>\n<p>Loading ....  </p>';
        }

        setTimeout(() => {
            botResponse.querySelector('p').innerHTML = getResponse(userMessage);
            formatCode();
            window.scrollBy(0, document.body.scrollHeight * 1000000);
        }, 1000);

        input_box.rows = 1;
        input_box.value = '';
        input_box.innerHTML = '';

        chats.appendChild(message);
        chats.appendChild(botResponse);

        const firstChat = chats.querySelector('.message.bot');
        if (firstChat && total_messages < 2) {
            const firstChatLogo = firstChat.querySelector('img');
            const rect = firstChatLogo.getBoundingClientRect();
            const translateX = rect.left - bg_logo.offsetLeft;
            const translateY = rect.top - bg_logo.offsetTop;
            bg_logo.style.transform = `translate(${translateX - 30}px, ${translateY - 70}px) scale(.44)`;
        }

        setTimeout(() => {
            window.scrollBy(0, document.body.scrollHeight * 1000000);
        }, 400)
    } else {
        input_box.rows = 1;
        input_box.value = '';
        input_box.innerHTML = '';
    }
};



function clearChat() {
    chats.innerHTML = '';
    chatbot.classList.remove('new');
    bg_logo.style.transform = `none`;
}

input_box.addEventListener('keydown', function (event) {
    const maxRows = 8;
    
    if (event.shiftKey && event.key === 'Enter') {
        event.preventDefault();
        const currentRows = parseInt(input_box.getAttribute('rows'), 10);
        if (currentRows < maxRows) {
            input_box.rows = Math.min(currentRows + 1, maxRows);
        }
        const cursorPos = input_box.selectionStart;
        input_box.value = input_box.value.slice(0, cursorPos) + '\n' + input_box.value.slice(cursorPos);
        input_box.setSelectionRange(cursorPos + 1, cursorPos + 1);
    } else if (event.key === 'Enter') {
        event.preventDefault();
        submitData();
    }
});

input_box.addEventListener('input', () => {
    input_box.rows = 1;

    if (input_box.value.trim() !== '') {
        const maxRows = 8;
        input_box.rows = Math.min(Math.floor(input_box.scrollHeight / input_box.clientHeight), maxRows);
    }
});

document.addEventListener('keydown', function (event) {
    if (event.key === '/') {
        event.preventDefault();
        input_box.focus();
    }
});


function getResponse(message) {
    var response = 'Bot response to your message: \n' + message;
    html = converter.makeHtml(response);
    return html
}

function formatCode() {
    document.querySelectorAll('.message.bot.no-code code').forEach((originalCode) => {
        originalCode.parentElement.parentElement.parentElement.classList.remove('no-code');
        const codeText = originalCode.textContent.trim();
        const codeBlockDiv = document.createElement('div');
        codeBlockDiv.classList.add('code-block');
  
        const copyButton = document.createElement('button');
        copyButton.classList.add('copy-btn');
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.onclick = () => copyCode(copyButton);
  
        const preElement = document.createElement('pre');
        const codeElement = document.createElement('code');
        codeElement.textContent = codeText;
  
        preElement.appendChild(codeElement);
        codeBlockDiv.appendChild(copyButton);
        codeBlockDiv.appendChild(preElement);
  
        originalCode.replaceWith(codeBlockDiv);
        
    });
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
    const firstChat = chats.querySelector('.message.bot');
    if (firstChat && chats.querySelectorAll('.message').length < 3) {
        const firstChatLogo = firstChat.querySelector('img');
        const rect = firstChatLogo.getBoundingClientRect();
        const translateX = rect.left - bg_logo.offsetLeft;
        const translateY = rect.top - bg_logo.offsetTop;
        bg_logo.style.transform = `translate(${translateX - 30}px, ${translateY - 40}px) scale(.44)`;
    }
}

function copyCode(button) {
    const codeBlock = button.nextElementSibling.querySelector('code');
    const codeText = codeBlock.textContent;

    navigator.clipboard.writeText(codeText).then(() => {
        alert('Code copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy code: ', err);
    });
}

document.querySelector('.send-btn').addEventListener('click', submitData);