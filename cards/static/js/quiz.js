const cards = JSON.parse(document.getElementById('quiz-cards').textContent);

const term = document.getElementById('quiz-term');
const form = document.getElementById('quiz-form');
const answer = document.getElementById('quiz-answer');
const feedback = document.getElementById('quiz-feedback');
const progress = document.getElementById('quiz-progress');
const back = document.getElementById('quiz-back');

let index = 0;
let score = 0;
let checked = false; // true while showing feedback, next Enter moves on

function normalize(text) {
    return text.trim().toLowerCase();
}

function showCard() {
    if (index >= cards.length) {
        term.textContent = `You got ${score} out of ${cards.length}`;
        progress.textContent = '';
        feedback.textContent = '';
        form.style.display = 'none';
        back.style.display = 'inline-block';
        return;
    }

    progress.textContent = `Card ${index + 1} of ${cards.length}`;
    term.textContent = cards[index].term;
    feedback.textContent = '';
    answer.value = '';
    answer.focus();
}

form.addEventListener('submit', (e) => {
    e.preventDefault();

    if (checked) {
        checked = false;
        index++;
        showCard();
        return;
    }

    const card = cards[index];

    if (normalize(answer.value) === normalize(card.definition)) {
        score++;
        feedback.textContent = 'Correct! Press Enter to continue.';
    } else {
        feedback.textContent = `Incorrect, the answer was "${card.definition}". Press Enter to continue.`;
    }

    checked = true;
});

showCard();
