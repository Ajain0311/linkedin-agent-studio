import os
import json
import re
from google import genai
from google.genai import types

SWE_PROFILE_CONTEXT = """
Candidate: Aditya Dhing
Role: Full Stack Software Engineer (.NET Core, React.js, FastAPI, Playwright, AI Applications)
"""

def clean_input(text: str) -> str:
    # Remove common Hinglish phrasing
    t = text.lower()
    for phrase in [
        "ke bare me", "ke baare me", "ki post", "post krte h", "post karte h", "use hui h", 
        "use hua h", "banaya h", "banayi h", "bhai", "samja", "dala to", "chahiye"
    ]:
        t = t.replace(phrase, "")
    return t.strip()

def generate_ai_post(topic: str, tone: str = "authority", api_key: str = None) -> dict:
    key = api_key or os.environ.get("GEMINI_API_KEY")

    if key:
        try:
            client = genai.Client(api_key=key)
            prompt = f"""
            You are an elite Tech LinkedIn Ghostwriter.
            The user provided this raw topic or rough idea: "{topic}".
            
            RULES:
            1. Output must be 100% FLUENT, GRAMMATICALLY PERFECT ENGLISH.
            2. ZERO Hindi/Hinglish words in the headline, hooks, or content.
            3. Understand what the user wants to talk about:
               - If topic mentions 'Linkedin Agent Studio', write about building an Autonomous LinkedIn AI Content Engine with FastAPI, Playwright, and PIL.
               - If topic mentions 'Three.js' / 'Redis', write about 3D WebGL in-memory data visualizer.
            4. Return strictly valid JSON:
            {{
                "headline": "Catchy English Headline",
                "tag": "Tech Tag",
                "hooks": ["Hook 1", "Hook 2", "Hook 3"],
                "content": "Full LinkedIn post text in proper English with emojis and hashtags",
                "banner_title": "Max 5 words",
                "banner_subtitle": "Max 10 words"
            }}
            """
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[WARN] Gemini API error: {e}")

    lower_topic = topic.lower()

    # Rule 1: LinkedIn Agent Studio / Automation
    if "agent studio" in lower_topic or "linkedin" in lower_topic:
        return {
            "headline": "Building an Autonomous LinkedIn Agent Studio with FastAPI & Playwright",
            "tag": "Agentic AI · Automation",
            "hooks": [
                "I automated my entire LinkedIn tech posting workflow using FastAPI, Playwright, and Gemini AI.",
                "Why manual content scheduling is obsolete for software engineers in 2026.",
                "Inside the architecture of my self-hosted LinkedIn AI Agent Studio."
            ],
            "content": """🤖 Tired of manual content creation and scheduling? I built an Autonomous LinkedIn Agent Studio to automate the entire technical publishing lifecycle.

Here is the exact architectural breakdown:

1️⃣ The Brain (Content & Hook Engine):
Integrated with Gemini to transform rough engineering ideas and commit logs into high-signal technical posts with customizable tones and viral hooks.

2️⃣ Dynamic Banner & Diagram Pipeline:
Generates 16:9 cinematic dark-tech cards via PIL and automatically indexes architectural diagrams straight from my local GitHub repositories.

3️⃣ Session Encrypted Playwright Publisher:
Instead of fragile API limits, a persistent headless Playwright runner authenticates using encrypted session cookies, uploads multi-image carousels, and publishes directly with zero manual friction.

Key takeaway: When you build developer tools, always solve your own distribution and visibility bottlenecks first.

What are your thoughts on agentic workflows for software developers? Let me know below! 👇

#SoftwareEngineering #AIAgents #FastAPI #Playwright #Python #Automation #SystemDesign #OpenSource""",
            "banner_title": "LinkedIn Agent Studio",
            "banner_subtitle": "Autonomous AI content engine & Playwright publisher"
        }

    # Rule 2: Three.js + Redis
    if "three" in lower_topic or "redis" in lower_topic:
        return {
            "headline": "Visualizing In-Memory Systems: Bringing 3D WebGL to Redis Cache Inspection",
            "tag": "Three.js · Redis",
            "hooks": [
                "Terminal CLIs are fast, but what if you could visually inspect distributed cache clusters in 3D?",
                "Why I integrated Three.js into RedisCache-UI instead of building another flat dashboard.",
                "How interactive WebGL graphs transformed the way I debug distributed cache keys."
            ],
            "content": """⚡ Who said backend caching tools have to live entirely in an ASCII terminal?

When managing thousands of cached keys in Redis across microservice namespaces, flat tables and CLI grep commands quickly become overwhelming. 

That is why I integrated Three.js into RedisCache-UI — turning abstract in-memory key-value data into an interactive visual graph.

Here is what this architectural shift unlocked:

1️⃣ Spatial Namespace Clustering:
Namespaces are rendered as 3D node clusters. High-cardinality prefixes and cache hotspots become immediately obvious at a glance.

2️⃣ Real-Time TTL Heatmaps:
Nodes visually transition colors based on remaining TTL countdowns — cold, expiring, and persistent keys are identifiable in real-time.

3️⃣ Low-Overhead WebGL Rendering:
By offloading rendering to the client's GPU via Three.js canvas instancing, the interface handles 10,000+ key nodes smoothly with 60 FPS performance without lagging the browser.

Sometimes the best developer productivity comes from making invisible backend infrastructure tangible and visual.

Check out the project on GitHub: github.com/Ajain0311/RedisCache-UI

Fellow engineers, what's your take on bringing 3D/WebGL visualizations to developer tools? Innovation or overkill? 👇

#SoftwareEngineering #ThreeJS #Redis #WebGL #Frontend #DeveloperTools #OpenSource #FullStack""",
            "banner_title": "RedisCache-UI in 3D",
            "banner_subtitle": "Visualizing in-memory cache clusters with Three.js & WebGL"
        }

    # Generic intelligent fallback in clean English
    cleaned = clean_input(topic).title() or "Modern Software Architecture"
    return {
        "headline": f"Engineering Breakdown: {cleaned}",
        "tag": "Architecture",
        "hooks": [
            f"Most engineers overlook data flow efficiency when implementing {cleaned}.",
            f"Here is how we optimized {cleaned} for low latency and high availability.",
            f"3 architectural lessons learned while shipping {cleaned} in production."
        ],
        "content": f"""🚀 Engineering Breakdown: {cleaned}

Building high-throughput production systems requires decoupling concerns and optimizing data flow efficiency from day one.

Here is the 3-step architectural framework I rely on:

1️⃣ Decoupled Data Layer:
Ensure strict abstraction boundaries isolate business logic from database and third-party storage interactions.

2️⃣ In-Memory Caching & Localized Invalidation:
Shave off database round trips by serving hot data from localized cache layers with TTL-bound expiry.

3️⃣ Observability First:
Metrics over guesswork. Instrument endpoints with distributed tracing and structured logging before optimizing code.

What has been your experience implementing {cleaned} in production? Let's discuss in the comments 👇

#SoftwareEngineering #SystemArchitecture #Backend #Cloud #FullStack #OpenSource""",
        "banner_title": cleaned[:28],
        "banner_subtitle": "Architectural principles & performance optimization"
    }
