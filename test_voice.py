import speech_recognition as sr


recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.energy_threshold = 100
recognizer.pause_threshold = 1
recognizer.phrase_threshold = 0.3


mic_index = 1


with sr.Microphone(device_index=mic_index) as source:

    print("Calibrating...")
    
    recognizer.adjust_for_ambient_noise(
        source,
        duration=2
    )


    print("🎤 Speak a full sentence...")


    audio = recognizer.listen(
        source,
        timeout=20,
        phrase_time_limit=15
    )


print("Processing...")


# Save captured audio for debugging
with open(
    "test_audio.wav",
    "wb"
) as f:
    f.write(
        audio.get_wav_data()
    )


try:

    text = recognizer.recognize_google(
        audio,
        language="en-IN"
    )


    print("\n✅ Result:")
    print(text)



except sr.UnknownValueError:

    print(
        "❌ Speech detected but Google could not understand"
    )


except sr.RequestError as e:

    print(
        "❌ Google API Error:",
        e
    )