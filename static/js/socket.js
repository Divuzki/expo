const socket = io("http://localhost:8000");

const alertBox = document.getElementById("alert-box"),
  messagesBox = document.getElementById("messages-box"),
  messageInput = document.getElementById("message-input"),
  sendBtn = document.getElementById("send-btn"),
  receiver = document.querySelector(".me_ohh");

if (sendBtn) {
  socket.on("welcome", (msg) => {
    console.log(msg);
    sendBtn.classList.add("me_ohh");
  });

  const handleAlerts = (msg, type) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `;
    setTimeout(() => {
      alertBox.innerHTML = "";
    }, 5000);
  };

  socket.on("welcome2", (msg) => {
    handleAlerts(msg, "primary");
  });
  socket.on("byebye", (msg) => {
    handleAlerts(msg, "danger");
  });

  sendBtn.addEventListener("click", () => {
    const message = messageInput.value;
    messageInput.value = "";

    socket.emit("message", message);
  
  });

  socket.on("messageToClients", (msg) => {
    console.log(msg);
    messagesBox.innerHTML += `
      <section class="sm:w-4/6 w-5/6">
            <div class="flex m-8 ml-1 break-words sm:break-all w-full">
              <img src="./img.jpg" class="w-8 h-8 sticky top-2 rounded-full m-3">
              <div class="p-3 bg-gray-100 shadow rounded-tl-lg rounded-tr-lg rounded-br-lg">
              <div class="text-sm">Divine Ikhuoria</div>
              <div class="text-xs text-gray-600">${msg}</div>
              <div class="text-gray-400" style="font-size: 8pt">
                8 minutes ago
              </div>
            </div>
          </div>
          </section>
    `;
  });
}