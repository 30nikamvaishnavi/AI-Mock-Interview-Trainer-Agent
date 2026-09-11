import speech_recognition as sr


def speech_to_text():

    recognizer = sr.Recognizer()


    with sr.Microphone(
        device_index=1
    ) as source:

        print("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )


        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=30
        )


    try:

        print("Processing...")

        text = recognizer.recognize_google(
            audio
        )

        return text


    except sr.UnknownValueError:

        return "Could not understand audio"


    except sr.RequestError:

        return "Speech service unavailable"


    except Exception as e:

        return str(e)