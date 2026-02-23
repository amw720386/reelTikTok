# ReelReddit

**Transform engaging Reddit stories into captivating short-form video content automatically.**

ReelTikTok scrapes trending threads from Reddit, generates AI-powered voiceovers, overlays dynamic visuals, and uploads finished videos directly to YouTube Shorts—all with minimal manual intervention.

https://github.com/user-attachments/assets/6ef34482-03f8-4db2-95bf-bddcc45a0159

## Features

- **Automated Web Scraping** - Extracts top posts and comments from r/AskReddit
- **AI Text-to-Speech** - Converts Reddit text to natural-sounding audio using Azure Cognitive Services
- **Dynamic Video Processing** - Overlays images on background videos with intelligent scaling and centering
- **Video Compilation** - Combines processed clips with audio tracks and background music
- **YouTube Integration** - Automatically uploads finished videos to YouTube Shorts with metadata
- **Configuration Management** - Environment-based setup for API credentials and file paths

## Project Structure

```
reelTikTok-prod/
├── main.py                # Entry point - orchestrates the pipeline
├── scrape.py              # Reddit web scraping and audio generation
├── videoprocess.py        # Image overlay and video frame processing
├── videocompile.py        # Video and audio composition
├── ytupload.py            # YouTube Shorts upload automation
├── .env                   # Environment configuration (credentials, API keys)
├── data/
│   ├── background/        # Background video files
│   ├── cache/             # Temporary processing files
│   ├── output/            # Final compiled videos
│   └── timestamps.txt     # Frame timing synchronization
└── README.md
```

## Dependencies

- **Python 3.8+**
- [opencv-python](https://github.com/opencv/opencv) - Video frame processing
- [moviepy](https://github.com/Zulko/moviepy) - Audio-video composition
- [selenium](https://github.com/SeleniumHQ/selenium) - Browser automation for YouTube upload
- [praw](https://github.com/praw-dev/praw) - Reddit API client
- [azure-cognitiveservices-speech](https://github.com/Azure-Samples/cognitive-services-speech-sdk) - Text-to-speech
- [google-auth-oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib) - YouTube API authentication

## Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/yourusername/reelTikTok-prod.git
cd reelTikTok-prod
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with your API credentials:

```properties
# Reddit API (from https://www.reddit.com/prefs/apps)
client_id="your_reddit_client_id"
client_secret="your_reddit_client_secret"
user_agent="reelTikTok by YourUsername"

# Azure Text-to-Speech (from https://portal.azure.com)
azure_speech_key="your_azure_speech_key"
azure_region="eastus"

# Google YouTube API
client_secret_file="client_secret_xxx.json"
token_file="token.pickle"
```

### 3. Set Up YouTube Credentials

1. Enable the YouTube Data API v3 in [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials (Desktop app)
3. Download JSON and save as `client_secret_xxx.json` in the project root
4. The first run will prompt you to authorize the app

### 4. Add Background Videos

Place your background video file in the `data/background/` directory:

```bash
mkdir -p data/background
mkdir -p data/cache
mkdir -p data/output
```

**Recommended specs for background videos:**
- **Format:** MP4 (H.264 codec)
- **Resolution:** 1080x1920 (vertical for Shorts)
- **Duration:** 30-60 seconds
- **File size:** Under 100MB

Example: `data/background/2.mp4`

## Usage

Run the complete pipeline:

```bash
python main.py
```

This will:
1. **Scrape** trending Reddit threads
2. **Generate** AI voiceovers for text content
3. **Process** videos with image overlays
4. **Compile** final video with audio
5. **Upload** to YouTube Shorts automatically

Finished videos are saved to `./data/output/`

## Configuration

Adjust behavior by editing environment variables or modifying these files:

- `scrape.py` - Reddit subreddit selection, post filtering
- `videoprocess.py` - Video resolution, image scaling logic
- `videocompile.py` - Audio mixing, background music settings
- `ytupload.py` - Title formatting, tags, visibility settings

## Troubleshooting

- **Video upload fails** - Verify YouTube API credentials and ensure account has upload permissions
- **Audio generation fails** - Check Azure Cognitive Services API key and regional availability
- **Missing frames** - Verify background video exists at `./data/background/2.mp4`

## License

[MIT License](https://mit-license.org/)

---

**Questions or suggestions?** Open an issue.
