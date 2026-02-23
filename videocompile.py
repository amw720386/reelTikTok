from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.audio.fx import AudioFadeIn, AudioFadeOut, MultiplyVolume
import random
import os

video_path = "./data/cache/video.mp4"
voice_path = "./data/cache/output.mp3"
title_path = "./data/title.txt"
sentiment_path = "./data/title_sentiment.txt"
music_dir = "./data/background/audio"
output_path = "./data/output/final.mp4"

with open(sentiment_path, "r") as f:
    compound = float(f.read().strip())

if compound < -0.3:
    music_file = "sad.mp3"
else:
    music_file = f"{random.randint(1,4)}.mp3"
music_path = os.path.join(music_dir, music_file)

video_clip = VideoFileClip(video_path)
voice_audio = AudioFileClip(voice_path)
bg_music = AudioFileClip(music_path).with_duration(voice_audio.duration)

num_loops = int(voice_audio.duration // bg_music.duration) + 1  
bg_music = bg_music * num_loops 

bg_music = bg_music.subclipped(0, voice_audio.duration)  

fade_duration = min(3, voice_audio.duration / 6)
bg_music = AudioFadeIn(fade_duration).apply(bg_music)
bg_music = AudioFadeOut(fade_duration).apply(bg_music)

if music_file == "sad.mp3":
    bg_music = MultiplyVolume(0.1).apply(bg_music)  
else:
    bg_music = MultiplyVolume(0.2).apply(bg_music)  

combined_audio = CompositeAudioClip([bg_music, voice_audio])
final_video = video_clip.with_audio(combined_audio)
final_video.write_videofile(
    output_path,
    codec="libx264",
    audio_codec="aac",
    audio_bitrate="128k",
    bitrate="8000k",
    fps=60,
    preset="slow"
)

final_video.close()
voice_audio.close()
bg_music.close()
video_clip.close()


