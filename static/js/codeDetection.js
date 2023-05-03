const assistantMessages = document.querySelectorAll(".assistant-message");

assistantMessages.forEach((message) => {
  if (message.innerHTML.includes("%%%CODE_START%%%")) {
    const codeSplit = message.innerHTML.split("%%%CODE_START%%%");
    const codeEndSplit = codeSplit[1].split("%%%CODE_END%%%");

    const codeContainer = document.createElement("div");
    codeContainer.classList.add("assistant-code");

    codeContainer.innerHTML = codeEndSplit[0];

    message.innerHTML = codeSplit[0] + codeEndSplit[1];

    message.appendChild(codeContainer);
  }
});