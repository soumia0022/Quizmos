import {pollState} from "./poll_state.js";
export function clean_up_code_mirror(){
    if (pollState.answerCodeEditor) {
        pollState.answerCodeEditor = null;
    }
}