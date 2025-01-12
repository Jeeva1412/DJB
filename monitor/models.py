from django.db import models

class ScreenStream(models.Model):
    client_id = models.CharField(max_length=255,null=True)  # Store client ID
    video = models.FileField(upload_to='videos/',null=True)  # Video file path
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the video was created

    def __str__(self):
        return f"Video for client {self.client_id} created at {self.created_at}"
