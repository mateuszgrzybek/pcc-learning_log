from django.db import models

class Topic(models.Model):
    """Temat, który użytkownik aktualnie studiuje"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Zwróć string reprezentujący model"""
        return self.text

class Entry(models.Model):
    """Coś konkretnego czego użytkownik nauczył się na dany temat"""
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Zwróć string reprezentujący model"""
        if len(self.text) <= 50:
            return self.text
        else:
            return self.text[:50] + "..."
