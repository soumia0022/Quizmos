export class PollUI {
  constructor(questionManager, webSocket) {
    this.questionManager = questionManager;
    this.webSocket = webSocket;
    this.bindEvents();
  }

   initialize() {
        this.bindEvents();
        this.initQRCode();
        this.setupCopyUrl();
    }

    bindEvents() {
        // Poll control buttons
        document.getElementById('start-poll-btn').addEventListener('click', () => {
            document.getElementById('start-poll-btn').style.display = 'none';
            document.getElementById('question-display').style.display = 'block';
            this.questionManager.updateDisplay();
        });

        document.getElementById('prev-btn').addEventListener('click', () => {
            this.questionManager.previous();
        });

        document.getElementById('next-btn').addEventListener('click', () => {
            this.questionManager.next();
        });
    }

    initQRCode() {
        // QR code magnification
        const magnify = document.getElementById('magnify');
        const qrOverlay = document.getElementById('qrOverlay');
        const close = document.getElementById('close');

        magnify.addEventListener('click', () => {
            qrOverlay.style.display = 'flex';
        });

        close.addEventListener('click', () => {
            qrOverlay.style.display = 'none';
        });
    }

    setupCopyUrl() {
        const copyBtn = document.getElementById('copy-url-btn');
        copyBtn.addEventListener('click', () => {
            const urlInput = document.getElementById('join-url-input');
            urlInput.select();
            document.execCommand('copy');
            copyBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyBtn.textContent = 'Copy';
            }, 2000);
        });
    }



}