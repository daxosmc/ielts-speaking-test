let userName = "";
let currentQuestionIndex = 0;
let mode = "";
let questions = [];

// ✅ Start Session (Ensures backend is ready)
async function startSession() {
    userName = document.getElementById("username").value.trim();
    if (!userName) {
        alert("Please enter your name");
        return;
    }

    document.getElementById("welcome-screen").classList.add("hidden");
    document.getElementById("mode-selection").classList.remove("hidden");

    const response = await fetch("/start/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_name: userName }),
    });

    if (!response.ok) {
        alert("Error starting session. Please check the backend.");
        return;
    }

    console.log("✅ Session started successfully");
}

// ✅ Start Practice Mode (Fixing Unresponsiveness)
async function startPracticeMode() {
    mode = "practice";
    document.getElementById("mode-selection").classList.add("hidden");
    document.getElementById("test-container").classList.remove("hidden");

    const response = await fetch("/practice_mode/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
        alert("Error starting practice mode. Please check the backend.");
        return;
    }

    const data = await response.json();
    
    if (!data.questions || data.questions.length === 0) {
        alert("Error: No practice questions received.");
        return;
    }

    questions = data.questions;
    console.log("✅ Practice questions loaded:", questions);
    askQuestion();
}

// ✅ Start Test Mode (Fixing Unresponsiveness)
async function startTestMode() {
    mode = "test";
    document.getElementById("mode-selection").classList.add("hidden");
    document.getElementById("test-container").classList.remove("hidden");

    const response = await fetch("/test_mode/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
        alert("Error starting test mode. Please check the backend.");
        return;
    }

    const data = await response.json();
    
    if (!data.questions || data.questions.length === 0) {
        alert("Error: No test questions received.");
        return;
    }

    questions = data.questions;
    console.log("✅ Test questions loaded:", questions);
    askQuestion();
}

// ✅ Ask Question (Handles Next Question Properly)
function askQuestion() {
    if (currentQuestionIndex >= questions.length) {
        document.getElementById("question-title").innerText = "Test Completed!";
        document.getElementById("speak-button").classList.add("hidden");
        document.getElementById("next-button").classList.add("hidden");

        if (mode === "test") {
            document.getElementById("download-report").classList.remove("hidden");
        } else {
            document.getElementById("home-button").classList.remove("hidden"); 
        }
        return;
    }

    document.getElementById("question-title").innerText = questions[currentQuestionIndex];
    document.getElementById("transcription").innerText = "";
    document.getElementById("feedback").innerText = "";
}

async function startRecording() {
    document.getElementById("recording-status").innerText = "🎤 Listening...";

    try {
        const response = await fetch("/transcribe/");
        const data = await response.json();

        if (data.error) {
            alert("Transcription Error: " + data.error);
            return;
        }

        document.getElementById("transcription").innerText = data.transcription;
        document.getElementById("recording-status").innerText = "";

        // ✅ Call feedback API if in practice mode
        if (mode === "practice") {
            const feedbackResponse = await fetch("/rate_response/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ response: data.transcription }),
            });

            const feedbackData = await feedbackResponse.json();
            document.getElementById("feedback").innerText = `📊 Feedback: ${JSON.stringify(feedbackData)}`;
        }
    } catch (error) {
        console.error("Error in transcription:", error);
        alert("An error occurred while transcribing.");
    }
}

// ✅ Rate Response API
async function rateResponse(response) {
    const res = await fetch("/rate_response/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ response: response }),
    });

    return await res.json();
}

// ✅ Fix Next Button
function nextQuestion() {
    currentQuestionIndex++;
    askQuestion();
}

// ✅ Fix PDF Download
async function downloadPDF() {
    const response = await fetch("/download_report/");
    
    if (!response.ok) {
        alert("Error: Unable to download the report. Make sure you have completed the test.");
        return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${userName}_IELTS_Report.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    setTimeout(() => {
        window.location.href = "/";
    }, 2000);
}

// ✅ Fix Home Button
function goHome() {
    window.location.reload();
}
