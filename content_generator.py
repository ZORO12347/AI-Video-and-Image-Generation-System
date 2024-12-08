import os
import shutil
import requests
from dotenv import load_dotenv
from database_manager import DatabaseManager
from notifications import NotificationManager

# Load environment variables
load_dotenv()


class ContentGeneratorWithNotifications:
    def __init__(self):
        self.db = DatabaseManager()
        self.notifier = NotificationManager()
        self.unsplash_api_key = os.getenv("UNSPLASH_API_KEY")
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")

    def generate_images(self, prompt, output_dir, count=5):
        """
        Generate images using the Unsplash API.
        """
        os.makedirs(output_dir, exist_ok=True)
        image_paths = []
        for i in range(count):
            response = requests.get(
                f"https://api.unsplash.com/photos/random",
                headers={"Authorization": f"Client-ID {self.unsplash_api_key}"},
                params={"query": prompt}
            )
            if response.status_code == 200:
                image_url = response.json()["urls"]["regular"]
                file_path = os.path.join(output_dir, f"image_{i + 1}.jpg")
                with open(file_path, "wb") as img_file:
                    img_file.write(requests.get(image_url).content)
                image_paths.append(file_path)
            else:
                raise Exception(f"Image API Error: {response.status_code}")
        return image_paths

    def generate_videos(self, prompt, output_dir, count=5):
        """
        Generate distinct videos using Pexels API.
        """
        os.makedirs(output_dir, exist_ok=True)
        video_paths = []

        # Fetch multiple videos in one request
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": f"{self.pexels_api_key}"},
            params={"query": prompt, "per_page": count}
        )

        if response.status_code == 200:
            videos = response.json().get("videos", [])

            # Check if enough videos were returned
            if len(videos) < count:
                raise Exception(f"Not enough videos returned by Pexels API. Only {len(videos)} found.")

            # Save distinct videos
            for i, video in enumerate(videos[:count]):
                video_url = video["video_files"][0]["link"]  # Assuming the first file is preferred
                file_path = os.path.join(output_dir, f"video_{i + 1}.mp4")
                with open(file_path, "wb") as video_file:
                    video_file.write(requests.get(video_url).content)
                video_paths.append(file_path)
        else:
            raise Exception(f"Video API Error: {response.status_code}")

        return video_paths

    def generate_content(self, user_id, prompt):
        """
        Generate images and videos for the user and update the database.
        """
        try:
            # Create user-specific directories
            user_dir = os.path.join("generated_content", user_id)
            shutil.rmtree(user_dir, ignore_errors=True)
            os.makedirs(user_dir, exist_ok=True)

            # Generate content
            image_dir = os.path.join(user_dir, "images")
            video_dir = os.path.join(user_dir, "videos")
            images = self.generate_images(prompt, image_dir)
            videos = self.generate_videos(prompt, video_dir)

            # Update database
            record_id = self.db.insert_generation_record(user_id, prompt)
            self.db.update_generation_status(record_id, videos, images)

            # Notify user
            self.notifier.send_email(
                recipient="user@example.com",
                subject="Your AI Content is Ready!",
                body=f"Hello {user_id},\nYour content for the prompt '{prompt}' is ready."
            )
        except Exception as e:
            print(f"Error generating content: {e}")
            raise
