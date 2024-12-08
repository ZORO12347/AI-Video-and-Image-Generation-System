from fastapi import FastAPI, HTTPException, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
from database_manager import DatabaseManager
from content_generator import ContentGeneratorWithNotifications

# Initialize FastAPI app
app = FastAPI()

# Directories and static files
BASE_CONTENT_DIR = "generated_content"
if not os.path.exists(BASE_CONTENT_DIR):
    os.makedirs(BASE_CONTENT_DIR)
app.mount("/static", StaticFiles(directory=BASE_CONTENT_DIR), name="static")

# Initialize database and content generator
db = DatabaseManager()
generator = ContentGeneratorWithNotifications()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Helper function to normalize static file paths
def normalize_path(path):
    return f"/static/{os.path.relpath(path, BASE_CONTENT_DIR).replace(os.sep, '/')}"

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    """
    Display a form for user login and content prompt submission.
    """
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, user_id: str = Form(...), prompt: str = Form(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Handle form submission for content generation.
    """
    # Log the login attempt
    print(f"User {user_id} logged in.")

    # Check if content already exists
    user_content = db.fetch_user_content(user_id)
    if user_content and user_content[-1]["status"] == "Completed":
        return await content_page(request, user_id)

    # Trigger content generation
    background_tasks.add_task(generator.generate_content, user_id, prompt)
    return templates.TemplateResponse("processing.html", {"request": request, "user_id": user_id})

@app.get("/content/{user_id}", response_class=HTMLResponse)
async def content_page(request: Request, user_id: str):
    """
    Display generated content for the user.
    """
    user_content = db.fetch_user_content(user_id)
    if not user_content:
        raise HTTPException(status_code=404, detail="No content found for this user.")
    latest_record = user_content[-1]

    # Check the status
    if latest_record["status"] != "Completed":
        return templates.TemplateResponse("processing.html", {"request": request, "user_id": user_id})

    # Get generated images and videos
    videos = json.loads(latest_record["video_paths"])
    images = json.loads(latest_record["image_paths"])
    normalized_videos = [normalize_path(path) for path in videos]
    normalized_images = [normalize_path(path) for path in images]

    # Log the content view
    print(f"User {user_id} viewed their content.")

    return templates.TemplateResponse(
        "content.html",
        {"request": request, "user_id": user_id, "videos": normalized_videos, "images": normalized_images}
    )

@app.get("/content/{user_id}", response_class=HTMLResponse)
async def content_page(request: Request, user_id: str):
    print(f"Fetching content for user_id: {user_id}")
    user_content = db.fetch_user_content(user_id)
    print(f"Content fetched: {user_content}")
    if not user_content:
        raise HTTPException(status_code=404, detail="No content found for this user.")
    latest_record = user_content[-1]
    print(f"Latest record: {latest_record}")


