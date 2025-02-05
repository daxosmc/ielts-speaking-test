from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf(transcription, ai_feedback, scores):
    pdf_filename = "ielts_report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "IELTS Speaking Test Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, "Transcription:")
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(100, height - 120, transcription[:90] + "...")

    # ✅ Fix AI Feedback
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 160, "AI Feedback:")

    # Extract text from dictionary
    ai_feedback_text = ai_feedback.get("examiner_response", "No feedback available")
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(100, height - 180, ai_feedback_text[:90] + "...")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 220, "IELTS Scores:")
    c.drawString(100, height - 240, f"Fluency: {scores['fluency']}")
    c.drawString(100, height - 260, f"Vocabulary: {scores['vocabulary']}")
    c.drawString(100, height - 280, f"Grammar: {scores['grammar']}")
    c.drawString(100, height - 300, f"Pronunciation: {scores['pronunciation']}")
    c.drawString(100, height - 320, f"Final Score: {scores['final_score']}")

    c.save()
    return pdf_filename