import speech_recognition as sr

recognizer = sr.Recognizer()

for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {mic_name}")

device_index = int(input("Enter the correct device index: "))

with sr.Microphone(device_index=device_index) as source:
    print("🎙️ Speak now...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_sphinx(audio)
        print("✅ Transcribed Text:", text)
    except sr.UnknownValueError:
        print("❌ Could not understand the audio")
    except sr.RequestError:
        print("🚨 Speech recognition service unavailable")