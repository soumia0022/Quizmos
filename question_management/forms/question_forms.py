# from django import forms
# from question_management.models.question_models import Question
#
#
# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = [
#             'question_text', 'question_type', 'text_fill_question', 'text_fill_answer',
#             'dropdown_fill_question', 'dropdown_options', 'multiple_choice_question',
#             'multiple_choice_options', 'multiple_choice_answers', 'single_choice_question',
#             'single_choice_option', 'single_choice_answers', 'wordcloud_question', 'match_question',
#             'match_options', 'match_answers', 'timer', 'audio_file', 'video_file', 'youtube_link'
#         ]
#
#     def clean_audio_file(self):
#         audio_file = self.cleaned_data.get('audio_file')
#         if audio_file and not audio_file.name.endswith(('.mp3', '.wav', '.aac', '.ogg', '.flac')): # Can change these based on what can be embedded
#             raise forms.ValidationError("Invalid audio file format. Supported formats: mp3, wav, aac, ogg, flac.") # Style this
#         return audio_file
#
#     def clean_video_file(self):
#         video_file = self.cleaned_data.get('video_file')
#         if video_file and not video_file.name.endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv')):
#             raise forms.ValidationError("Invalid video file format. Supported formats: mp4, avi, mov, wmv, flv.")
#         return video_file
#
#     def clean_youtube_link(self):
#         youtube_link = self.cleaned_data.get('youtube_link')
#         if youtube_link and not youtube_link.startswith(('http://', 'https://')):
#             raise forms.ValidationError("Invalid URL format for YouTube link.")
#         return youtube_link
#
