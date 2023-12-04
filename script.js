const startButton = document.getElementById('start-btn')
const nextButton = document.getElementById('next-btn')
const results = document.getElementById('results-container')
const questionContainerElement = document.getElementById('question-container')
const questionElement = document.getElementById('question')
const answerButtonsElement = document.getElementById('answer-buttons')
var score = document.getElementById('score')
var total = document.getElementById('total')
var wrongQ = document.getElementById('wrong-questions')

let shuffledQuestions, currentQuestionIndex, score_value

startButton.addEventListener('click', startGame)
nextButton.addEventListener('click', () => {
  currentQuestionIndex++
  setNextQuestion()
})

function startGame() {
  results.classList.add('hide')
  startButton.classList.add('hide')
  shuffledQuestions = questions.sort(() => Math.random() - .5)
  currentQuestionIndex = 0
  score_value = 0
  wrongQ.textContent = null
  questionContainerElement.classList.remove('hide')
  setNextQuestion()
}

function setNextQuestion() {
  resetState()
  showQuestion(shuffledQuestions[currentQuestionIndex])
}

function showQuestion(question) {
  questionElement.innerText = question.question
  question.answers.forEach(answer => {
    const button = document.createElement('button')
    button.innerText = answer.text
    button.classList.add('btn')
    if (answer.correct) {
      button.dataset.correct = answer.correct
    }
    button.addEventListener('click', selectAnswer)
    answerButtonsElement.appendChild(button)
  })
}

function resetState() {
  clearStatusClass(document.body)
  nextButton.classList.add('hide')
  results.classList.add('hide')
  while (answerButtonsElement.firstChild) {
    answerButtonsElement.removeChild(answerButtonsElement.firstChild)
  }
}

function selectAnswer(e) {
  const selectedButton = e.target
  const correct = selectedButton.dataset.correct
  setStatusClass(document.body, correct)
  Array.from(answerButtonsElement.children).forEach(button => {
    setStatusClass_dup(button, button.dataset.correct)
  })
  if (shuffledQuestions.length > currentQuestionIndex + 1) {
    nextButton.classList.remove('hide')
  } else {
    score_value = score_value
    score.textContent = score_value
    total.textContent = shuffledQuestions.length
    startButton.innerText = 'Restart'
    startButton.classList.remove('hide')
    results.classList.remove('hide')
  }
}

function setStatusClass(element, correct) {
  clearStatusClass(element)
  if (correct) {
    score_value++ 
    element.classList.add('correct')
  } else {
    element.classList.add('wrong')
    wrongQ.innerHTML += (shuffledQuestions[currentQuestionIndex].question + '<br /> <br />')
  }
}
function setStatusClass_dup(element, correct) {
  clearStatusClass(element)
  if (correct) {
    element.classList.add('correct')
  } else {
    element.classList.add('wrong')
  }
}

function clearStatusClass(element) {
  element.classList.remove('correct')
  element.classList.remove('wrong')
}







const questions = [
  {
    question: 'Computational thinking is?',
    answers: [
      { text: 'Programming', correct: false },
      { text: 'Thinking like a computer', correct: false },
      { text: 'Coding', correct: false},
      { text: 'Logically solving problems', correct: true}

    ]
  },
  {
    question: 'Which of these is an example of abstraction?',
    answers: [
      { text: 'The layers in a network protocol stack', correct: false },
      { text: 'Use a pre-written library of procedures and functions to perform operations such as sorting and searching', correct: false },
      { text: 'Ignore the colour of a player token in a snakes ladder game model', correct: false},
      { text: 'Break a complex problem into modules using top down design', correct: false},
      { text: 'Subdividing a problem into smaller tasks that different teams can work on independently', correct: true}
    ]
  },
  {
    question: 'What is taking a complex problem and breaking it down into a series of small more manageable problems called?',
    answers: [
      { text: 'Decomposition', correct: true },
      { text: 'Abstraction ', correct: false },
      { text: 'Pattern Recognition', correct: false },
      { text: 'Algorithms', correct: false }
    ]
  },
  {
    question: 'What is looking at problems individually and considering how similar problems have been solved previously called?',
    answers: [
      { text: 'Decomposition', correct: false },
      { text: 'Abstraction ', correct: false },
      { text: 'Pattern Recognition', correct: true },
      { text: 'Algorithms', correct: false },
      { text: 'Similarity comparity', correct: false }
    ]
  },
  {
    question: 'What is focusing only on the important details, while ignoring irrelevant information called?',
    answers: [
      { text: 'Decomposition', correct: false },
      { text: 'Abstraction ', correct: true },
      { text: 'Pattern Recognition', correct: false },
      { text: 'Algorithms', correct: false },
    ]
  },
  {
    question: 'What is using simple steps or rules to solve each of the smaller problems can be designed called',
    answers: [
      { text: 'Decomposition', correct: false },
      { text: 'Abstraction ', correct: false },
      { text: 'Pattern Recognition', correct: false },
      { text: 'Algorithms', correct: true },
    ]
  },
  {
    question: 'Decomposition makes problems _____?',
    answers: [
      { text: 'Better to code', correct: false },
      { text: 'Harder to solve', correct: false },
      { text: 'More manageable', correct: true },
      { text: 'More recognisable', correct: false }
    ]
  },
  {
    question: 'Which of the following is not a component of computational thinking?',
    answers: [
      { text: 'Abstraction', correct: false },
      { text: 'Decomposition', correct: false },
      { text: 'Pattern recognition/Generalising', correct: false },
      { text: 'Psuedocode', correct: true },
      { text: 'Algorithmic thinking', correct: false }
    ]
  },
  {
    question: 'Define the term abstraction within computational thinking?',
    answers: [
      { text: 'Adding numbers together', correct: false },
      { text: 'Representing real world problems in a computer program, using symbols and removing unnecessary elemen', correct: true },
      { text: 'Taking a real world problem and designing a computer program that exactly replicates every part of that problem in the computer', correct: false },
      { text: 'Performing multiple calculations on a list of variables', correct: false }
    ]
  }
]