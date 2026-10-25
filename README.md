# 🚀 LinkedIn Agent Studio (v2.5 Cinematic)
*Autonomous Tech LinkedIn Content Engine & Auto-Publisher*

A sleek, cyberpunk-inspired web studio designed for Software Engineers to brainstorm high-signal tech posts with AI, render 16:9 dark-tech architecture banners, index local repository diagrams, and auto-publish directly to LinkedIn.

---

## ✨ Features

- **🧠 Live Gemini AI Brainstormer**: Converts raw project thoughts or commit ideas into 100% professional English technical posts with dynamic viral hooks.
- **🎨 Dark-Tech Banner Engine**: PIL-powered 1200x675 (16:9) cinematic banner generator with custom glowing tags and author branding.
- **📁 Repo Diagram & Asset Vault**: 1-click access to architecture diagrams, workflows, and screenshots from local repositories.
- **⚡ 1-Click Native Publisher**: Direct pre-filled LinkedIn post integration with auto-copy and image clipboard injection.
- **🤖 Headless Playwright Engine**: Session-authenticated publisher for automated posting.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, FastAPI, Uvicorn, Pydantic
- **AI & Automation**: Google Gemini 2.5 Flash, Playwright Chromium
- **Graphics**: Pillow (PIL), Canvas
- **Frontend**: Tailwind CSS, Vanilla JS, FontAwesome, JetBrains Mono

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Ajain0311/linkedin-agent-studio.git
cd linkedin-agent-studio

# Install dependencies
pip install -r requirements.txt

# Run the studio locally
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open `http://127.0.0.1:8000` in your browser.

---

## ☁️ Deployment (Render / Railway / HuggingFace)

- **Build Command**: `pip install -r requirements.txt && playwright install chromium`
- **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
