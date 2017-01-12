import tweepy
from config import C_KEY, C_SECRET, A_TOKEN, A_TOKEN_SECRET
from fakepic import FakeSenatePic

def handle_tweets():

    # look at your last tweet
    print("\n\nLOOKING AT PAST REALSENATEFLOOR TWEETS")
    public_tweets = api.home_timeline()
    last_pic_tweet_user = None
    last_pic_tweet_id = None
    for tweet in public_tweets:
        print("tweet: %s" % tweet.text)
        # if this tweet is a reply & has image
        if tweet.in_reply_to_screen_name and tweet.in_reply_to_status_id_str and tweet.entities.get("media", None):
            print("**break**")
            last_pic_tweet_user = tweet.in_reply_to_screen_name
            last_pic_tweet_id = tweet.in_reply_to_status_id_str
            break

    # search tweets
    print("\n\nLOOKING AT MENTIONS")
    mentions = api.mentions_timeline() # QUESTION: is there a way to filter tweets here?
    for mention in mentions: # these are in reverse chronological order
        print("mention: %s" % mention.text)
        poster_tweet_sn = mention.in_reply_to_screen_name
        poster_tweet_id = mention.in_reply_to_status_id_str
        has_trigger_phrase = 'bern this' in mention.text

        # if this tweet is a reply and has trigger phrase
        if poster_tweet_sn and poster_tweet_id and has_trigger_phrase:
            print("  relevant mention!")
            poster_tweet_url = 'https://twitter.com/%s/status/%s' %(poster_tweet_sn, poster_tweet_id)

            # check if you have already responded to this tweet w/ pic
            # if so, break out of loop
            # QUESTION: is there a potential bug w/ not responding to tweets if img processing somehow fails?
            trigger_tweet_sn = mention.user.screen_name
            trigger_tweet_id = mention.id_str
            if trigger_tweet_id == last_pic_tweet_id:
                print("**break (already responded to this tweet)**")
                break

            fake_pic_maker = FakeSenatePic(poster_tweet_url)
            fake_pic_maker.make_fake_pic()

            # upload image to twitter as a response
            # TODO: change status text
            status = '@%s here ya go' % trigger_tweet_sn
            print("    tweeting!")
            api.update_with_media(fake_pic_maker.outfile, status=status, in_reply_to_status_id=trigger_tweet_id)
            # deleting pics after
            fake_pic_maker.cleanup()



if __name__ == '__main__':

    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)
    # api.update_status('hello world')

    handle_tweets()
