'''
Created on Feb 7, 2014

@author: KJ
'''
import json
import sys

import tweepy

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

from scikits.learn.features.text import WordNGramAnalyzer

#import sys
# following four keys are provided by twitter
consumer_key="WxlLPjHHynHASubxXPtuHQ"
consumer_secret="ZsyLG0t1H4WWtwewdp12fbIJyZre6aE306JP9sY"

access_token="19610295-TtV1mgxk09JYW4GQFFBY2nzvDGaWAtRwa3yfTdmds"
access_token_secret="gQYrVkmvXKo821HZmwIFBhuISKIIgMB3m3r96QdQfIY"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    
        
    def on_data(self, data):
        parsed_json =json.loads(data)
        new_tagged_sent = []
        try:
            if 'text' in parsed_json: 
                # following lines are needed in order to run the code in terminal
                # commented because the eclipse has option to run its terminal in utf-8  
                if type(parsed_json['text']) == unicode:
                    tweet_text = parsed_json['text'].encode(sys.stdout.encoding, 'replace')
                else:      
                    tweet_text = parsed_json['text']
                
                new_tagged_sent = WordNGramAnalyzer(min_n=1, max_n=2).analyze(tweet_text)
                print tweet_text
                print new_tagged_sent
                
                add_to_graph(new_tagged_sent)
                #print 'Accuracy: %4.1f%%' % (100.0 * unigram_tagger.evaluate(tagged_sent))
        except   UnicodeEncodeError:
            print "error in ", parsed_json 
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    
    #track=['costa'] is the topic of twitter data stream
    stream.filter(track=['python'])
    #stream.sample()