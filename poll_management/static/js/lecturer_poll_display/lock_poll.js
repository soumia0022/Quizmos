import { pollState } from '../poll_state.js'

export function unlock() {
    const unlockButton = document.getElementById("unlock");
    const lockButton = document.getElementById("lock");

    if (unlockButton.style.display == "") {
        lockButton.style.display = "";
        unlockButton.style.display = "none";


        pollState.lecturer_webSocket.send(JSON.stringify({
            type: 'poll_status',
            action: 'unlock'
        }));
    }
}

function lock() {
    const lockButton = document.getElementById("lock");
    const unlockButton = document.getElementById("unlock");

    if (lockButton.style.display == "") {
        lockButton.style.display = "none";
        unlockButton.style.display = "";


        pollState.lecturer_webSocket.send(JSON.stringify({
            type: 'poll_status',
            action: 'lock'
        }));
    }
}

window.lock = lock;
window.unlock = unlock;