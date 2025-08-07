from django.db import models # type: ignore

class Topic(models.Model):
    """um assunto sobre o qual usuario esta aprendendo."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Devolve uma apresentação em string do modelo."""
        return self.text

class Entry(models.Model):
    """algo específico aprendido sobre um assunto."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Devolve uma apresentação em string do modelo."""
        return self.text[:50] + "..."