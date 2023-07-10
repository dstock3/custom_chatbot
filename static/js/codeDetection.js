const assistantMessages = document.querySelectorAll(".assistant-message");

assistantMessages.forEach((message) => {
  if (message.innerHTML.includes("%%%CODE_START%%%")) {
    const codeSplit = message.innerHTML.split("%%%CODE_START%%%");
    const codeEndSplit = codeSplit[1].split("%%%CODE_END%%%");
    
    const codeContainer = document.createElement("pre");
    codeContainer.classList.add("assistant-code");

    const codeSubContainer = document.createElement("code");
    codeSubContainer.classList.add("assistant-code-sub");
    const code = codeEndSplit[0];
    codeSubContainer.textContent = code;
    codeContainer.appendChild(codeSubContainer);

    if (message.innerHTML.includes("%%%LANGUAGE_START%%%")) {
      const languageSplit = message.innerHTML.split("%%%LANGUAGE_START%%%");
      const languageEndSplit = languageSplit[1].split("%%%LANGUAGE_END%%%");
      const language = languageEndSplit[0];

      const codeBlockHeader = document.createElement("div");
      codeBlockHeader.classList.add("assistant-code-header");

      const codeBlockHeaderText = document.createElement("div");
      codeBlockHeaderText.textContent = language;
      codeBlockHeaderText.classList.add("assistant-code-header-text");
      codeBlockHeader.appendChild(codeBlockHeaderText);

      const codeBlockMinimize = document.createElement("div");
      codeBlockMinimize.classList.add("assistant-code-header-minimize");
      codeBlockMinimize.textContent = "-";

      codeBlockMinimize.addEventListener("click", () => {
        codeContainer.classList.toggle("assistant-code-minimized");
        codeSubContainer.style.display = codeContainer.classList.contains("assistant-code-minimized") ? "none" : "block";
        codeBlockMinimize.textContent = codeContainer.classList.contains("assistant-code-minimized") ? "+" : "-";
      });
      codeBlockHeader.appendChild(codeBlockMinimize);
      codeContainer.prepend(codeBlockHeader);
    }

    const spanStartIndex = codeSplit[0].indexOf("<span>");
    const spanEndIndex = codeSplit[0].indexOf("</span>") + 7;
    const messageOneContent = codeSplit[0].substring(spanStartIndex, spanEndIndex);

    const messageOne = document.createElement("span");
    messageOne.innerHTML = messageOneContent;

    const messageTwoContent = codeSplit[0].substring(spanEndIndex);
    const messageTwo = document.createElement("span");
    messageTwo.innerHTML = messageTwoContent;

    message.innerHTML = "";
    
    message.appendChild(messageOne);
    message.appendChild(messageTwo);
    message.appendChild(codeContainer);
  }
});