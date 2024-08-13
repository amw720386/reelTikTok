import moviepy.editor as mpe
from os import listdir, remove, path

my_clip = mpe.VideoFileClip("./data/cache/video.avi")
audio_background = mpe.AudioFileClip("./data/cache/output.mp3")
final_clip = my_clip.set_audio(audio_background)
final_clip.write_videofile("./data/output/final.mp4", fps=60)


def deleteFiles(directory, extension=""):
    for f in listdir(directory):
        if f.endswith(extension):
            remove(path.join(directory, f))


# Delete temp files
deleteFiles("./data/audio", ".mp3")
deleteFiles("./data/screenshots", ".png")
deleteFiles("./data/cache", ".avi")
deleteFiles("./data/cache", ".mp3")
deleteFiles("./data", ".txt")
