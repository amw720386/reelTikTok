
# ReelTikTok

With the click of a button create your very own reddit-based piece of short form content!

In-built webscraping from the [AskReddit](https://www.reddit.com/r/AskReddit/) subreddit formatted and automatically voiced over to create the wonderful classic form of content we've come to know and love!

https://github.com/user-attachments/assets/70051dab-ac37-4bb3-8156-70f1ad6b0894

## Dependencies
 
- [OpenCV C++](https://github.com/opencv/opencv)
- [MoviePy](https://github.com/Zulko/moviepy)
- [Selenium](https://github.com/SeleniumHQ/selenium)
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)


## Usage

1. Run the main.py file which handles the scraping seperately. 

```
C:\Users> python main.py
```

2. Run the ReelTikTok.cpp file which handles the video overlay editing process and produces several different clips.

```
C:\Users> g++ ReelTikTok.cpp
```

3. Run the vidaudiocombine.py file which stitches the clips together and saves the final product.

```
C:\Users> python vidaudiocombine.py
```

The final product should be saved in this directory
```
../data/output
```
## Authors

- [Ahamed Mohamed Wajibu](https://github.com/amw720386/)
- [Aryan Shah](https://github.com/ghostarmor)
