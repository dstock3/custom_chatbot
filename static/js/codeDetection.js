const assistantMessages = document.querySelectorAll(".assistant-message");

assistantMessages.forEach((message) => {
  if (message.innerHTML.includes("%%%CODE_START%%%")) {
    const codeSplit = message.innerHTML.split("%%%CODE_START%%%");
    const codeEndSplit = codeSplit[1].split("%%%CODE_END%%%");

    const codeContainer = document.createElement("div");
    codeContainer.classList.add("assistant-code");
    codeContainer.innerHTML = codeEndSplit[0];

    const messageOne = document.createElement("span");
    messageOne.innerHTML = codeSplit[0];

    const messageTwo = document.createElement("span");
    messageTwo.innerHTML = codeEndSplit[1];

    message.innerHTML = "";

    message.appendChild(messageOne);
    message.appendChild(codeContainer);
    message.appendChild(messageTwo);
  }
});