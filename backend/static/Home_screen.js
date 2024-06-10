document.addEventListener('DOMContentLoaded', () => {
    const menu_btn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const threads = document.getElementById('Recent_btns');
    const HS1 = document.getElementById('HS1');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const newchat = document.getElementById('New_chat');
    

    var lastThread;
    var last_threadId;

    menu_btn.addEventListener('click',function()  {
        if (sidebar.style.transform === "translateX(-300px)") {
            sidebar.style.transform = "translateX(0px)";
            menu_btn.style.transform = "rotate(90deg)";
        } 
        else if(sidebar.style.transform === "translateX(0px)"){
            sidebar.style.transform = "translateX(-300px)"
            menu_btn.style.transform = "rotate(0deg)"
        }
        else {
            sidebar.style.transform = "translateX(0px)";
        }
    });

    function fetchThreads() {
        fetch('/threads')
            .then(response => response.json())
            .then(data => {
                threads.innerHTML = ''; // Clear the threads list before appending new ones
                data.threads_list.forEach(thread  => {
                    const button = document.createElement('button');
                    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");

                    svg.setAttribute('viewBox', '0 0 24 24');
                    svg.setAttribute('fill', 'currentColor');
                    svg.setAttribute('class', 'w-6 h-6');

                    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    path.setAttribute('fill-rule', 'evenodd');
                    path.setAttribute('d', "M9 4.5a.75.75 0 0 1 .721.544l.813 2.846a3.75 3.75 0 0 0 2.576 2.576l2.846.813a.75.75 0 0 1 0 1.442l-2.846.813a3.75 3.75 0 0 0-2.576 2.576l-.813 2.846a.75.75 0 0 1-1.442 0l-.813-2.846a3.75 3.75 0 0 0-2.576-2.576l-2.846-.813a.75.75 0 0 1 0-1.442l2.846-.813A3.75 3.75 0 0 0 7.466 7.89l.813-2.846A.75.75 0 0 1 9 4.5ZM18 1.5a.75.75 0 0 1 .728.568l.258 1.036c.236.94.97 1.674 1.91 1.91l1.036.258a.75.75 0 0 1 0 1.456l-1.036.258c-.94.236-1.674.97-1.91 1.91l-.258 1.036a.75.75 0 0 1-1.456 0l-.258-1.036a2.625 2.625 0 0 0-1.91-1.91l-1.036-.258a.75.75 0 0 1 0-1.456l1.036-.258a2.625 2.625 0 0 0 1.91-1.91l.258-1.036A.75.75 0 0 1 18 1.5ZM16.5 15a.75.75 0 0 1 .712.513l.394 1.183c.15.447.5.799.948.948l1.183.395a.75.75 0 0 1 0 1.422l-1.183.395c-.447.15-.799.5-.948.948l-.395 1.183a.75.75 0 0 1-1.422 0l-.395-1.183a1.5 1.5 0 0 0-.948-.948l-1.183-.395a.75.75 0 0 1 0-1.422l1.183-.395c.447-.15.799-.5.948-.948l.395-1.183A.75.75 0 0 1 16.5 15Z")
                    path.setAttribute('clip-rule', 'evenodd');
                    svg.appendChild(path);

                    button.appendChild(svg);

                 
                    let parts = thread[0].id.split('_');
                    let lastFourValues = parts[parts.length - 1].slice(-4);
                    console.log(lastFourValues);
                    button.appendChild(document.createTextNode("thread_"+lastFourValues));

                    button.addEventListener('click', () => loadThread(thread[0].id));
                    threads.appendChild(button);
                
                });
            });
    }

    function addMessage(sender, message) {
        const lines = message.split('\n');
        const messageDiv = document.createElement('div');
        messageDiv.className = sender;
        for (let line of lines) {
            const lineDiv = document.createElement('div');
            lineDiv.textContent = line;
            messageDiv.appendChild(lineDiv);
        }
        HS1.appendChild(messageDiv);
        HS1.scrollTop = HS1.scrollHeight;
    }


    function loadThread(threadId) {
        HS1.innerHTML = '';
        last_threadId = threadId;
        fetch(`/threads/${threadId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                data.messages.forEach(msg => {
                    addMessage(msg.sender, msg.content);
                });
            });
        }

    fetchThreads();

    function addCurrentMessage(sender, message, threadId) {
        console.log(threadId);
        const lines = message.split('\n');
        const messageDiv = document.createElement('div');
        if (sender === 'assistant' && threadId === last_threadId) {
            messageDiv.className = 'assistant';
            for (let line of lines) {
                const lineDiv = document.createElement('div');
                lineDiv.textContent = line;
                messageDiv.appendChild(lineDiv);
            }
            HS1.appendChild(messageDiv);
            HS1.scrollTop = chat.scrollHeight;
        }
    }

    sendBtn.addEventListener('click', () => {
        const message = userInput.value;
        if (message.trim() !== '') {
            addMessage('user', message);
            sendBtn.disabled = true;
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, threadId: last_threadId })
            })
            .then(response => response.json())
            .then(data => {
                addCurrentMessage('assistant', data.response, data.threadId);
                sendBtn.disabled = false;
            })
            .catch(error => {
                console.error('Error:', error);
                sendBtn.disabled = false;
            });
            userInput.value = '';
        }
    });

    newchat.addEventListener('click', () => {
        createThread().then(lastThread => {
            console.log(lastThread);
            fetchThreads();
        });
    });

    async function createThread() {
        const response = await fetch(`/add_thread`);
        const data = await response.json();
        lastThread = data;
        last_threadId = lastThread.id;
        return lastThread.id;
    }


    const profile = document.getElementById('profile');
    const profile_menu = document.querySelector('.profile_menu');

    profile.addEventListener('click',function(){
        if(profile_menu.style.right === "-160px"){
            profile_menu.style.right = "30px";
        }
        else {
            profile_menu.style.right = "-160px";
        }
    });

    profile.addEventListener('mouseover',function(){
        if(profile_menu.style.right === "-160px"){
            profile_menu.style.right = "30px";
        }
        else {
            profile_menu.style.right = "-160px";
        }
    });


    const profile_btn = document.getElementById('profile_btn');
    profile_btn.addEventListener('click',function(){
        window.location.href = "/profile_page";
    })


    const Upgrade_btn = document.getElementById('Upgrade_btn');
    const upgrade_menu = document.getElementById('upgrade_monthly');
    const close_btn = document.getElementById('upgrade_close_btn');
    const body = document.querySelector('body');

    Upgrade_btn.addEventListener('click',function(){
        upgrade_menu.style.display = "block";
        body.style.backgroundColor = "";
    });

    close_btn.addEventListener('click',function(){
        upgrade_menu.style.display = "none";
    });


    const plan_btns = document.querySelectorAll('.plan_btn');
    const Monthly_plan = document.getElementById('Monthly_plan');
    const Yearly_plan = document.getElementById('Yearly_plan'); 
    const monthly_info = document.getElementById('priceInfo');
    const price_tag = document.getElementById('price_tag');
    const time_p = document.getElementById('time_p');
    const elements = document.querySelectorAll('.upgrade_main > .plans> button');


    plan_btns.forEach(function(plan_btn) { 
        plan_btn.addEventListener('click', function() { 
        elements.style.Color = "#F65434";   
        });
    });

    Monthly_plan.addEventListener('click',function(){
        price_tag.textContent = "5";
        time_p.textContent = "per month";
    });

    Yearly_plan.addEventListener('click',function(){
        price_tag.textContent = "60";
        time_p.textContent = "annually, billed $5 per month";
    });


    const Search_btn = document.getElementById('searchButton');
    const parentmain = document.getElementById('main_screen');
    console.log(parentmain);   

    var isFirstTime = true;

    Search_btn.addEventListener('click',function(){
        var query = document.getElementById('searchInput').value;
        if(query) {
            var parentElemant = document.getElementById('HS1');
            if(isFirstTime){
                console.log(query, parentElemant);
                parentElemant.textContent = query;
                isFirstTime = false;
            }
            else {
                var newElement = document.createElement('p');
                newElement.textContent = query;
                parentElemant.appendChild(newElement);
            }
        }
        
    });
});