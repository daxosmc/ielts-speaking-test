import speech_recognition as sr

recognizer = sr.Recognizer()

def transcribe_audio():
    try:
        with sr.Microphone(device_index=1) as source:  # Adjust the index if needed
            print("🎙️ Speak now...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)  # Using Google STT

            return {"transcription": text}
    except sr.UnknownValueError:
        return {"error": "Could not understand audio"}
    except sr.RequestError:
        return {"error": "Speech recognition service unavailable"}