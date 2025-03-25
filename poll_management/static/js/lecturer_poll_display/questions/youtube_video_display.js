export function youtube_video_display(embedURL){
    return `
       <div class="video-container">
        <iframe 
            width="560" 
            height="315" 
            src="${embedURL}" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
    </div>
    `;
}