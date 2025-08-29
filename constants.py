"""App constants"""

AI: dict[str, dict[str, str]] = {
    "PERPLEXITY": {
        "MODEL": "sonar",
        "SONAR": "sonar",
        "SONAR_PRO": "sonar-pro",
        "SONAR_REASONING_PRO": "sonar-reasoning-pro",
        "BASE_URL": "https://api.perplexity.ai",
    },
    "OPEN_AI": {
        "MODEL": "gpt-4o-mini",
        "BASE_URL": "",
    },
    "CLAUDE": {
        "MODEL": "claude-3-7-sonnet-latest",
        "BASE_URL": "",
    },
    "GEMINI": {
        "MODEL": "gemini-2.5-flash",
        "GEMINI_FLASH-LITE": "gemini-2.5-flash-lite",
        "GEMINI_FLASH": "gemini-2.5-flash",
        "GEMINI_PRO": "gemini-2.5-pro",
        "GEMINI_PREVIEW": "gemini-live-2.5-flash-preview",
        "GEMINI_IMAGE_PREVIEW": "gemini-2.5-flash-image-preview",
        "BASE_URL": "https://generativelanguage.googleapis.com/v1beta/openai/",
    },
    "DEEPSEEK": {
        "MODEL": "gemini-2.0-flash",
        "BASE_URL": "https://api.deepseek.com/v1",
    },
    "GROQ": {
        "MODEL": "gemini-2.0-flash",
        "BASE_URL": "https://api.groq.com/openai/v1",
    },
}
