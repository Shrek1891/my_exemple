const arr = Array(9).fill(0);
const gameBoard = document.querySelector('#gameBoard');
let step = 2;
const title = document.querySelector('#player');
const reset = document.querySelector('#reset');
const winCombinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
];
let indexArrayPlayer = [];
let indexArrayComputer = [];

const checkWin = (winCombinations, indexArray) => {
    if (winCombinations.some(combination => combination.every(index => indexArray.includes(index)))) {
        return winCombinations.find(combination => combination.every(index => indexArray.includes(index)));
    }
}

const setWinner = (name, winCombination, color = 'green') => {
    title.textContent = `${name} won!!!`;
    title.style.color = color;
    gameBoard.style.pointerEvents = 'none';
    gameBoard.style.opacity = '0.5';
    reset.style.opacity = '1';
    reset.style.pointerEvents = 'all';
    reset.style.cursor = 'pointer';
    if (winCombination) {
        winCombination.forEach(index => {
            const div = gameBoard.querySelector(`[data-n="${index}"]`);
            div.style.backgroundColor = 'yellow';
        });
    }
    reset.addEventListener('click', () => {
        window.location.reload();
    })
}

const turn_of_player = (index, array, name, winComb, opponent) => {
    array.push(index);
    let isWin = checkWin(winComb, array);
    if (isWin) {
        setWinner(name, isWin);
        return
    }
    title.textContent = opponent;
    return array;
}


arr.forEach((item, index) => {
        const div = document.createElement('div');
        div.setAttribute('data-n', index.toString());
        gameBoard.appendChild(div);
    }
)
gameBoard.addEventListener('click', (e) => {
        const n = +e.target.getAttribute('data-n');
        if (arr[n] !== 0) return;
        arr[n] = step;
        e.target.textContent = 'X'
        indexArrayPlayer = turn_of_player(n, indexArrayPlayer, 'Player ', winCombinations, 'Computer');
        if (indexArrayPlayer.length + indexArrayComputer.length === 9) {
            setWinner('Nobody', [], 'red');
            return;
        }
        computerMove(arr)

    }
)

// Computer's turn after player's turn

function checkWinner(board) {
    for (let i = 0; i < winCombinations.length; i++) {
        const [a, b, c] = winCombinations[i];
        if (board[a] && board[a] === board[b] && board[a] === board[c]) {
            return {winner: board[a], pattern: winCombinations[i]};
        }
    }
    return board.includes('') ? null : {winner: 'Tie', pattern: null};
}

//part of computer's move
function computerMove(arr) {
    const computerMove = bestMove(arr);
    arr[computerMove] = 1; // Mark computer's move
    const div = document.querySelector(`[data-n="${computerMove}"]`);
    div.textContent = '0';
    indexArrayComputer = turn_of_player(computerMove, indexArrayComputer, 'Computer', winCombinations, 'Player 1');

}

function bestMove(board) {
    let isFindingWinningMove = false;
    for (let i = 0; i < 9; i++) {
        if (board[i] === 0) {
            board[i] = 2;
            let res = checkWinner(arr);
            if (res && res.winner === 2) {
                isFindingWinningMove = true;
                return i; // Blocking move found
            }
            board[i] = 0; // Undo move
        }
    }
    for (let i = 0; i < 9; i++) {
        if (board[i] === 0) {
            board[i] = 1; // Computer's move
            if (checkWinner(board)?.winner === 1) {
                isFindingWinningMove = true;
                return i; // Winning move found
            }
            board[i] = 0; // Undo move
        }
    }

    if (!isFindingWinningMove) {
        while (true) {
            const randomIndex = Math.floor(Math.random() * 9);
            if (board[randomIndex] === 0) {
                return randomIndex;
            }
        }
    }

}








