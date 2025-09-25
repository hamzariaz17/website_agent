from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

app = FastAPI()

# Allow CORS (frontend ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production me apna domain dalna (e.g., ["https://hamza.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API setup
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Please set it in environment")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Route for chatbot
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # ✅ Hamza ke business context add kiya
    company_info = """
    You are an AI Customer Support Agent for Tech Solutions services company.
    The company provides the following services:
    - Website Development (React.js, Next.js, MongoDB, Node.js)
    - Mobile App Development (Flutter)
    - SEO Services (Search Engine Optimization)
    - Digital Marketing Services
    - UI/UX Design
    - AI Chatbot & AI Agent Development
    - E-commerce Development
    - Cloud Deployment & DevOps

    Rules:
    - Only answer questions related to these services.
    - Be professional, polite, and helpful.
    - If customer asks something unrelated, politely say:
      "I specialize in Website Development, Flutter Apps, SEO, and Digital Marketing. 
      Would you like to know more about these services?"
    """

    # AI ko prompt
    prompt = f"""
    {company_info}
    Customer: {user_message}
    """

    response = model.generate_content(prompt)
    return {"reply": response.text}
