document.addEventListener("DOMContentLoaded", function () {
            const questionTypeDropdown = document.getElementById("question-type-dropdown");
            const timerSettings = document.getElementById("timer-settings");
            const timerDiv = document.getElementById("timer");

            // Show Timer Input Only for Relevant Question Types
            questionTypeDropdown.addEventListener("change", function () {
                    timerSettings.style.display = "block";

            });
        });

        document.addEventListener("DOMContentLoaded", function () {
            const questionTypeDropdown = document.getElementById("question-type-dropdown");
            const mediaButtons = document.getElementById("media-buttons");
            const videoOptions = document.getElementById("video-options");
            const audioFields = document.getElementById("audio-upload-field");
            const videoFields = document.getElementById("video-upload-field");
            const youtubeFields = document.getElementById("youtube-url-field");
            const imageFields = document.getElementById("image-upload-field");
            const addAudioBtn = document.getElementById("add-audio-btn");
            const addVideoBtn = document.getElementById("add-video-btn");
            const addImageBtn = document.getElementById("add-image-btn");
            const uploadVideoBtn = document.getElementById("upload-video-btn");
            const addYoutubeBtn = document.getElementById("add-youtube-btn");
            const audioFileInput = document.querySelector("input[name='audio_file']");
            const videoFileInput = document.querySelector("input[name='video_file']");
            const imageFileInput = document.querySelector("input[name='image_file']");
            const youtubeLinkInput = document.querySelector("input[name='youtube_link']");
            const resetMediaBtn = document.getElementById("reset-media-btn");


            questionTypeDropdown.addEventListener("change", function () {
                const selectedType = questionTypeDropdown.value;
                mediaButtons.style.display = selectedType ? "block" : "none";
                audioFields.style.display = "none";
                videoFields.style.display = "none";
                youtubeFields.style.display = "none";
                imageFields.style.display = "none";
                addAudioBtn.disabled = false;
                addVideoBtn.disabled = false;
                addImageBtn.disabled = false;
                uploadVideoBtn.disabled = false;
                addYoutubeBtn.disabled = false;
            });



            // Show audio upload field and hide other media options
            addAudioBtn.addEventListener("click", function () {
                audioFields.style.display = "block";
                videoFields.style.display = "none";
                imageFields.style.display = "none";
                youtubeFields.style.display = "none";
                videoOptions.style.display = "none";
            });

            // Show video options and hide other media options
            addVideoBtn.addEventListener("click", function () {
                audioFields.style.display = "none";
                videoOptions.style.display = "block";
                imageFields.style.display = "none";
                youtubeFields.style.display = "none";
            });

            // Show video upload field and hide YouTube URL field
            uploadVideoBtn.addEventListener("click", function () {
                videoFields.style.display = "block";
                youtubeFields.style.display = "none";
            });

            // Show YouTube URL field and hide video upload field
            addYoutubeBtn.addEventListener("click", function () {
                youtubeFields.style.display = "block";
                videoFields.style.display = "none";
            });

            // Show image options and hide other media options
            addImageBtn.addEventListener("click", function () {
                audioFields.style.display = "none";
                videoOptions.style.display = "none";
                imageFields.style.display = "block";
                youtubeFields.style.display = "none";
            });

            // Disable other media options once an audio file is uploaded
            audioFileInput.addEventListener("change", function () {
                if (audioFileInput.files.length > 0) {
                    addVideoBtn.disabled = true;
                    uploadVideoBtn.disabled = true;
                    addImageBtn.disabled = true;
                    addYoutubeBtn.disabled = true;
                }
                // Can change allowed types based on what can be implemented when embedding
                validateFileInput(audioFileInput, ["audio/mpeg", "audio/wav", "audio/ogg", "audio/flac", "audio/mp4", "audio/x-m4a"]);
            });

            // Disable other media options once a video file is uploaded
            videoFileInput.addEventListener("change", function () {
                if (videoFileInput.files.length > 0) {
                    addAudioBtn.disabled = true;
                    addVideoBtn.disabled = true;
                    addImageBtn.disabled = true;
                    addYoutubeBtn.disabled = true;
                }
                // Can change allowed types based on what can be implemented when embedding
                validateFileInput(videoFileInput, ["video/mp4", "video/avi", "video/quicktime", "video/x-msvideo", "video/x-matroska", "video/x-flv", "video/x-ms-wmv"]);
            });

            // Disable other media options once an image file is uploaded
            imageFileInput.addEventListener("change", function () {
                if (imageFileInput.files.length > 0) {
                    addVideoBtn.disabled = true;
                    uploadVideoBtn.disabled = true;
                    addAudioBtn.disabled = true;
                    addYoutubeBtn.disabled = true;
                }
                // Can change allowed types based on what can be implemented when embedding
                validateFileInput(imageFileInput, ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/tiff", "image/webp", "image/svg+xml"]);
            });


            youtubeLinkInput.addEventListener("change", function(e) {
                addVideoBtn.disabled = true;
                addAudioBtn.disabled = true;
                addImageBtn.disabled = true;
                uploadVideoBtn.disabled = true;

                // Validation to ensure a valid URL is entered for the YouTube link
                const urlPattern = /^(https?:\/\/)/;
                if (!urlPattern.test(youtubeLinkInput.value)) {
                    alert("Please enter a valid URL (must start with http:// or https://)");
                    e.preventDefault();
                }

            });

            // Validation for audio and video files (disallow certain types)
            function validateFileInput(input, allowedTypes) {
                if (input.files.length > 0) {
                    let file = input.files[0];
                    let fileType = file.type;
                    let fileName = file.name.toLowerCase();

                    // Check MIME type
                    if (!allowedTypes.includes(fileType)) {
                        alert("Invalid file type! Please upload a valid file.");
                        return;
                    }
                }
            }

            resetMediaBtn.addEventListener("click", function() {
                addVideoBtn.disabled = false;
                addAudioBtn.disabled = false;
                addImageBtn.disabled = false;
                addYoutubeBtn.disabled = false;
                uploadVideoBtn.disabled = false;

                audioFileInput.value = '';
                videoFileInput.value = '';
                imageFileInput.value = '';
                youtubeLinkInput.value = '';

            });

    });