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
        # Example: li_at=AQED... jsessionid="ajax:..." OR AQED... , "ajax:..."
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

        # If only 2 plain tokens were given line by line
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
            # Ensure proper quote wrapping if missing for JSESSIONID
            jsession_formatted = f'"{jsession_val.strip('"')}"'
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
