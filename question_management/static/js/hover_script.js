$(document).ready(function() {
    $('#hover-popup-box').appendTo('body').css({
        'position': 'absolute',
        'z-index': 1000,
        'display': 'none'
    });

    $('.question-text').hover(function() {
        var questionItem = $(this).closest('.question-item');
        var questionId = questionItem.data('id');
        var popup = $('#hover-popup-box');
        var questionActions = questionItem.find('.question-actions');
        var textElement = $(this);
        $.get(`/questions/question/${questionId}/preview/`, function(data) {
            popup.html(`
                <div class="popup-content">
                    <div>Type: ${data.question_type}</div>
                    <div>Timer: ${data.question_timer || 'None'}</div>
                </div>
            `);
            var actionsRect = questionActions.get(0).getBoundingClientRect();
            var textRect = textElement.get(0).getBoundingClientRect();
            popup.css({
                display: 'block',
                top: textRect.top + $(window).scrollTop() + textElement.outerHeight()/2 - popup.outerHeight()/2,
                left: actionsRect.left + $(window).scrollLeft(),
                width: questionActions.outerWidth()
            });
        });
    }, function() {
        $('#hover-popup-box').css('display', 'none');
    });

    $('.view-full-btn').click(function() {
        var questionId = $(this).data('id');
        window.location.href = `/questions/question/${questionId}/`;
    });
});
