from config import C_KEY, C_SECRET, A_TOKEN, A_TOKEN_SECRET, USE_VIRTUAL_DISPLAY
from pyvirtualdisplay import Display
from selenium import webdriver
import tweepy
from wand.image import Image
import os
import re

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

class FakeSenatePic:

    senate_pic_original = 'images/senate_pic_original.jpg'
    senate_pic_canvas = 'images/senate_pic_canvas.png'

    def __init__(self, tweet_url):
        self.tweet_url = tweet_url
        self.tweet_id = tweet_url.split('/')[-1].split('?')[0]
        self.outfile = 'output/%s/final.png' % self.tweet_id
        self.tweet_obj = api.get_status(self.tweet_id)

    def make_fake_pic(self):

        try:
            os.mkdir('output')
        except FileExistsError:
            pass

        try:
            os.mkdir('output/%s' %self.tweet_id)
        except FileExistsError:
            pass

        self._screenshot_tweet()
        self._crop_tweet()
        self._compose_image()


    def _screenshot_tweet(self):
        outfile = 'output/%s/screenshot.png' %self.tweet_id
        if not os.path.isfile('output/%s/screenshot.png' %self.tweet_id):
            print("    fakepic: screenshotting tweet")

            if USE_VIRTUAL_DISPLAY:
                display = Display(visible=0, size=(1920, 600))
                display.start()

            driver = webdriver.Firefox()
            driver.get(self.tweet_url)
            driver.save_screenshot(outfile)
            driver.quit()

    def _crop_tweet(self):
        outfile = 'output/%s/tweet_cropped.png' %self.tweet_id

        tweet_height = self._get_tweet_height()

        if not os.path.isfile(outfile):
            print("    fakepic: cropping image of tweet")
            with Image(filename='output/%s/screenshot.png' %self.tweet_id) as img:
                # TODO: smart cropping
                # make sure it works for tweets of various lengths, replies, photos
                img.crop(350, 70, width=580, height=tweet_height)
                img.save(filename=outfile)

    def _get_tweet_height(self):
        # approximating how the tweet should be cropped based on contents
        tweet_text_len = len(self.tweet_obj.text)

        # logic for height here
        if tweet_text_len < 50:
            height = 250
        elif tweet_text_len < 100:
            height = 275
        else:
            height = 300

        # give more space if there are links (assuming rich snippets)
        if self.tweet_obj.entities.get('urls', None):
            height += 140

        return height

    def _compose_image(self):

        # making canvas
        if not os.path.isfile(FakeSenatePic.senate_pic_canvas):
            self._make_canvas()

        if not os.path.isfile(self.outfile):
            print("    fakepic: adding tweet to poster")
            with Image(filename=FakeSenatePic.senate_pic_canvas) as senate_floor_img:
                with Image(filename='output/%s/tweet_cropped.png' %self.tweet_id) as tweet_img:
                    cropped_height = tweet_img.height
                    print(cropped_height)
                    tweet_img.resize(int(tweet_img.width*.55),int(tweet_img.height*.55))
                    tweet_img.rotate(2)
                    if cropped_height > 300: # position diff if there is media & tweet is tall
                        senate_floor_img.composite(tweet_img, left=660, top=120)
                    else:
                        senate_floor_img.composite(tweet_img, left=660, top=150)
                    senate_floor_img.save(filename=self.outfile)

    def _make_canvas(self):
        with Image(filename=FakeSenatePic.senate_pic_original) as senate_floor_img:
            with Image(filename='images/white.png') as white:
                white.rotate(2)
                white.resize(340, 260)
                senate_floor_img.composite(white, left=655, top=110)
                senate_floor_img.save(filename=FakeSenatePic.senate_pic_canvas)

    def cleanup(self):
        # cleanup images
        os.remove('output/%s/screenshot.png' % self.tweet_id)
        os.remove('output/%s/tweet_cropped.png' % self.tweet_id)
        os.remove('output/%s/final.png' % self.tweet_id)
        os.rmdir('output/%s' % self.tweet_id)


if __name__ == '__main__':

    a_good_tweet = 'https://twitter.com/realdonaldtrump/status/239088515122614272?lang=en'

    fake_pic = FakeSenatePic(a_good_tweet)
    fake_pic.make_fake_pic()
