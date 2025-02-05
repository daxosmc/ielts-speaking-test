from transformers import pipeline

# Load a free open-source AI model (Hugging Face GPT-Neo)
ai_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

def ai_examiner(transcription: str):
    try:
        response = ai_pipeline(transcription, max_length=100, num_return_sequences=1, truncation=True)
        return {"examiner_response": response[0]["generated_text"]}
    except Exception as e:
        return {"error": str(e)}