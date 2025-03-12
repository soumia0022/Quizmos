let isSpeaking = false;
let utterance;

function toggleSpeech() {
    if (isSpeaking) {
        window.speechSynthesis.cancel(); // Stop speech
        document.getElementById("ttsButton").innerText = "🔊 Read Aloud";
        isSpeaking = false;
    } else {
        let text = document.body.innerText; // Get full page text
        let speech = new SpeechSynthesisUtterance(text);
        speech.lang = "en-GB"; // Use British English
        speech.rate = 1.0; // Adjust speed (0.5 - 2)

        speech.onend = function() {
            isSpeaking = false;
            document.getElementById("ttsButton").innerText = "🔊 Read Aloud";
        };

        window.speechSynthesis.speak(speech);
        document.getElementById("ttsButton").innerText = "⏹ Stop Reading";
        isSpeaking = true;
    }
}

function speakSelectedText() {
    let selectedText = window.getSelection().toString().trim();

    if (!selectedText) {
        alert("Please select some text to read.");
        return;
    }

    if (isSpeaking) {
        window.speechSynthesis.cancel(); // Stop speaking
        document.getElementById("ttsSelectedButton").innerText = "🔊 Read Selection";
        isSpeaking = false;
    } else {
        utterance = new SpeechSynthesisUtterance(selectedText);
        utterance.lang = "en-GB";
        utterance.rate = 1.0;

        utterance.onend = function () {
            isSpeaking = false;
            document.getElementById("ttsSelectedButton").innerText = "🔊 Read Selection";
        };

        window.speechSynthesis.speak(utterance);
        document.getElementById("ttsSelectedButton").innerText = "⏹ Stop Reading";
        isSpeaking = true;
    }
}
