import os
import json
import random
from typing import List, Dict

POST_IDEAS = [
    {
        "id": "idea-1",
        "category": "AI Agents & Autonomous SWE",
        "tag": "AI Engineering",
        "title": "How I Built an Autonomous AI Software Engineer with FastAPI & Gemini",
        "subtitle": "Self-driving agent pipeline that plans, tests, and pushes commits daily.",
        "content": """🤖 Can AI write, verify, and push production-ready code while you sleep?

Over the past few weeks, I’ve been building the DailyCode Engine — an autonomous AI agent pipeline designed to test the limits of self-driving software development.

Here is the exact architecture breakdown:

1️⃣ The Brain (Gemini 2.5 + FastAPI):
Instead of simple prompt-response loops, the system follows a structured pipeline: System Specs → Schema Generator → API Engine → Unit Test suite.

2️⃣ Deterministic JSON Storage Engine:
Before touching any external database, an in-memory & file-based JSON DB validates incoming schemas with strict zero-trust rules.

3️⃣ Autonomous GitHub Actions Pipeline:
Every scheduled cycle, the agent validates tests, triggers Git commits, and logs telemetry without manual intervention.

Key Takeaway: The future of software engineering isn't writing code from scratch — it's architecting self-healing agents that build and verify reliably.

What are your thoughts on agentic workflows in software engineering? Would you trust an agent with your CI/CD? 👇

#SoftwareEngineering #AIAgents #FastAPI #GeminiAI #Python #Automation #SystemDesign #OpenSource"""
    },
    {
        "id": "idea-2",
        "category": "Enterprise & High Concurrency",
        "tag": ".NET Architecture",
        "title": "Optimizing .NET Core APIs for High-Concurrency Citizen Services",
        "subtitle": "Resolving bottlenecks, in-memory caching strategies, and storage abstractions.",
        "content": """⚡ What happens when your .NET Core API gets hit with government-scale traffic?

Working on large-scale citizen platforms taught me 3 critical lessons about performance optimization that tutorials rarely mention:

1️⃣ The Silent Killer: Database Thread Starvation
When concurrency spikes, slow DB round-trips quickly exhaust thread pools. Moving from direct queries to an in-memory cache layer cut latency by over 60%.

2️⃣ Provider-Agnostic Storage Abstraction:
Hardcoding S3 or Azure Blob SDKs into controllers is a technical debt trap. Creating a custom storage abstraction layer enabled zero-refactor migrations between local MinIO and Azure Blob Storage.

3️⃣ Visibility Beats Guesswork:
You can’t fix what you can’t observe. Integrating structured logging with Serilog & Grafana Loki pinpointed 90% of our slow endpoints in minutes.

Architecture tip: Always profile under load before refactoring.

Fellow .NET devs, what’s your #1 performance optimization rule in production? 💬

#DotNet #CSharp #Performance #SystemDesign #BackendArchitecture #Azure #APIs #SoftwareEngineering"""
    },
    {
        "id": "idea-3",
        "category": "Mobile & System Architecture",
        "tag": "React Native",
        "title": "Building a Multi-Module Consumer Super App with React Native & Expo",
        "subtitle": "Combining food delivery, rides & marketplace in one modular application.",
        "content": """📱 Consolidating 3 separate products into ONE super app without turning the codebase into spaghetti code:

Recently engineered a consumer platform combining Food Delivery, Ride Booking, and Local Marketplace into a unified mobile client.

Here is how we kept the architecture modular and maintainable:

🔹 Modular Federation in React Native + Expo:
Each vertical (food, ride, shop) operates as an isolated feature package with its own state slice, preventing cross-module side effects.

🔹 Real-time Geolocation & Push Sync:
Leveraging background location tracking and deep linking to ensure ride and order tracking updates seamlessly even when minimized.

🔹 Clean ASP.NET Core Backend Contracts:
Unified JWT authentication with role-based access control (RBAC) powering all modules through a consistent API gateway.

The biggest challenge? Balancing app bundle size and battery performance while keeping location tracking real-time.

Are you building with React Native in 2026? How do you manage massive cross-platform apps? 👇

#ReactNative #Expo #MobileDevelopment #DotNetCore #SuperApp #SystemArchitecture #TechJourney"""
    },
    {
        "id": "idea-4",
        "category": "Developer Tools",
        "tag": "Open Source",
        "title": "Why I Built RedisCache-UI: Browser-Based Redis Key Management",
        "subtitle": "No CLI required — real-time inspection, TTL management, and bulk operations.",
        "content": """🛠️ Developer tools shouldn't make simple tasks frustrating.

Native Redis CLI is lightning fast, but when you need to inspect TTLs, search regex patterns across 10,000 keys, or safely delete cache namespaces in staging, the CLI can get tedious.

So I built **RedisCache-UI** — a lightweight, standalone browser tool for developers:
✅ Real-time key visualization with TTL expiry countdowns.
✅ Regex search and selective namespace bulk-deletion.
✅ Zero-install, pure client-side interface for fast debugging.

Open source on GitHub: github.com/Ajain0311/RedisCache-UI

Always build tools that solve your own friction points first. 🚀

What's your favorite developer productivity tool? Let me know below!

#OpenSource #Redis #DeveloperTools #WebDevelopment #Frontend #JavaScript #Productivity"""
    }
]

def get_ideas():
    return POST_IDEAS

def get_idea_by_id(idea_id: str):
    for i in POST_IDEAS:
        if i["id"] == idea_id:
            return i
    return POST_IDEAS[0]
