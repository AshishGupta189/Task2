document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInputElement = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const url='http://127.0.0.1:5000/generate-text';


    sendButton.addEventListener("click", function () {
        const userMessage = userInputElement.value;
        if (userMessage) {
            appendUserMessage(userMessage);
            userInputElement.value = "";
            simulateAssistantTyping();
            callAssistantAPI(userMessage);
        }
    });

    async function callAssistantAPI(userMessage) {
        try{
            const response=await fetch(url,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({userMessage}),
            })
            if(response.ok){
                const data=await response.json();
                console.log(data)
                simulateAssistantResponse(data.assistantReply)
            }else{
                console.log("error")
            }

        }catch(error){
            console.log(error)
        }
        
    }
    
        // async function callAssistantAPI(userMessage) {
        //     let response;
        //     try{
        //         console.log("function called");
        //         // Make the API request and handle the response
        //         await fetch(url, {
        //             method: 'POST',
        //             headers: {
        //                 'Content-Type': 'application/json'
        //             },
        //             body: JSON.stringify({ userMessage })
        //         })

        //         // .then(response => {
        //         //     if (!response.ok) {
        //         //         throw new Error('Network response was not ok');
        //         //     }
        //         //     console.log("here")
        //         //     return response.json();
        //         // })
        //         // .then(data => {
        //         //     // Handle the response from the backend
        //         //     console.log("There")
        //         //     simulateAssistantResponse(data.assistantReply); // Here, 'data' contains the response data
        //         // })
        //         // .catch(error => {
        //         //     // Handle any errors that occurred during the fetch
        //         //     console.error('Error:', error);
        //         // })
        //     }catch(error){
        //         console.error('Error:', error);
        //     }
        // }
                
    function appendUserMessage(message) {
        const messageElement = createMessageElement(message, "user-message");
        chatBox.appendChild(messageElement);
    }

    function simulateAssistantTyping() {
        const typingMessage = createTypingMessage();
        chatBox.appendChild(typingMessage);
    }

        function simulateAssistantResponse(assistantReply) {
            console.log("function called response");
                const responseMessage = createAssistantMessage("Assistant: " + assistantReply);        
        }


    function createTypingMessage() {
        return createMessageElement("Assistant is typing...", "assistant-message message-text typing");
    }

    function createAssistantMessage(message) {
        console.log("function called message");
        return createMessageElement(message, "assistant-message");
    }

    function createMessageElement(message, className) {
        console.log("function called");
        const messageElement = document.createElement("div");
        const classNames = className.split(" "); // Split the class name by space
        classNames.forEach(name => {
            messageElement.classList.add(name); // Add each class separately
        });
        console.log("function called");
        messageElement.innerHTML = `<span class="message-text">${message}</span>`;
        return messageElement;
    }

    // function replaceLastTypingWithResponse(responseMessage) {
    //     const typingMessages = document.querySelectorAll(".message-text.typing");
    //     if (typingMessages.length > 0) {
    //         chatBox.replaceChild(responseMessage, typingMessages[typingMessages.length - 1].parentNode);
    //     }
    // }
});

