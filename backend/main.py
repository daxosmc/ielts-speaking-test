from fastapi import FastAPI, Response
import speech_recognition as sr
import random
import os
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

# Mount the frontend directory
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

import random

# ✅ Function to generate real-time ratings
def rate_response(response):
    return {
        "fluency": round(random.uniform(6.0, 9.0), 1),
        "vocabulary": round(random.uniform(6.0, 9.0), 1),
        "grammar": round(random.uniform(6.0, 9.0), 1),
        "pronunciation": round(random.uniform(6.0, 9.0), 1)
    }

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

# ✅ Define User Input Model
class UserInput(BaseModel):
    user_name: str

# Store user responses and scores globally
user_data = {"current_user": None}

# ✅ Start Session
@app.post("/start/")
def start_session(data: UserInput):
    user_name = data.user_name.strip()
    user_data["current_user"] = user_name  
    user_data[user_name] = {"responses": {}, "scores": {}, "questions": []}

    return JSONResponse(content={
        "message": f"🎙️ Welcome {user_name}! Choose a mode: Practice or Test.",
        "instructions": "Use /practice_mode or /test_mode to continue."
    })

# ✅ Add Transcription API
@app.get("/transcribe/")
def transcribe():
    user_name = user_data["current_user"]
    if not user_name:
        return JSONResponse(content={"error": "Please start a session first using /start/."}, status_code=400)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 Transcription: {text}")
        return JSONResponse(content={"transcription": text})
    except sr.UnknownValueError:
        return JSONResponse(content={"transcription": "Could not understand audio."})
    except sr.RequestError:
        return JSONResponse(content={"transcription": "Speech recognition service unavailable."})

# ✅ Function to Generate the PDF Report
def generate_pdf(user_name, scores):
    """Generates a PDF report and ensures it's properly saved."""
    directory = "generated_reports"
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
    filename = f"{directory}/{user_name}_IELTS_Report.pdf"

    try:
        print(f"📄 Creating PDF report for: {user_name}")  # Debugging
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, f"IELTS Speaking Test Report - {user_name}")
        c.drawString(100, 730, "-----------------------------------")

        y = 700
        c.drawString(100, y, "Scores:")
        y -= 20
        for category, score in scores.items():
            c.drawString(120, y, f"{category}: {score}")
            y -= 20

        c.save()  # ✅ Ensure the PDF is properly saved!
        print(f"✅ PDF successfully created: {filename}")  # Debugging

        return filename
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return None

# ✅ Practice Mode
@app.post("/practice_mode/")
def practice_mode():
    user_name = user_data["current_user"]
    if not user_name:
        return JSONResponse(content={"error": "Please start a session first using /start/."}, status_code=400)

    questions = ["What is your favorite hobby?", "Describe your best friend.", "What do you enjoy about traveling?"]

    user_data[user_name]["questions"] = questions
    user_data[user_name]["responses"] = {}

    return JSONResponse(content={"questions": questions})

# ✅ Test Mode
@app.post("/test_mode/")
def test_mode():
    user_name = user_data["current_user"]
    if not user_name:
        return JSONResponse(content={"error": "Please start a session first using /start/."}, status_code=400)

    # Part 1: Introduction
    part1_questions = [
        "Can you tell me a little about yourself?",
        "Where are you from?",
        "Do you work or study?",
        "What do you like about your city?"
    ]
    
    # Part 2: Cue Card
    cue_cards = [
        "Describe a memorable trip you had.",
        "Talk about a book that influenced you.",
        "Describe a person who inspires you."
    ]
    selected_cue_card = random.choice(cue_cards)

    # Part 3: Two-Way Discussion
    discussion_questions = [
        "Why do you think people enjoy traveling?",
        "How can reading change a person’s perspective?",
        "Do you think role models are important in society?"
    ]

    # ✅ Store test questions
    user_data[user_name]["questions"] = part1_questions + [selected_cue_card] + discussion_questions
    user_data[user_name]["responses"] = {}

    # ✅ Generate mock scores
    scores = {
        "fluency": round(random.uniform(6.0, 9.0), 1),
        "vocabulary": round(random.uniform(6.0, 9.0), 1),
        "grammar": round(random.uniform(6.0, 9.0), 1),
        "pronunciation": round(random.uniform(6.0, 9.0), 1),
    }
    scores["final_score"] = round(sum(scores.values()) / 4, 1)

    # ✅ Generate PDF report
    pdf_file = generate_pdf(user_name, scores)
    if not pdf_file:
        return JSONResponse(content={"error": "Failed to generate PDF report"}, status_code=500)

    print(f"📄 Your IELTS Report has been generated: {pdf_file}")

    return JSONResponse(content={"message": "Test completed!", "scores": scores, "pdf_report": pdf_file})

# ✅ API Endpoint: Rate User Response
# ✅ API Endpoint: Rate User Response
@app.post("/rate_response/")
def rate_response_api(data: dict):
    response_text = data.get("response", "")
    if not response_text:
        return JSONResponse(content={"error": "Response text is missing"}, status_code=400)
    
    scores = rate_response(response_text)  # Call the function to generate ratings
    return JSONResponse(content=scores)

# ✅ Serve the generated PDF file
@app.get("/download_report/")
def download_pdf():
    user_name = user_data["current_user"]
    if not user_name:
        return JSONResponse(content={"error": "Please start a session first using /start/."}, status_code=400)

    pdf_path = f"generated_reports/{user_name}_IELTS_Report.pdf"

    if os.path.exists(pdf_path):
        print(f"📥 Serving PDF report: {pdf_path}")  # Debugging
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"{user_name}_IELTS_Report.pdf"
        )
    else:
        print("❌ PDF report not found!")  # Debugging
        return JSONResponse(content={"error": "PDF report not found. Run test mode first."}, status_code=404)