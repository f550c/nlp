from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb #pip install MySQL-python 
import time
import json



#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("localhost","root","ch","dbname")
conn.set_character_set('utf8')
c = conn.cursor()
c.execute('SET NAMES utf8;')
c.execute('SET CHARACTER SET utf8;')
c.execute('SET character_set_connection=utf8;')


#consumer key, consumer secret, access token, access secret.
ckey="dkTYu157yhvg1Ic03Xfefg8qV"
csecret="JogB2CWmGOhZgGoC46VJUCLtsp08oCvaDPIH0jx6r7hQ8UuNgw"
atoken="3260043218-Koiw35ap8lY4NqJuZBcRZBCiK8ziR5ZIf6MvOs4"
asecret="ya3N3WtvQ6gvXbVHJKdbqNJnGSPZXopVA0pbicQH1gAdQ"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"]
        
        c.execute("INSERT INTO taula (time, username, tweet) VALUES (%s,%s,%s)",
            (time.time(), username, tweet))

        conn.commit()

        print((username,tweet))
        
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])
