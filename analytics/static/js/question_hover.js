$(document).ready(function() {
    console.log('Document ready, setting up hover popup.');

    $('#hover-popup-box').appendTo('body').css({
        'position': 'absolute',
        'z-index': 1000,
        'display': 'none'
    });

    $('.question-text').hover(
        function() {
            console.log('Hover entered on question-text.');
            var questionItem = $(this).closest('.question-item');
            var questionId = questionItem.data('question-id'); 
            console.log('Question ID:', questionId);
            var popup = $('#hover-popup-box');
            var questionActions = questionItem.find('.question-actions');
            var textElement = $(this);

            $.get(`/questions/question/${questionId}/preview/`)
                .done(function(data) {
                    console.log('AJAX GET success, data received:', data);
                    popup.html(`
                        <div class="popup-content">
                            <div>Type: ${data.question_type}</div>
                            <div>Timer: ${data.question_timer || 'None'}</div>
                        </div>
                    `);
                    if (questionActions.length === 0) {
                        console.warn('No .question-actions element found for question ID:', questionId);
                    }
                    var actionsRect = questionActions.get(0).getBoundingClientRect();
                    var textRect = textElement.get(0).getBoundingClientRect();
                    console.log('Text rect:', textRect, 'Actions rect:', actionsRect);
                    popup.css({
                        display: 'block',
                        top: textRect.top + $(window).scrollTop() + textElement.outerHeight() / 2 - popup.outerHeight() / 2,
                        left: actionsRect.left + $(window).scrollLeft(),
                        width: questionActions.outerWidth()
                    });
                })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    console.error('AJAX GET failed:', textStatus, errorThrown);
                });
        },
        function() {
            $('#hover-popup-box').css('display', 'none');
            console.log('Hover left on question-text, hiding popup.');
        }
    );

    $('.view-full-btn').click(function() {
       var questionId = $(this).data('question-id');
       window.location.href = `/questions/question/${questionId}/`;
    });
});
