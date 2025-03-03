import {ws} from './websocket.js';

function unlock() {
    const unlockButton = document.getElementById("unlock");
    const lockButton = document.getElementById("lock");

    if (unlockButton.style.display == "") {
        lockButton.style.display = "";
        unlockButton.style.display = "none";


        ws.send(JSON.stringify({
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


        ws.send(JSON.stringify({
            type: 'poll_status',
            action: 'lock'
        }));
    }
}


window.lock = lock;
window.unlock = unlock;