from django.db import models
from django.conf import settings

# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    cover_image_url = models.URLField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    developer = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
    
class TrackerItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('not_started', 'Not Started'),
            ('playing', 'Playing'),
            ('done', 'Completed'),
            ('dropped', 'Dropped'),
        ],
        default='not_started'
    )
    rating = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.status})"
    
    @property
    def status_color(self):
        status_colors = {
            'not_started': 'secondary',
            'playing': 'primary',
            'done': 'success',
            'dropped': 'danger',
        }
        return status_colors.get(self.status, 'secondary')