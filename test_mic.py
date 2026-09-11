import speech_recognition as sr


mic_index = 1

recognizer = sr.Recognizer()


with sr.Microphone(device_index=mic_index) as source:

    print("Adjusting noise...")
    recognizer.adjust_for_ambient_noise(
        source,
        duration=3
    )

    print("Speak loudly now...")
    
    audio = recognizer.listen(
        source,
        timeout=10,
        phrase_time_limit=5
    )


print("Audio captured")

print("Energy threshold:")
print(recognizer.energy_threshold)


with open("voice_test.wav","wb") as f:
    f.write(audio.get_wav_data())


print("Saved voice_test.wav")