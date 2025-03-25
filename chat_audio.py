from io import BytesIO
from playsound import playsound
from client_openai import OpenAIClient

import datetime
import speech_recognition as sr

openaiClient = OpenAIClient()

client = openaiClient.get_client()


recognizer = sr.Recognizer()

audio_path = 'files/audio/chat'
audio_name = 'audio.mp3'


def record_audio():
    with sr.Microphone() as source:
        print('Ouvindo ...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    return audio


def transcribe_audio(audio):
    wave_data = ""
    wave_data = BytesIO(audio.get_wav_data())
    wave_data.name = 'audio.wav'
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=wave_data,
        language="pt",
    )
    return transcription.text


def chat(message):
    response = client.chat.completions.create(
        messages=message,
        model="gpt-3.5-turbo-0125",
        max_tokens=1000,
        temperature=0,
    )
    return response


def create_audio(text):
    audio_file = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
    )
    date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_name = f"assistant_{date}.mp3"
    audio_file.write_to_file(f"{audio_path}/{audio_name}")
    return audio_name


def play_audio(audio_file):
    playsound(f"{audio_path}/{audio_file}")


if __name__ == '__main__':

    messages = []
    while True:
        audio = record_audio()
        transcription = transcribe_audio(audio)

        messages.append({"role": "user", "content": transcription})
        print(f"User: {messages[-1]['content']}")
        response = chat(messages)
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content})
        print(f"Assistant: {messages[-1]['content']}")
        audio_file = create_audio(messages[-1]['content'])
        play_audio(audio_file)
