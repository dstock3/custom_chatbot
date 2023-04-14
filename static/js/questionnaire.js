const questionsDataElement = document.querySelector("#questions-data");
const questions = JSON.parse(questionsDataElement.value);
const sections = Object.keys(questions);
const totalQuestions = Object.values(questions).flat().length;
const progressBar = document.querySelector("#progress-bar");
const nextButton = document.querySelector("#next-button");
const submitButton = document.querySelector("#submit-button");
let currentSectionIndex = 0;
let currentQuestionIndex = 0;

nextButton.addEventListener("click", handleNextClick);

function handleNextClick() {
    const currentSection = document.querySelector(`#${sections[currentSectionIndex]}-section`);
    const currentSectionQuestions = currentSection.querySelectorAll(".question-container");
    let questionProgInput = document.getElementById("questionProg");
    questionProgInput.value = parseInt(questionProgInput.value) + 1;

    currentSectionQuestions[currentQuestionIndex].style.display = "none";
    currentQuestionIndex++;

    if (currentQuestionIndex >= currentSectionQuestions.length) {
        currentSection.style.display = "none";
        currentSectionIndex++;
        currentQuestionIndex = 0;
    }
    
    if (currentSectionIndex < sections.length) {
        renderQuestion();
    } else {
        submitButton.style.display = "block";
    }
}

const renderQuestion = () => {
    const currentSection = document.querySelector(`#${sections[currentSectionIndex]}-section`);
    const currentSectionQuestions = currentSection.querySelectorAll(".question-container");
    const currentSectionHeading = document.querySelector(`.section-head-container h3:nth-child(${currentSectionIndex * 2 + 1})`);


    // remove active class from previous section heading
    const previousSectionHeading = document.querySelector(`.section-head-container h3.active-section`);
    if (previousSectionHeading) {
        previousSectionHeading.classList.remove('active-section');
    }

    currentSection.style.display = "block";
    currentSectionQuestions[currentQuestionIndex].style.display = "flex";
    currentSectionQuestions[currentQuestionIndex].style.flexDirection = "column";
    currentSectionHeading.classList.add('active-section'); // add active class to current section heading

    updateProgressBar();
}

const updateProgressBar = () => {
    let questionProg = parseInt(document.getElementById("questionProg").value);
    let progress = questionProg / totalQuestions * 100;
    progressBar.style.width = `${progress}%`;
}

renderQuestion();