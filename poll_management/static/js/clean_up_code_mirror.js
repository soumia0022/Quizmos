export function clean_up_code_mirror(pollState){
    if (pollState.answerCodeEditor) {
        pollState.answerCodeEditor = null;
    }
}