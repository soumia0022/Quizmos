export function createLockOverlay() {
    if (document.getElementById('poll-lock-overlay')) {
        return; // Already exists
    }

    const overlay = document.createElement('div');
    overlay.id = 'poll-lock-overlay';
    overlay.className = 'poll-lock-overlay';
    overlay.innerHTML = `
        <div class="lock-message">
            <i class="fas fa-lock lock-icon"></i>
            <h3>This question is locked</h3>
            <p>Please wait for the lecturer to unlock responses</p>
            <button id="close-overlay-btn" class="close-btn">Close</button>
        </div>
    `;

    // Initially hidden
    overlay.style.display = 'none';
    document.body.appendChild(overlay);

    // Add CSS for the lock overlay
    const style = document.createElement('style');
    style.textContent = `
        .poll-lock-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(5px);
            z-index: 1000;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .lock-message {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 400px;
        }

        .lock-icon {
            font-size: 3rem;
            color: #dc3545;
            margin-bottom: 1rem;
        }

    `;
    document.head.appendChild(style);

    // Close button functionality
    overlay.querySelector('#close-overlay-btn').addEventListener('click', () => {
        showLockOverlay();
    });
}

function showLockOverlay() {
    const overlay = document.getElementById('poll-lock-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

function hideLockOverlay() {
    const overlay = document.getElementById('poll-lock-overlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

window.showLockOverlay = showLockOverlay;
window.hideLockOverlay = hideLockOverlay;


