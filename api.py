import tweepy


Consumer_Key = ""
Consumer_Secret = "" 

Access_Token = ""
Access_Token_Secret = ""  

auth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)

auth.set_access_token(Access_Token, Access_Token_Secret)
auth.secure = True

api = tweepy.API(auth)