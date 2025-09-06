const DEFAULT_TEXT_TYPING_ARRAY = [
    "The sun beat down on the deserted beach. A lone seagull cried overhead, its mournful call echoing across the sand. " +
    "A young woman sat on a weathered driftwood log, sketching in a notebook. She was lost in her own world, oblivious " +
    "to the vastness of the ocean and the secrets it held. She was searching for inspiration, for something to capture " +
    "the essence of this moment, this feeling of solitude and freedom.",
    "The quick brown fox jumps over the lazy dog. This sentence contains all the letters of the English alphabet. " +
    "It is often used in typing tests. Practice makes perfect. Keep practicing and you will improve. The quick brown " +
    "fox jumps over the lazy dog. ",
    "see talk head of long can old only river give two look idea did hear why but as were before use study most but " +
    "follow city again say story study got say he he cut see land until sea miss school much back move line left " +
    "letter want often small animal work state made was learn people the use is line around talk took sometimes " +
    "no school being form this then while second above he all our large open together not mile world they " +
    "leave off been tell new at",
    "Proofreader applicants are tested primarily on their spelling, speed, and skill in finding errors in the sample " +
    "text. Toward that end, they may be given a list of ten or twenty classically difficult words and a proofreading test, " +
    "both tightly timed. The proofreading test will often have a maximum number of errors per quantity of text and " +
    "a minimum amount of time to find them. The goal of this approach is to identify those with the best skill set.",
    "As you embark on your own journey of self-discovery and empowerment, don't forget to extend a helping hand to others. " +
    "Your positive energy and unwavering belief in yourself can be a beacon of hope for those around you. " +
    "Encourage and support your friends, family, and colleagues in their pursuits. Celebrate their successes, " +
    "offer a listening ear during their struggles, and remind them of their own unique talents and potential. " +
    "Remember, the impact of your kindness and encouragement can ripple outward, creating a chain reaction of " +
    "positivity and inspiration."
]

const TEST = [
    'Test text'
]

const randomTextTypingArray = (arr) => {
    const randomIndex = Math.floor(Math.random() * arr.length);
    return arr[randomIndex];
}
const message = document.querySelector('#message');
const randomText = randomTextTypingArray(DEFAULT_TEXT_TYPING_ARRAY);
const containerTextTyping = document.querySelector('#text-to-type');
containerTextTyping.textContent = randomText;
let index = 0
let prevChar = randomText[0];
let isStart = false
let isEnd = false;
let startTime;
const punctuation = [',', '.', '!', '?', '…', ';', ':', '-', '—', '(', ')', '[', ']', '{', '}', '"', "'", '`', " "];
const startButton = document.querySelector('#startButton');

function replaceCharAndColor(element, index, newChar, color, colorBg) {
    let text = element.textContent;
    if (index < 0 || index >= text.length) {
        console.error("Index out of range: " + index);
        return;
    }
    const before = text.slice(0, index);
    const after = text.slice(index + 1);
    const highlightedText = `<span style="color: ${color}; font-weight: bold; background-color: ${colorBg};">${newChar}</span>`;
    const newText = before + highlightedText + after;
    element.innerHTML = newText;
}

function speedTyping(e) {
    if (index == 0) {
        isStart = true;
        startTime = new Date();
    }
    if (e.key === "Alt" || e.key === "Control" || e.key === "Shift" || e.key === "Meta") {
        return;
    }
    if (e.key === randomText[index]) {
        if (index > 0) {
            replaceCharAndColor(containerTextTyping, index - 1, prevChar, 'white', 'transparent');
            prevChar = randomText[index];
        }
        replaceCharAndColor(containerTextTyping, index, e.key.toUpperCase(), 'green', 'transparent');
        index++;
    } else {
        replaceCharAndColor(containerTextTyping, index - 1, prevChar, 'white', 'transparent');
        if (punctuation.includes(randomText[index])) {
            replaceCharAndColor(containerTextTyping, index, randomText[index], 'red', 'red');
        } else {
            replaceCharAndColor(containerTextTyping, index, randomText[index].toUpperCase(), 'red', 'transparent');
        }
    }
}

function game() {
    window.addEventListener('keydown', speedTyping)
}

game();

window.addEventListener('keyup', (e) => {
    if (index === randomText.length) {
        isEnd = true;
        const timeTaken = (new Date() - startTime) / 1000;
        const SPS = (index / timeTaken).toFixed(2);
        message.textContent = "Yooohhoooo! You finished in " + timeTaken + " seconds with a speed of " + SPS + " characters per second.";
        window.removeEventListener('keydown', speedTyping);
        startButton.hidden = false;
    }
})

startButton.addEventListener('click', (e) => {
    e.preventDefault();
    index = 0;
    prevChar = randomText[0];
    isStart = false;
    isEnd = false;
    startTime = null;
    containerTextTyping.textContent = randomText;
    message.textContent = '';
    startButton.hidden = true;
    game();
})


