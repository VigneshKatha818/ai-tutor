import os
from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import AsyncGroq
from dotenv import load_dotenv
from google import genai
import os
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your real API key configuration
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY", "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"))

@app.get("/", response_class=HTMLResponse)
async def get_interface():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/stream")
async def stream_tutor(topic: str = Form(...)):
    async def generate_explanation():
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a friendly AI Tutor. Explain the user's topic like they are 5 years old using clear, simple analogies."},
                {"role": "user", "content": f"Explain this topic: {topic}"}
            ],
            stream=True
        )
        async for chunk in response:
            # FIXED: Safely extracting data based on the latest groq library rules
            if hasattr(chunk, 'choices') and chunk.choices:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    yield delta.content

    return StreamingResponse(generate_explanation(), media_type="text/plain")
