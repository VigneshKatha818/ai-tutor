import os
from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paste your actual gsk_ key inside the quotes as a safe local backup
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY", "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"))

@app.post("/stream")
async def stream_tutor(topic: str = Form(...)):
    async def generate_explanation():
        response = await client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a friendly AI Tutor. Explain the user's topic like they are 5 years old using clear, simple analogies."},
                {"role": "user", "content": f"Explain this topic: {topic}"}
            ],
            stream=True
        )
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    return StreamingResponse(generate_explanation(), media_type="text/plain")
