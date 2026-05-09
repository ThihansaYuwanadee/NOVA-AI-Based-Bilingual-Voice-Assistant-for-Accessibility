import speech_recognition as sr
import pyttsx3
import pywhatkit
import gtts
import playsound
from google import genai
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
from pathlib import Path
import requests
import json
import pygame
from pywinauto.application import Application
from pywinauto.timings import TimeoutError as PywinautoTimeoutError
import time

API_KEY = "062e667ab318764cf35b5bccf2b24128"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

translator01 = GoogleTranslator(source="auto", target="si")

r = sr.Recognizer() 
input_lang = 'si-LK'
output_lang = 'en'
output_lang01 = 'si'

def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()

def en_translator(i_MyText):
    translator = GoogleTranslator(source="en", target='si')
    translated_text = translator.translate(i_MyText)
    print(translated_text)
    si_sound(translated_text)

def si_translator(i_MyText):
    translator = GoogleTranslator(source="si", target='en')
    translated_text = translator.translate(i_MyText)
    print(translated_text)
    SpeakText(translated_text)

def si_sound(in_awnser):
   try:
        converted_audio = gtts.gTTS(in_awnser, lang=output_lang01)
        # The file is saved locally and played
        converted_audio.save('SA.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('SA.mp3')
        
        # 4. Play the audio
    
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
                time.sleep(0.1)

        
        # 5. Keep the script running until the audio finishes playi
   except Exception as e:
        print(f"An error occurred during TTS or Playback: {e}")
   finally:
        # 6. Clean up: Delete the temporary file
        pygame.mixer.music.stop()
            
        # 6. Unload the file from the mixer
        # This is the most crucial step to release the file lock on Windows.
        pygame.mixer.music.unload()
        
        # 7. Add a small, immediate wait for the OS to release the lock
        time.sleep(0.5) 
        
        # 8. Clean up: Delete the temporary file
        if os.path.exists('SA.mp3'):
            try:
                os.remove('SA.mp3')
                print(f"Successfully cleaned up and deleted '{'SA.mp3'}'.")
            except PermissionError as pe:
                print(f"Warning: Still could not delete the file after unload. Error: {pe}")
        

def gemini(gemini_key_word):
    # NOTE: It is best practice to load API keys from environment variables.
    # Replace "AIzaSyAYKtkTEnUr7CNigsk0e1ACiI-Yp_YysWo" with your actual Gemini API key
    client = genai.Client(api_key="AIzaSyAYKtkTEnUr7CNigsk0e1ACiI-Yp_YysWo")
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents= gemini_key_word+" I NEED SMALL AWNSER"
)
    gemini_output=response.text
    # Remove markdown formatting like asterisks
    gemini_output_create=gemini_output.replace("*", "")
    print(gemini_output_create)
    si_sound(gemini_output_create)

def close_chrome_windows():
    try:
        # Taskkill command forcefully closes the Chrome process
        os.system('taskkill /F /IM chrome.exe')
        print("Successfully sent command to close Chrome on Windows.")
        SpeakText("Successfully sent command to close Chrome on Windows.")
    except Exception as e:
        print(f"Error executing taskkill: {e}")

# Function to close a specific Downloads File Explorer window
def close_specific_downloads_window_windows():
    window_title = "Downloads"
    try:
        # Use pywinauto to connect to the File Explorer application
        app = Application(backend="uia").connect(path="explorer.exe")
        # Search for a window whose title contains "Downloads"
        window = app.window(title_re=f".*{window_title}.*")
        
        if window.exists() and window.is_visible():
            window.close()
            print(f"Successfully closed the window titled: '{window.element_info.name}'")
            SpeakText("Successfully closed the window titled")
        else:
            print(f"No active File Explorer window found titled: '{window_title}'")
            SpeakText("No active File Explorer window found titled")

    except PywinautoTimeoutError:
        print("File Explorer process (explorer.exe) is not running or timed out.")
        SpeakText("File Explorer process (explorer.exe) is not running or timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        SpeakText("have some error")

# Function to close a specific Documents File Explorer window
def close_specific_documents_window_windows():
    window_title = "Documents"
    try:
        app = Application(backend="uia").connect(path="explorer.exe")
        window = app.window(title_re=f".*{window_title}.*")
        
        if window.exists() and window.is_visible():
            window.close()
            print(f"Successfully closed the window titled: '{window.element_info.name}'")
            SpeakText("Successfully closed the window titled")
        else:
            print(f"No active File Explorer window found titled: '{window_title}'")
            SpeakText("No active File Explorer window found titled")

    except PywinautoTimeoutError:
        print("File Explorer process (explorer.exe) is not running or timed out.")
        SpeakText("File Explorer process (explorer.exe) is not running or timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        SpeakText("have some error")
    
def youtube_play(yt_key_word):
    # Opens a YouTube video in the default browser
    SpeakText("Playinh you tube video")
    pywhatkit.playonyt(yt_key_word)
    start(False)
    
     

def google_search(search_keyword):
    # Performs a Google search in the default browser
    pywhatkit.search(search_keyword)
    SpeakText("searching from google")
    print("Searching...")


def get_weather(city_name):
    # Construct the full URL for the OpenWeatherMap API
    complete_url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(complete_url)
        response.raise_for_status() # Raise an exception for bad status codes

        data = response.json()

        if data.get("cod") != "404":
            main_data = data["main"]
            weather_data = data["weather"][0]
            
            temperature = main_data["temp"]
            pressure = main_data["pressure"]
            humidity = main_data["humidity"]
            weather_description = weather_data["description"].capitalize()
            
            print("-" * 30)
            print(f"Weather in {city_name.capitalize()}:")
            SpeakText(f"Weather in {city_name.capitalize()}")
            print(f"Temperature: {temperature}°C")
            SpeakText(f"Temperature {temperature}°C")
            print(f"Condition:  {weather_description}")
            SpeakText(f"Condition   {weather_description}")
            print(f"Humidity    {humidity}%")
            SpeakText(f"Humidity:    {humidity}%")
            print(f"Pressure:    {pressure} hPa")
            SpeakText(f"Pressure    {pressure} hPa")
            print("-" * 30)

        else:
            print(f"Error: City '{city_name}' not found.")
            SpeakText("Error: City '{city_name}' not found.")


    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        SpeakText("have some error")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        SpeakText("have some error")

# Global state variable to control the main loop
is_listening = True 


def ml_identifier(voice):
    global is_listening # Must declare global to modify the variable
    
    # Define system folder paths
    home_dir = Path.home()
    downloads_path = home_dir / "Downloads"
    folder_path_str = str(downloads_path)
    folder_path_str_documents=home_dir / "Documents"
    
    # --- Training Data ---
    x_train = [
        # Class 1: Downloads Folder (Open)
        "Open download folder", "open download", "download",
        "බාගන්න", "open downloads",
        "downloads folder", "show downloads",
        
        # Class 0: Documents Folder (Open)
        "i need to open document folder", "open document", "i like to document folder", "documents", 
        "ලිපිගොනු ෆෝල්ඩරය", "open my documents", "go to documents folder", "document files open",
        "show documents folder", "open my files",
        
        # Class 3: YouTube/Song (Play)
        "ගීතය sindu", "දෙන්න සිංදුව සීදුව සිදුව", "song play youtube", "play you tube", 
        "සිංදුව", "ගීතය", "sindu", "youtube", "සින්දුව", "play song", "play me a song", 
        "open youtube and play", "find a song on youtube", "play something", "search for song",
        
        # Class 2: Weather (Check)
        "What is the weather like",
        "weather check",
        "check weather",
        "current temperature",
        "කාලගුණය",           # Sinhala for 'weather'
        "කාලගුණය කොහොමද",    # Sinhala for 'How is the weather'
        "දැන් කාලගුණය",
        # Class 4: GOOGLE SEARCH
        
        "google search", "search on google", "find information on", "search for this",
        "Google", "ගූගල් සොයන්න", "සොයන්න", "search web for", "look up", "can you search",
        "find this on google", "web search",
        
        # Class 5: GEMINI AI
        "gemini", "jemini", "AI",
        "ජෙමිනිගෙන්", "ජෙමිනි", "ai", "ask AI",
        "give me answer",
        
        # Class 6: WIKIPEDIA SEARCH
       
        
        # Class 7: CHROME CLOSE
        "close chrome", "exit chrome ", 
        "ක්‍රෝම් නවත්වන්න", "close all chrome",
        
        # Class 8: DOWNLOADS FOLDER CLOSE
        "close downloads","close file download", "close downloads folders",
        "බාගත් ෆෝල්ඩර වහන්න", 
        
        # Class 9: EN->SI Translation
        "translate to sinhala", " sinhala", "translate this to sinhala",
        "භාෂා පරිවර්තනය to sinhala", "සිංහලට පරිවර්තනය කරන්න", "sinhala translate",
        
        
        # Class 10: SI->EN Translation
        "translate to english", "english","give me english" 
        "ඉංග්‍රීසි වලට පරිවර්තනය කරන්න", " ඉංග්‍රීසි", 
       
        
        # Class 11: DOCUMENTS FOLDER CLOSE
        "close document","close documents folder", "documents off",
        "ලිපිගොනු ෆෝල්ඩරය වහන්න",  

        # Class 12: STOP LISTENING/EXIT (NEW)
        "stop listening", "exit program","shut down", "stop", "නතර කරන්න", 
        "exit", 
#13
        "hi", "hello", "hey", "how are you", "good morning",
        "good evening", "good afternoon",
      ]

    # --- Training Labels ---
    y_train = [
        1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,3,3,3,
        2, 2,2,2,2,2,2,
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
        5, 5, 5, 5, 5, 5, 5, 5, 
        7, 7, 7, 7,
        8, 8, 8, 8,
        9, 9, 9, 9, 9, 9,
        10, 10, 10, 10,
        11, 11, 11, 11, 
        12, 12, 12, 12, 12, 12, # Class 12: Stop Listening
        13, 13, 13, 13, 13,13,13,
    ] 
    # Initialize and train the ML model (Naive Bayes Classifier)
    vectorize = CountVectorizer(ngram_range=(1, 2))
    x_train_vectorize = vectorize.fit_transform(x_train)
    model = MultinomialNB()
    model.fit(x_train_vectorize, y_train)

    # Predict the class of the user's voice command
    x_test = [voice]
    x_test_vectorize = vectorize.transform(x_test)
    predictions = model.predict(x_test_vectorize)[0] # Get the single prediction value
    
    # --- COMMAND EXECUTION LOGIC ---
    if predictions == 12:
        # This is the STOP/EXIT command
        print('Stop command received. Shutting down assistant...')
        SpeakText("Goodbye! I am stopping now.")
        is_listening = False # Set the global flag to False to break the while loop
        return # Exit the function immediately

    elif predictions == 3:
        print('Playing your YOUTUBE VIDEO....')
        # Check if the command contains a key word for the song, and pass that to the function.
        # Simple extraction might be needed here, or rely on pywhatkit's robustness.
        youtube_play(voice) 

    elif predictions == 2:
        print('weather passed..')
        get_weather('Colombo,LK') 

    elif predictions == 4:
        google_search(voice)

    elif predictions == 5:
        gemini(voice)  

    elif predictions == 7:
        close_chrome_windows()

    elif predictions == 8:
        close_specific_downloads_window_windows()
    
    elif predictions == 9:
        en_translator(voice)

    elif predictions == 10:
        si_translator(voice)

    elif predictions == 11:
        close_specific_documents_window_windows()

    elif predictions==13:
        print("Heloo   This is  Nova  AI  How  May I Assit  You ")
        SpeakText("Heloo   This  is  Nova  AI  How  May I Assit  You ")

    elif predictions == 1: # Open Downloads
        try:
            if os.path.exists(folder_path_str):
                os.startfile(folder_path_str)
                print("\nSuccess! Your Downloads folder should now be open in the file explorer.")
            else:
                print("\nERROR: The Downloads folder was not found at the expected location.")
        except Exception as e:
            print(f"\nAn error occurred while trying to open the folder: {e}")

    elif predictions == 0: # Open Documents
        try:
            if os.path.exists(folder_path_str_documents):
                os.startfile(folder_path_str_documents)
                print("\nSuccess! Your Documents folder should now be open in the file explorer.")
            else:
                print("\nERROR: The Documents folder was not found at the expected location.")
        except Exception as e:
            print(f"\nAn error occurred while trying to open the folder: {e}")
            
    else:
        # Fallback for unrecognized commands
        print("Command not recognized. Trying a general Google search.")
        SpeakText("Command not recognized. Trying a general Google search.")
        google_search(voice)


def start(command):
    global is_listening # Ensure we are using the global variable
    is_listening = command
    
    # Main loop that keeps the assistant running
    while is_listening:     
        try:
            print('Listening...')
            
            with sr.Microphone() as source2:
                # Adjust for noise for better accuracy
                r.adjust_for_ambient_noise(source2, duration=1.0)
                # Before the try block, or outside the loop if r is defined globally
                r.energy_threshold = 4000 # Example value, you'll need to experiment
# Comment out or remove r.adjust_for_ambient_noise
                
                # Listen for user's input, with a time limit
                audio2 = r.listen(source2, phrase_time_limit=10) 
                
                # Recognize the speech using Google
                MyText = r.recognize_google(audio2, language=input_lang)
                MyText = MyText.lower()

                print(f"You said: {MyText}")
                
                # Process the command, which might set is_listening to False
                ml_identifier(MyText)

                
                
        except sr.UnknownValueError:
            # Handle cases where no speech is detected or speech is unclear
            print("No speech detected or could not understand the audio.")
            
        except sr.WaitTimeoutError:
             # Handle listening session ending without user input
             print("Listening timed out, waiting for new command.")
             
        except sr.RequestError as e:
            # Handle API connection errors
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == '__main__':
    # Start the assistant, initializing the state to True
    start(True)
    # This line executes only after the 'while is_listening' loop breaks
    print("Assistant has exited.")