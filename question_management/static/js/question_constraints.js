function displayErrorMessage(message, event){
    alert(message);
    console.log('comign to display message function')
    event.preventDefault(); //don't allow the submission to go through
}