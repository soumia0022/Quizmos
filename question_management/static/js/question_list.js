$(document).ready(function(){
    $('.question-item').hover(
        function() {
            const questionId = $(this).data('id');
            $.get(`/question/${questionId}/preview/`, function(data) {
                $('#preview-box').html(`
                    <p>Type: ${data.question_type}</p>
                    <p>Timer: ${data.timer || 'None'}</p>
                    <p>Text: ${data.question_text}</p>
                `);
            });
        },
        function() {
            $('#preview-box').empty();
        }
    );

    $('.question-item').click(function(){
        const questionId = $(this).data('id');
        window.location.href = `/question/${questionId}/`;
    });
});
