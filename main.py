import praw as pw
import random
import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, VideoFileClip, concatenate_audioclips
from os import listdir, remove, path
import chromedriver_autoinstaller


reddit = pw.Reddit(
    client_id="lcBdUVrZ1HEkcNxA7TaW_A",
    client_secret="OD8L4FiaQdqhnu-l0sbxg_CJcpQnxQ",
    user_agent="testscript by InfinityDev",
)

audioDirectory = "./data/audio"
screenshotDir = "./data/screenshots"
maxComments = 3
screenshotFileNames = []
voiceoverFileNames = []

chromedriver_autoinstaller.install()
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(
    executable_path="chromedriver.exe", options=chrome_options)


def selectPost():
    posts = list(reddit.subreddit("askreddit").top(
        time_filter="day", limit=50))
    randNum = random.randint(1, len(posts))
    count = 1
    for post in posts:
        if count == randNum:
            if post.over_18:
                return selectPost()
            return post
        count += 1


def createSpeechAudio(id, text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 172)
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[0].id)
    filePath = audioDirectory + "/" + id + ".mp3"
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath


selectedPost = selectPost()
if selectedPost == None:
    print("Uh oh")
    exit()


def getComments():
    comments = []
    for comment in selectedPost.comments:
        if len(comments) >= maxComments:
            break
        if len(comment.body.split()) <= 100:
            comments.append(comment)
    return comments


def takeScreenshots():
    driver.get(selectedPost.url)
    sleep(4)

    postContent = driver.find_element(By.TAG_NAME, 'shreddit-post')

    screenshotName = screenshotDir + "/post.png"
    screenshotFileNames.append(screenshotName)
    file = open(screenshotName, "wb")
    file.write(postContent.screenshot_as_png)
    file.close()
    # Get comment screenshots
    for comment in getComments():
        commentElement = None
        commentElement = driver.find_element(
            By.XPATH, f"//shreddit-comment[@thingid='t1_{comment.id}']")

        # Get whole comment and screenshot
        commentSCName = f'{screenshotDir}/comment-{comment.id}.png'
        screenshotFileNames.append(commentSCName)
        cFile = open(commentSCName, "wb")
        cFile.write(commentElement.screenshot_as_png)
        cFile.close()

    return screenshotName


takeScreenshots()


# Create audio files
title = selectedPost.title
if title.startswith('[Serious]') or title.endswith('[Serious]'):
    title = title.replace('[Serious]', '')
voiceoverFileNames.append(createSpeechAudio(
    "originalpost-" + selectedPost.id, selectedPost.title))
for comment in getComments():
    voiceoverFileNames.append(createSpeechAudio(
        "comment-" + comment.id, comment.body))

# Write timestamps to txt file (for C++ file to access)
time_stamp = 0
timestamps_file = open("./data/timestamps.txt", 'w')
for i in range(len(screenshotFileNames)):
    timestamps_file.write(
        screenshotFileNames[i] + " | " + voiceoverFileNames[i] + " | " + str(time_stamp) + '\n')
    time_stamp += AudioFileClip(voiceoverFileNames[i]).duration
timestamps_file.write('NULL | NULL | ' + str(time_stamp))
timestamps_file.close()


def createClip(audioFile):
    audioClip = AudioFileClip(audioFile)
    return audioClip


clips = []
for i in range(len(screenshotFileNames)):
    clip = createClip(voiceoverFileNames[i])
    clips.append(clip)

final_clip = concatenate_audioclips(clips)

outputFile = "./data/cache/output.mp3"
final_clip.write_audiofile(
    outputFile
)

exit()
