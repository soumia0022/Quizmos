export function video_file_display(question){
    html += `
      <div class="video-container mb-3">
        <video 
          controls
          width="100%" 
          style="max-width: 640px;"
          class="rounded"
        >
          <source src="${question.video_file}" type="video/mp4">
          Your browser does not support the video element.
        </video>
      </div>
    `;
    return html;
}