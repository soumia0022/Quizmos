// index.js - This is the main entry point that ties everything together
import { QuestionManager } from './questions.js';
import { WebSocketManager } from './websocket.js';
import { PollUI } from './ui.js';

document.addEventListener('DOMContentLoaded', () => {
    // First initialize WebSocket
    const webSocket = new WebSocketManager(pollConfig.code);

    // Then initialize Question Manager with the WebSocket
    const questionManager = new QuestionManager(pollConfig.questions, webSocket);

    // Initialize UI and pass both managers
    const ui = new PollUI(questionManager, webSocket);

    // Start setup
    ui.initialize();
});