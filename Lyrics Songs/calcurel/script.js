let currentInput = '';
let operator = '';
let previousInput = '';
let shouldResetDisplay = false;
let prankTriggered = false;

const display = document.getElementById('result');

function updateDisplay(value) {
    display.value = value;
}

function appendToDisplay(value) {
    if (display.classList.contains('lyrics-mode')) {
        return; 
    }
    
    if (shouldResetDisplay) {
        currentInput = '';
        shouldResetDisplay = false;
    }
    
    if (value === '.' && currentInput.includes('.')) {
        return; 
    }
    
    currentInput += value;
    updateDisplay(currentInput);
}

function clearDisplay() {
    if (!prankTriggered) {
       
        prankTriggered = true;
        triggerPrank();
    } else {
      
        currentInput = '';
        operator = '';
        previousInput = '';
        shouldResetDisplay = false;
        updateDisplay('0');
    }
}

function deleteLast() {
    if (display.classList.contains('lyrics-mode')) return;
    
    if (currentInput.length > 0) {
        currentInput = currentInput.slice(0, -1);
        updateDisplay(currentInput || '0');
    }
}

function setOperator(op) {
    if (display.classList.contains('lyrics-mode')) return;
    
    if (currentInput === '') return;
    
    if (operator !== '' && previousInput !== '') {
        calculate();
    }
    
    operator = op;
    previousInput = currentInput;
    currentInput = '';
    shouldResetDisplay = true;
}

function calculate() {
    if (display.classList.contains('lyrics-mode')) return;
    
    if (operator === '' || previousInput === '' || currentInput === '') {
        return;
    }
    
    const prev = parseFloat(previousInput);
    const current = parseFloat(currentInput);
    let result;
    
    switch (operator) {
        case '+': result = prev + current; break;
        case '-': result = prev - current; break;
        case '*': result = prev * current; break;
        case '/':
            if (current === 0) {
                updateDisplay('Error');
                return;
            }
            result = prev / current;
            break;
        default: return;
    }
    
    result = Math.round(result * 100000000) / 100000000;
    
    currentInput = result.toString();
    operator = '';
    previousInput = '';
    shouldResetDisplay = true;
    updateDisplay(currentInput);
}

function triggerPrank() {
    display.classList.add('lyrics-mode');
    playMusic();
    displayLyricsWithDelay();
    
    currentInput = '';
    operator = '';
    previousInput = '';
    shouldResetDisplay = false;
}

function playMusic() {
    const audio = new Audio();
    audio.src = 'music.mp3'; 
    audio.volume = 0.7; 
    audio.loop = false; 
    audio.currentTime = 252; 
    
    audio.addEventListener('loadedmetadata', () => {
        audio.currentTime = 252; 
    });
    
    audio.play().catch(error => {
        console.log('Could not play music:', error);
        playFallbackTone();
    });
    
    window.currentAudio = audio;
}

function playFallbackTone() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const notes = [440, 523, 659, 523, 440, 523, 659, 523]; 
        let noteIndex = 0;
        
        function playNote() {
            if (noteIndex < notes.length) {
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.frequency.setValueAtTime(notes[noteIndex], audioContext.currentTime);
                gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                
                oscillator.start();
                oscillator.stop(audioContext.currentTime + 0.4);
                
                noteIndex++;
                setTimeout(playNote, 500);
            }
        }
        
        playNote();
    } catch (error) {
        console.log('Fallback audio not available:', error);
    }
}

function displayLyricsWithDelay() {
    const lyrics = [ 
        "OOooohhhhhhhhhhhh",
        "Nandito ako",
        "Umiibig sayo",
        "Kahit na",
        "Nagdurugo ang puso",
        "At kung sakaling",
        "Iwanan ka niya",
        "Huwag kang mag alala",
        "May nagmamahal sayo",
        "Nandito akoooooooooooooo"
    ];
    
    let currentLine = 0;
    let currentChar = 0;
    let displayText = "";
    
    function displayNextChar() {
        if (currentLine < lyrics.length) {
            const currentLyric = lyrics[currentLine];
            
            if (currentChar < currentLyric.length) {
                displayText += currentLyric[currentChar];
                updateDisplay(displayText);
                currentChar++;
                setTimeout(displayNextChar, 170); 
            } else {
                setTimeout(() => {
                    displayText = "";
                    updateDisplay(displayText);
                    currentLine++;
                    currentChar = 0;
                    setTimeout(displayNextChar, 135); 
                }, 900); 
            }
        } else {
            setTimeout(() => {
                display.classList.remove('lyrics-mode');
                updateDisplay('0');
            }, 1000);
        }
    }
    
    displayNextChar();
}

document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if (key >= '0' && key <= '9' || key === '.') {
        appendToDisplay(key);
    } else if (key === '+' || key === '-' || key === '*' || key === '/') {
        setOperator(key);
    } else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculate();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    } else if (key === 'Backspace') {
        deleteLast();
    }
});

updateDisplay('0');
