import os
import shutil
import moviepy.editor as mp 
import cv2
from .audio import get_audio_durations, generate_audio, generate_clone, generate_master_sound
import utils.text as gt

# Video conversion function
def video_conversion(video_file: str, video_save_path: str, audio_file: str):
    try:
        video = mp.VideoFileClip(video_file)
        audio = mp.AudioFileClip(audio_file)
        output = video.set_audio(audio)
        output.write_videofile(video_save_path, codec="libx264")


        print("Conversion completed successfully.")
        return video_save_path
    except FileNotFoundError:
        raise FileNotFoundError("Input file does not exist.")
    except OSError as e:
        raise OSError(f"Error occurred during conversion: {e}")
    
# Video Generating function 
def generate_video(presentation_id, voice_id, user_path, video_title, user_voice_file, user_name): 
    image_folder_path = user_path + "/temp-files"
    image_folder = gt.generate_images(presentation_id, image_folder_path)
    video_name = video_title + ".avi"
    video_path = user_path + "/" + video_name
    video = cv2.VideoWriter(video_path, 0, 1, (1600, 900))
      
    images = [img for img in os.listdir(image_folder) if img.endswith("png")] 
    images.sort()
    # API_KEY = "f5ef28538059549f46f9832bf9309ab6"
    # API_KEY = "32e2a6e83130d6f0e6718bf99df3e474"
    API_KEY = "f6d5b3935e642e4f1c548ae7d4be465f"

    # should be inputting path to file / name of file, right now is actual raw file itself
    voice_id = generate_clone(user_voice_file, API_KEY, user_name)
    # print("New voice ID: " + voice_id)

    audio_file_paths = generate_audio(voice_id, gt.generate_text(presentation_id, image_folder_path), image_folder_path)
    durations = get_audio_durations(audio_file_paths)

    for image, duration in zip(images, durations):
        current_image = cv2.imread(os.path.join(image_folder, image))
        for _ in range(duration):
            video.write(current_image)  
      
    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 

    generate_master_sound(audio_file_paths, user_path)
    video_save_path = user_path + "/" + video_title + ".mp4"
    video_name = video_conversion(video_path, video_save_path, user_path + "/master_sound.wav")
    os.remove(user_path + "/master_sound.wav")
    os.remove(video_path)
    return video_name
