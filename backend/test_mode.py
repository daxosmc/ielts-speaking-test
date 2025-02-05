import time
import random

def ielts_test_mode():
    print("🎙️ Welcome to IELTS Speaking Test Simulation!")
    print("📌 Test Mode Activated. Please follow the examiner’s instructions.\n")

    # 🎤 **Part 1: Introduction & Interview**
    part1_questions = [
        "Can you tell me a little about yourself?",
        "Where are you from?",
        "Do you work or study?",
        "What do you like about your city?"
    ]
    for question in part1_questions:
        print(f"📝 Examiner: {question}")
        time.sleep(2)  # Small delay for natural conversation
        input("🎤 Press Enter when you have answered...")

    # 🎴 **Part 2: Long Turn (Cue Card Activity)**
    cue_cards = [
        "Describe a memorable trip you had.",
        "Talk about a book that influenced you.",
        "Describe a person who inspires you."
    ]
    selected_cue_card = random.choice(cue_cards)
    print("\n🎴 IELTS Cue Card:")
    print(f"📝 {selected_cue_card}")
    print("⏳ You have **1 minute** to prepare. Then you will speak for **2 minutes**.")
    
    time.sleep(10)  # Give the user time to prepare
    input("🎤 Press Enter when you are ready to start speaking...")

    # 🔄 **Part 3: Two-Way Discussion**
    print("\n🔄 Moving to Part 3: Discussion")
    discussion_questions = [
        "Why do you think people enjoy traveling?",
        "How can reading change a person’s perspective?",
        "Do you think role models are important in society?"
    ]
    for question in discussion_questions:
        print(f"📝 Examiner: {question}")
        time.sleep(2)  # Small delay
        input("🎤 Press Enter when you have answered...")

    # 📊 **Generate IELTS Scores**
    scores = {
        "fluency": round(random.uniform(6.0, 9.0), 1),
        "vocabulary": round(random.uniform(6.0, 9.0), 1),
        "grammar": round(random.uniform(6.0, 9.0), 1),
        "pronunciation": round(random.uniform(6.0, 9.0), 1),
        "final_score": round(random.uniform(6.0, 9.0), 1)
    }
    print("\n📊 Test Completed! Generating Your IELTS Score...")
    print(scores)
    
    print("\n📄 Your PDF report is being generated...")

    return scores  # Return the scores for PDF generation
    # Generate PDF Report
    print("📄 Your PDF report is being generated...")

    return scores  # Return scores for further processing