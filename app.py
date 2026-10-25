import os
import json
import shutil
import uvicorn
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from ideas_engine import get_ideas
from image_gen import generate_banner
from ai_brain import generate_ai_post
from publisher import (
    is_authenticated,
    save_cookie_token,
    launch_interactive_login,
    publish_to_linkedin
)

app = FastAPI(title="LinkedIn Autonomous Agent Studio 2.5")

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
REPO_ASSETS_DIR = os.path.join(STATIC_DIR, "repo_assets")

os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(REPO_ASSETS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/generated", StaticFiles(directory=GENERATED_DIR), name="generated")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

class GenerateBannerRequest(BaseModel):
    title: str
    subtitle: str
    tag: str

class BrainstormRequest(BaseModel):
    topic: str
    tone: Optional[str] = "authority"
    gemini_key: Optional[str] = None

class SaveTokenRequest(BaseModel):
    li_at: str

class PublishRequest(BaseModel):
    text: str
    image_filenames: Optional[List[str]] = []

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "authenticated": is_authenticated(),
        "engine": "Agentic DailyCode 2.5",
        "author": "Aditya Dhing"
    }

@app.get("/api/ideas")
def fetch_ideas():
    return get_ideas()

@app.get("/api/repo-images")
def fetch_repo_images():
    """
    Returns real diagrams, assets and screenshots indexed directly from your local repositories!
    """
    images = []
    if os.path.exists(REPO_ASSETS_DIR):
        for f in os.listdir(REPO_ASSETS_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                images.append({
                    "name": f.replace('_', ' ').replace('-', ' ').title(),
                    "filename": f,
                    "url": f"/static/repo_assets/{f}",
                    "source": "Local Repos (AI Agents, Portfolio, System UseCases)"
                })
    return images

@app.post("/api/brainstorm")
def brainstorm(req: BrainstormRequest):
    data = generate_ai_post(req.topic, req.tone, req.gemini_key)
    return data

@app.post("/api/generate-banner")
def create_banner(req: GenerateBannerRequest):
    filename = f"banner_{abs(hash(req.title)) % 1000000}.png"
    out_path = os.path.join(GENERATED_DIR, filename)
    generate_banner(req.title, req.subtitle, req.tag, out_path)
    return {
        "status": "success",
        "image_url": f"/generated/{filename}",
        "filename": filename
    }

@app.post("/api/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    uploaded_urls = []
    filenames = []
    for f in files:
        safe_name = f"upload_{abs(hash(f.filename)) % 100000}_{f.filename.replace(' ', '_')}"
        dest = os.path.join(UPLOADS_DIR, safe_name)
        with open(dest, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
        uploaded_urls.append(f"/uploads/{safe_name}")
        filenames.append(safe_name)
    return {
        "status": "success",
        "urls": uploaded_urls,
        "filenames": filenames
    }

@app.post("/api/auth/save-token")
def auth_save_token(req: SaveTokenRequest):
    try:
        val = req.li_at.strip()
        if not val or len(val) < 10:
            raise HTTPException(status_code=400, detail="Token cannot be empty")
        
        # Scenario 1: User pasted JSON format
        if val.startswith("[") and val.endswith("]"):
            cookies = json.loads(val)
            with open(os.path.join(os.path.dirname(__file__), "linkedin_user_data", "session_cookies.json"), "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)
            return {"status": "success", "message": f"Saved {len(cookies)} cookies from JSON!"}

        # Scenario 2: User pasted two tokens separated by comma, space, newline, or semicolon
        parts = [p.strip() for p in val.replace(",", "\n").replace(";", "\n").splitlines() if p.strip()]
        
        li_at_val = ""
        jsession_val = ""

        for p in parts:
            if "li_at" in p.lower():
                li_at_val = p.split("=")[-1].strip().strip('"').strip("'")
            elif "ajax:" in p or "jsession" in p.lower():
                jsession_val = p.split("=")[-1].strip().strip('"').strip("'")
            elif len(p) > 50 and not li_at_val:
                li_at_val = p.strip('"').strip("'")
            elif ("ajax:" in p or len(p) < 60) and not jsession_val:
                jsession_val = p.strip('"').strip("'")

        if len(parts) >= 2 and not li_at_val:
            li_at_val = parts[0]
            jsession_val = parts[1]

        cookies = [
            {
                "name": "li_at",
                "value": li_at_val or val,
                "domain": ".linkedin.com",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "None"
            }
        ]

        if jsession_val:
            jsession_formatted = f'"{jsession_val.strip("\"")}"'
            cookies.append({
                "name": "JSESSIONID",
                "value": jsession_formatted,
                "domain": ".linkedin.com",
                "path": "/",
                "httpOnly": False,
                "secure": True,
                "sameSite": "None"
            })

        out_path = os.path.join(os.path.dirname(__file__), "linkedin_user_data", "session_cookies.json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2)

        return {
            "status": "success", 
            "message": f"Successfully linked {'li_at + JSESSIONID' if jsession_val else 'li_at'}!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/launch-login")
async def auth_interactive():
    try:
        res = await launch_interactive_login()
        return res
    except Exception as e:
        return {"status": "error", "message": f"Browser launch error: {str(e)}"}

@app.post("/api/publish")
async def publish_post(req: PublishRequest):
    paths = []
    for fn in (req.image_filenames or []):
        gen_path = os.path.join(GENERATED_DIR, fn)
        up_path = os.path.join(UPLOADS_DIR, fn)
        repo_path = os.path.join(REPO_ASSETS_DIR, fn)
        if os.path.exists(gen_path):
            paths.append(gen_path)
        elif os.path.exists(up_path):
            paths.append(up_path)
        elif os.path.exists(repo_path):
            paths.append(repo_path)

    res = await publish_to_linkedin(req.text, paths)
    return res

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
