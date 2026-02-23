import praw as pw
import random
import os
import undetected_chromedriver as uc
from dotenv import load_dotenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import azure.cognitiveservices.speech as speechsdk
from moviepy import AudioFileClip, concatenate_audioclips

nltk.download('vader_lexicon')
load_dotenv()

AZURE_KEY = os.getenv("azure_speech_key")
AZURE_REGION = os.getenv("azure_region")

AZURE_VOICES = [
    "en-US-JennyNeural",
    "en-US-GuyNeural",
    "en-GB-SoniaNeural",
    "en-AU-NatashaNeural"
]

def createSpeechAudio(id, text, voice_name="en-US-JennyNeural"):
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
    speech_config.speech_synthesis_voice_name = voice_name
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    file_path = f"{audioDirectory}/{id}.mp3"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure TTS failed: {result.reason}")
    return file_path

reddit = pw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    user_agent=os.getenv("user_agent"),
)

audioDirectory = "./data/audio"
screenshotDir = "./data/screenshots"
cacheDir = "./data/cache"
maxComments = 20
min_duration = 60
screenshotFileNames = []
voiceoverFileNames = []

chrome_options = uc.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

post_file = open("posts.txt", "r")

def selectPost():
    posts = list(reddit.subreddit("askreddit").top(time_filter="day", limit=50))
    for post in random.sample(posts, len(posts)):
        if not post.url in post_file.read():
            if not post.over_18:
                return post
    return None

selectedPost = selectPost()
if selectedPost is None:
    print("No suitable post found.")
    exit()

title = selectedPost.title.replace('[Serious]', '').strip()

with open("./data/title.txt", "w", encoding="utf-8") as f:
    f.write(title)

sia = SentimentIntensityAnalyzer()
compound = sia.polarity_scores(title)['compound']
with open("./data/title_sentiment.txt", "w") as f:
    f.write(str(compound))

driver.get(selectedPost.url)

post_file.close()

post_file = open("posts.txt", "a")
post_file.write(f"\n{selectedPost.url}")

sleep(4)

driver.execute_script("""
    const nav = document.querySelector('[is-hamburger-menu-included]');
    if (nav) nav.style.display = 'none';
""")

postContent = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "shreddit-post"))
)

postScreenshot = f"{screenshotDir}/post.png"
with open(postScreenshot, "wb") as f:
    f.write(postContent.screenshot_as_png)
screenshotFileNames.append(postScreenshot)

driver.set_window_size(375, 2000)

sleep(2)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(2)  
driver.execute_script("window.scrollTo(0, 0);")

titleAudio = createSpeechAudio(f"originalpost-{selectedPost.id}", title, voice_name="en-US-JennyNeural")
voiceoverFileNames.append(titleAudio)

total_duration = AudioFileClip(titleAudio).duration
comments_with_audio = []

for comment in selectedPost.comments:
    if len(comments_with_audio) >= maxComments:
        break
    if len(comment.body.split()) > 100:
        continue

    random_voice = random.choice(AZURE_VOICES)
    audio_path = createSpeechAudio(f"comment-{comment.id}", comment.body, voice_name=random_voice)
    duration = AudioFileClip(audio_path).duration
    total_duration += duration
    comments_with_audio.append((comment, audio_path, duration))

    if total_duration >= min_duration:
        break

driver.execute_script("""
  document.querySelectorAll("shreddit-comment[slot='replies']").forEach(el => el.style.display = 'none');
""")

for comment, audio_path, _ in comments_with_audio:
    try:
        commentElement = driver.find_element(
            By.XPATH, f"//shreddit-comment[@thingid='t1_{comment.id}' and not(@slot)]"
        )

        commentSCName = f"{screenshotDir}/comment-{comment.id}.png"
        with open(commentSCName, "wb") as f:
            f.write(commentElement.screenshot_as_png)

        screenshotFileNames.append(commentSCName)
        voiceoverFileNames.append(audio_path)

    except Exception as e:
        print(f"[!] Failed to screenshot comment {comment.id}: {e}")

time_stamp = 0
with open("./data/timestamps.txt", 'w') as f:
    for img, audio in zip(screenshotFileNames, voiceoverFileNames):
        f.write(f"{img} | {audio} | {time_stamp}\n")
        time_stamp += AudioFileClip(audio).duration
    f.write(f"NULL | NULL | {time_stamp}")

clips = [AudioFileClip(path) for path in voiceoverFileNames]
final_clip = concatenate_audioclips(clips)
outputFile = f"{cacheDir}/output.mp3"
final_clip.write_audiofile(outputFile)

exit()
