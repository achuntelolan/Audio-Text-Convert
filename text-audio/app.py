from flask import Flask, render_template, request
import os
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

UPLOAD_FOLDER = "user_uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Audio could not be recognized"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    converted_text = ""

    if request.method == "POST":
        file = request.files["file"]

        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp.mp3")
            file.save(file_path)

            # Convert MP3 to WAV
            sound = AudioSegment.from_mp3(file_path)
            wav_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp.wav")
            sound.export(wav_path, format="wav")

            # Convert audio to text
            converted_text = convert_audio_to_text(wav_path)

            # Clean up temporary files
            os.remove(file_path)
            os.remove(wav_path)

    return render_template("index.html", converted_text=converted_text)

if __name__ == "__main__":
    app.run(debug=True)
