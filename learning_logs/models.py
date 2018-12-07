from django.db import models

class Topic(models.Model):
    """Temat, który użytkownik aktualnie studiuje"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Zwróć string reprezentujący model"""
        return self.text
