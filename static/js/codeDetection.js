const assistantMessages = document.querySelectorAll(".assistant-message");

assistantMessages.forEach((message) => {
  if (message.innerHTML.includes("%%%CODE_START%%%")) {
    const codeSplit = message.innerHTML.split("%%%CODE_START%%%");
    const codeEndSplit = codeSplit[1].split("%%%CODE_END%%%");
    
    const languaageSplit = message.innerHTML.split("%%%LANGUAGE_START%%%");
    const languageEndSplit = languaageSplit[1].split("%%%LANGUAGE_END%%%");

    const language = languageEndSplit[0];
    
    const codeContainer = document.createElement("pre");
    codeContainer.classList.add("assistant-code");
    codeContainer.innerHTML = codeEndSplit[0];

    const codeBlockHeader = document.createElement("div");
    codeBlockHeader.classList.add("assistant-code-header");
    codeBlockHeader.innerHTML = language;
    codeContainer.prepend(codeBlockHeader);

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