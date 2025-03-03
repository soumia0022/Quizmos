from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from response_management.models.response_model import (
    MatchQuestionResponse, MultipleChoiceResponse,
    SingleChoiceResponse, DropdownFillResponse, TextFillResponse, 
    WordCloudResponse 
)
from poll_management.models.poll_model import Poll
from question_management.models.question_models import Question
#await: is like the waiter saying "I need to wait for the kitchen to finish this order, but I'll serve other tables while waiting"
#async: is like a waiter saying "I'm going to be serving multiple tables"
class PollConsumer(AsyncWebsocketConsumer):
    # This consumer handles WebSocket connections for a polling system
    students_joined = {}
    poll_lock_status = {}  # Track lock status for each poll

    async def connect(self):
        try:
            #extract the poll_code from the URL route
            self.poll_code = self.scope['url_route']['kwargs']['poll_code']
            # since the poll code is unique, we wil create a group name for this poll
            # so that all clients can receive updates
            self.poll_group_name = f'poll_{self.poll_code}'
        except Exception as e:
            print(f"Error extracting poll code: {e}")

        self.poll = await self.get_poll(self.poll_code)

        if self.poll_code not in self.students_joined:
            self.students_joined[self.poll_code] = 0

        # Initialize lock status for this poll if not already set
        if self.poll_code not in self.poll_lock_status:
            self.poll_lock_status[self.poll_code] = True

        if not self.poll:
            await self.close()
            return
        # Add this connection to the poll group - this allows broadcasting to all connected users
        await self.channel_layer.group_add(
            self.poll_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        # Send message when a student connects
        if self.scope["user"].role == 'Student':
            self.students_joined[self.poll_code] += 1
            await self.channel_layer.group_send(
                self.poll_group_name,
                {
                    'type': 'new_student',
                    'message': f'{self.students_joined[self.poll_code]}'
                })

        # Send current lock status to the new connection
        await self.send(text_data=json.dumps({
            'type': 'poll_status',
            'action': 'lock' if self.poll_lock_status[self.poll_code] else 'unlock'
        }))

    async def disconnect(self, close_code):
        # When a client disconnects, remove them from the poll group
        if self.scope["user"].role == 'Student':
            self.students_joined[self.poll_code] -= 1
            await self.channel_layer.group_send(
                self.poll_group_name,
                {
                    'type': 'new_student',
                    'message': f'{self.students_joined[self.poll_code]}'
                })
        await self.channel_layer.group_discard(
            self.poll_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # This handles incoming messages from clients
        # Parse the JSON data received
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        message_content = text_data_json.get('message')
        question_id = text_data_json.get('question_id')

        if message_type == 'new_student':

            await self.channel_layer.group_send(
                self.poll_group_name,
                {"type": "new_student", "message": message_content}
            )
        elif message_type == 'poll_status':
            # Handle poll lock/unlock requests (from lecturer)
            if self.scope["user"].role == 'Lecturer':  # Only lecturers can lock/unlock
                action = text_data_json.get('action')
                if action in ['lock', 'unlock']:
                    # Update lock status
                    self.poll_lock_status[self.poll_code] = (action == 'lock')

                    # Broadcast to all clients in the group
                    await self.channel_layer.group_send(
                        self.poll_group_name,
                        {
                            'type': 'poll_status_update',
                            'action': action
                        }
                    )
        elif message_type == 'get_poll_status':
            # Send current poll lock status to the requester
            await self.send(text_data=json.dumps({
                'type': 'poll_status',
                'action': 'lock' if self.poll_lock_status[self.poll_code] else 'unlock'
            }))
        elif message_type == 'question':
            # If it's a question, fetch it from the database and broadcast it
            questions = await self.get_all_questions()
            total_questions = len(questions)
            # Find the index of the requested question
            question = await self.get_question(question_id)
            # Calculating question_number with type conversion
            question_number = None
            for i, q in enumerate(questions):
                # Convert question_id to integer to match q.id's type
                if int(q.id) == int(question_id):
                    question_number = i + 1
                    break

            if question:
                await self.channel_layer.group_send(
                    self.poll_group_name,
                    {
                        "type": "poll_question",
                        "question": question,
                        "question_number": question_number,
                        "total_questions": total_questions
                    }
                )
        elif message_type == 'response':
            # Check if poll is locked before saving responses (for students)
            if self.scope["user"].role == 'Student' and self.poll_lock_status[self.poll_code] == False:
                # If poll is locked, reject the response
                await self.send(text_data=json.dumps({
                    'type': 'response_status',
                    'success': False,
                    'message': 'Poll is currently locked'
                }))
                return

            # Handle different types of responses
            success = await self.save_response(
                text_data_json.get('question_id'),
                text_data_json.get('response_type'),
                text_data_json.get('response_data')
            )
            # Notify the sender about the response status
            await self.send(text_data=json.dumps({
                'type': 'response_status',
                'success': success
            }))
            # Broadcast the response
            if success:
                await self.channel_layer.group_send(
                    self.poll_group_name,
                    {
                        'type': 'response_update',
                        'question_id': text_data_json.get('question_id'),
                        'response_type': text_data_json.get('response_type'),
                        'user': self.scope["user"].username
                    }
                )

    async def new_student(self, event):
        # Handler for sending regular messages back to the WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'new_student',
            'message': message
        }))

    async def poll_message(self, event):
        # Handles broadcasting messages to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message']
        }))

    async def poll_status_update(self, event):
        # Handler for broadcasting poll lock/unlock status
        await self.send(text_data=json.dumps({
            'type': 'poll_status',
            'action': event['action']
        }))

    async def poll_question(self, event):
        # Handler for sending questions back to the WebSocket
        question = event['question']
        question_number = event.get('question_number', None)
        total_questions = event.get('total_questions', None)

        await self.send(text_data=json.dumps({
            'type': 'question',
            'question': question,
            'question_number': question_number,
            'total_questions': total_questions
        }))

    @database_sync_to_async
    def get_question(self, question_id):
        # Database query to fetch question details
        # Decorated with database_sync_to_async because database operations are synchronous
        try:
            question = Question.objects.get(id=question_id)
            dropdown_options = question.dropdown_options.split(',') if question.dropdown_options else []
            match_options = question.match_options
            match_answers = question.match_answers
            return {
                'id': question.id,
                'text': question.question_text,
                'type': question.question_type,
                'mcq_options': question.multiple_choice_options,
                'single_option': question.single_choice_option,
                'dropdown_options': dropdown_options,
                'match_options': match_options,
                'match_answers': match_answers,

                'wordcloud_question': question.wordcloud_question,


                'dropdown_correct_answer': question.dropdown_correct_answer,
                'question_timer': question.question_timer,
            }
        except Question.DoesNotExist:
            return None

    @database_sync_to_async
    def get_poll(self, poll_code):
        try:
            return Poll.objects.get(number_code=poll_code)
        except Poll.DoesNotExist:
            return None

    @database_sync_to_async
    def save_response(self, question_id, response_type, response_data):
        try:
            question = Question.objects.get(id=question_id)

            response_models = {
                'match_question': (MatchQuestionResponse, 'match_responses'),
                'multiple_choice': (MultipleChoiceResponse, 'selected_options'),
                'single_choice': (SingleChoiceResponse, 'selected_option'),
                'dropdown_fill': (DropdownFillResponse, 'selected_option'),
                'text_fill': (TextFillResponse, 'answer_text'),
                'wordcloud': (WordCloudResponse, 'word_cloud_response') 
            }

            if response_type not in response_models:
                return False

            ResponseModel, field_name = response_models[response_type]

            # Create response object
            response_data = {
                'user': self.scope['user'],
                'poll': self.poll,
                'question': question,
                field_name: response_data
            }

            # check if response already exists
            existing_response = ResponseModel.objects.filter(
                user=self.scope['user'],
                poll=self.poll,
                question=question
            ).first()

            if existing_response:
                # update existing response
                setattr(existing_response, field_name, response_data[field_name])
                existing_response.save()
            else:
                # create new response
                ResponseModel.objects.create(**response_data)

            return True

        except Exception as e:
            print(f"Error saving response: {e}")
            return False

    async def response_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'response_update',
            'question_id': event['question_id'],
            'response_type': event['response_type'],
            'user': event['user']
        }))

    @database_sync_to_async
    def get_all_questions(self):
        return list(Question.objects.filter(poll=self.poll))