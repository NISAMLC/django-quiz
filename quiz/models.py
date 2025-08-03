from django.db import models


# Model for Quiz Set (like Intro to Python)
class QuizSet(models.Model):
    name = models.CharField(max_length=200)  # Quiz name
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name


# Model for Question
class Question(models.Model):
    quiz_set = models.ForeignKey(QuizSet, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    # Store the correct option number (1, 2, 3, or 4)
    correct_option = models.IntegerField(choices=[
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
    ])

    def __str__(self):
        return f"{self.quiz_set.name} - {self.question_text[:50]}"
