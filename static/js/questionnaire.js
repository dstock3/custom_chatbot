const questionsDataElement = document.querySelector("#questions-data");
console.log(questionsDataElement);
const questions = JSON.parse(questionsDataElement.value);

const sections = Object.keys(questions);
const totalQuestions = Object.values(questions).flat().length;
const progressBar = document.querySelector("#progress-bar");
const nextButton = document.querySelector("#next-button");
let currentSectionIndex = 0;
let currentQuestionIndex = 0;

nextButton.addEventListener("click", handleNextClick);

function handleNextClick() {
    const currentSection = document.querySelector(`#${sections[currentSectionIndex]}-section`);
    const currentSectionQuestions = currentSection.querySelectorAll(".question-container");

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
        // When all questions are answered, submit the form
        document.querySelector("form").submit();
    }
}

function renderQuestion() {
    const currentSection = document.querySelector(`#${sections[currentSectionIndex]}-section`);
    const currentSectionQuestions = currentSection.querySelectorAll(".question-container");

    currentSection.style.display = "block";
    currentSectionQuestions[currentQuestionIndex].style.display = "block";
    updateProgressBar();
}

function updateProgressBar() {
    const progress = (Object.values(questions).slice(0, currentSectionIndex).flat().length + currentQuestionIndex) / totalQuestions * 100;
    progressBar.style.width = `${progress}%`;
}

renderQuestion();