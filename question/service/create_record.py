from question.models import Question, Answer, Comment


class CreateInstance:
    def __init__(self, user, model, data):
        self.user = user
        self.model = model
        self.data = data
        self.obj = None

    def decide_to_create(self):
        if self.model == Question:
            self.create_question()
        elif self.model == Answer:
            self.create_answer()
        elif self.model == Comment:
            self.create_comment()

    def create_question(self):

        self.obj = Question.objects.create(
            user=self.user,
            title=self.data['title'],
            # description=self.data['description']
        )
        return self.obj

    def create_answer(self):
        self.obj = Answer.objects.create(

        )

    def create_comment(self):
        self.obj = Comment.objects.create(

        )
