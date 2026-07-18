import os
from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/stream")
async def stream_tutor(topic: str = Form(...)):
    async def generate_explanation():
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly AI Tutor. Explain the user's topic like they are 5 years old using clear, simple analogies."},
                {"role": "user", "content": f"Explain this topic: {topic}"}
            ],
            stream=True
        )
        async for chunk in response:
            content = chunk.choices.delta.content
            if content:
                yield content

    return StreamingResponse(generate_explanation(), media_type="text/plain")
