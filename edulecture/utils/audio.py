from elevenlabs import generate, clone, save, Voice
from elevenlabs import set_api_key
from pydub import AudioSegment
import os
from math import ceil

# Takes in file path to specific audio file and returns its duration in seconds
def get_audio_length(audio_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    duration_sec = ceil(len(audio) / 1000.0)
    return duration_sec

# Takes in array of paths to audio files and returns array of durations
def get_audio_durations(audio_files):
    durations = []
    for audio_file in audio_files:
        durations.append(get_audio_length(audio_file))
    return durations

def generate_clone(sample_voice, api_key, name):
    set_api_key(api_key)
    voice=clone(name=name, files=[sample_voice])
    return voice.voice_id

# Takes in sample voice file array and text file
def generate_audio(voice_id, text, image_folder_path):
    entiretext = open(text).read()
    texts = entiretext.split("*****")
    texts.pop()

    ctr = 1
    audio_file_paths = []

    for text in texts:
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        filename = "audio" + str(ctr) + ".wav"
        audio_file_path = os.path.join(image_folder_path, filename)
        save(audio, audio_file_path)
        ctr += 1
        audio_file_paths.append(audio_file_path)
    return audio_file_paths

def generate_master_sound(audio_files, save_path):
    master_sound = AudioSegment.from_file(save_path + "/temp-files/audio1.wav")
    for n in range(2,len(audio_files)+1):
        master_sound = master_sound + AudioSegment.from_file(save_path + "/temp-files/audio" + str(n) + ".wav")
    master_sound.export(save_path + "/master_sound.wav", format="wav")