"""App constants"""

AI: dict[str, dict[str, str]] = {
    "PERPLEXITY": {
        "MODEL": "sonar",
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
        "MODEL": "gemini-2.0-flash",
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
