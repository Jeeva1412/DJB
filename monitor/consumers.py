from channels.generic.websocket import AsyncWebsocketConsumer
import base64
import cv2
import numpy as np
from django.core.files.base import ContentFile
from .models import ScreenStream
import os
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

class ScreenStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.client_id = self.scope['url_route']['kwargs'].get('id')
        await self.channel_layer.group_add("screen_stream", self.channel_name)
        await self.accept()

        self.fps = 20
        self.video_writer = None
        self.temp_video_path = f"screen_stream_temp_{self.client_id}.mp4"
        logger.info(f"Client connected: {self.client_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("screen_stream", self.channel_name)

        try:
            # Release the video writer if initialized
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None

            # Save video to database if video file exists
            if os.path.exists(self.temp_video_path):
                await self.save_video_to_db(self.temp_video_path)
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
        finally:
            # Ensure temporary video file cleanup
            if os.path.exists(self.temp_video_path):
                os.remove(self.temp_video_path)
                logger.info(f"Temporary file cleaned up: {self.temp_video_path}")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            # Send frame to group
            await self.channel_layer.group_send(
                "screen_stream",
                {
                    "type": "send_frame",
                    "frame": base64.b64encode(bytes_data).decode("utf-8"),
                },
            )

            # Decode frame and initialize video writer
            frame = np.frombuffer(bytes_data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if self.video_writer is None:
                height, width, _ = frame.shape
                self.video_writer = cv2.VideoWriter(
                    self.temp_video_path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (width, height)
                )

            # Write frame to video writer
            if self.video_writer:
                self.video_writer.write(frame)

        except Exception as e:
            logger.error(f"Error receiving frame: {e}")

    async def send_frame(self, event):
        try:
            await self.send(text_data=event["frame"])
        except Exception as e:
            logger.error(f"Error sending frame: {e}")

    @sync_to_async
    def save_video_to_db(self, video_path):
        """
        Saves the temporary video file to the database and deletes the file.
        """
        try:
            # Read the video file
            with open(video_path, 'rb') as f:
                video_data = f.read()

            # Create a ContentFile and assign a proper name
            video_filename = f"{self.client_id}_video.mp4"
            content_file = ContentFile(video_data, name=video_filename)

            # Create a ScreenStream instance and save the video
            screen_stream = ScreenStream.objects.create(client_id=self.client_id, video=content_file)
            logger.info(f"Video successfully saved to database with ID: {screen_stream.id}")

        except Exception as e:
            logger.error(f"Error saving video to database: {e}")
        finally:
            # Ensure cleanup of the temporary file
            if os.path.exists(video_path):
                os.remove(video_path)
                logger.info(f"Temporary video file removed: {video_path}")
