$(document).ready(function() {
    // DOM elements and form validation code...

    // Handle hover for preview
    $('.question-item').hover(function() {
        const questionId = $(this).data('id');
        const popup = $('#hover-popup-box');
        $.get(`/questions/question/${questionId}/preview/`, function(data) {
            popup.html(`
                <div class="border rounded p-3">
                    <p>Type: ${data.question_type}</p>
                    <p>Timer: ${data.timer || 'None'}</p>
                </div>
            `);
            const offset = $(this).offset();
            popup.css({
                display: 'block',
                top: offset.top + $(this).outerHeight() / 2 - popup.outerHeight(), // Center vertically relative to the question
                left: offset.left - popup.outerWidth() - 10
            });
        }.bind(this));
    }, function() {
        $('#hover-popup-box').css('display', 'none');
    });

    // Handle click for full page view
    $('.view-full-btn').click(function() {
        const questionId = $(this).data('id');
        window.location.href = `/questions/question/${questionId}/`;
    });
});