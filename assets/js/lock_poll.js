function unlock(){
    const unlockButton = document.getElementById("unlock");
    const lockButton = document.getElementById("lock");
    if (unlockButton.style.display == ""){
        lockButton.style.display = "";
        unlockButton.style.display = "none";
    }

}

function lock() {
    const lockButton = document.getElementById("lock");
    const unlockButton = document.getElementById("unlock");

    if (lockButton.style.display == ""){
        lockButton.style.display = "none";
        unlockButton.style.display = "";
    }

}


