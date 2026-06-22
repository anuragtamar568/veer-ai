import customtkinter as ctk
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import threading

# --- 1. CONFIGURATION ---
genai.configure(api_key="YOUR_API_KEY_HERE") # Yahan apni API key daalein
model = genai.GenerativeModel("gemini-1.5-flash")
my_creator = "Aapka Naam"

# Speech engine setup
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_ai_response(prompt):
    full_prompt = f"Tum {my_creator} dwara banaye gaye ho. Tum ek personal assistant ho. {prompt}"
    response = model.generate_content(full_prompt)
    return response.text

# --- 2. GUI INTERFACE (Theme aur Design) ---
class AssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("My Personal AI Assistant")
        ctk.set_appearance_mode("dark") # Dark theme
        
        self.label = ctk.CTkLabel(self, text="Assistant ready...", font=("Arial", 20))
        self.label.pack(pady=20)

        self.btn = ctk.CTkButton(self, text="Sunn Raha Hoon...", command=self.start_voice_mode)
        self.btn.pack(pady=20)

    def start_voice_mode(self):
        threading.Thread(target=self.process_voice).start()

    def process_voice(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.configure(text="Boliye...")
            audio = r.listen(source)
            try:
                user_text = r.recognize_google(audio)
                self.label.configure(text=f"Aapne kaha: {user_text}")
                
                ai_reply = get_ai_response(user_text)
                speak(ai_reply)
                self.label.configure(text=ai_reply)
            except:
                self.label.configure(text="Maafi chahta hoon, samajh nahi paya.")

if __name__ == "__main__":
    app = AssistantApp()
    app.mainloop()
