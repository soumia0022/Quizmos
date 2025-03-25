export function audio_file_display(question){
    return `
    <div class="audio-container mb-3">
      <audio 
        controls
        class="w-100"
        style="max-width: 640px;"
      >
        <source src="${question.audio_file}" type="audio/mpeg">
        Your browser does not support the audio element.
      </audio>
    </div>
    `;
}