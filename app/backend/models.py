from django.db import models

# Create your models here.
class Questions(models.Model):
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    grade = models.IntegerField()
    subject = models.CharField(max_length=100)
    questionText = models.TextField()
    optionA = models.CharField(max_length=200)
    optionB = models.CharField(max_length=200)
    optionC = models.CharField(max_length=200)
    optionD = models.CharField(max_length=200)
    correctAnswer = models.CharField(max_length=1, choices=ANSWER_CHOICES, blank=True, null=True)
    explanation = models.TextField(help_text="Explanation for the correct answer", blank=True, null=True, default="")
    explanationVoice = models.FileField(upload_to='audio/explanations/', blank=True, null=True, help_text="Audio file with text-to-speech version of the explanation")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['grade', 'subject']

    def __str__(self):
        return f"Grade {self.grade} {self.subject}: {self.questionText[:50]}..."

    def get_correct_option_text(self):
        """Returns the text of the correct answer option"""
        option_map = {
            'A': self.optionA,
            'B': self.optionB,
            'C': self.optionC,
            'D': self.optionD,
        }
        return option_map.get(self.correctAnswer, '')

