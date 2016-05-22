import ast
import json
import subprocess

infile_test = "C:/Users/rotom/Desktop/yeahno.txt"
outfile_test = "C:/Users/rotom/Desktop/yeahnotest.txt"

class ParentTweetFetcher():

    """
    Takes a file of tweets in json format
    Returns the parents of those tweets
    alongside them using Twurl in tab-delimited format
    """

    def __init__(self, infile, outfile):

        self.infile = infile
        self.outfile = outfile
        self.tweetdict = {}
        self.parents = []
        self.chunks = []

    def grab_content(self, f):

        with open(f, 'r') as f:

            return f.readlines()

    def populate_tweetdict(self):

        for c in self.grab_content(self.infile):

            if c != '\n': #filter out any parsing detritus

                eval_dict = ast.literal_eval(c)
                parent_id = str(eval_dict['in_reply_to_status_id'])
                tweet_id = str(eval_dict['id'])
                self.parents.append(parent_id)
                tweet = eval_dict['text'].replace('\n', '\\n').encode('utf-8')
                self.tweetdict[parent_id] = [tweet_id, tweet]

    def chunk_ids(self):
        
        """
        A maximum of 100 tweets at a time can be
        requested from twitter
        """
        
        chunk = []
        
        for i in range(len(self.parents)):

            par = self.parents[i]            
            chunk.append(par)
            
            if (i+1)%100 == 0 or i == len(self.parents) - 1:
                self.chunks.append(chunk)
                chunk = []

    def write_output(self):

        """
        This method assumes your consumer key/secret are
        validated for making Twitter requests. See the Twurl
        readme for more information: https://github.com/twitter/twurl
        """

        with open(self.outfile, 'w') as f:

            f.write("parent_id\tparent_tweet\ttweet_id\ttweet\n")
            for chunk in self.chunks:

                id_list=""

                for crumb in chunk:
                    
                    id_list += str(crumb) + ','

                twurl_id_list = "/1.1/statuses/lookup.json?id=" + id_list
                p = subprocess.check_output(["twurl", twurl_id_list], shell=True)
                json_chunk = json.loads(p)

                for tweet in json_chunk:
                    
                    if str(tweet['id']) in self.tweetdict:
                        
                        
                        this_id = str(tweet['id'])
                        this_text = tweet['text'].replace('\n', '\\n').encode('utf-8')
                        
                        self.tweetdict[this_id].append(this_text)
                        line = this_id +'\t'+this_text+'\t'+self.tweetdict[this_id][0]+'\t'+ self.tweetdict[this_id][1]
                        f.write(line+'\n')
                        del self.tweetdict[this_id]         

    def get_tweets_and_parents(self):

        self.populate_tweetdict()
        self.chunk_ids()
        self.write_output()

if __name__ == '__main__':
    ptf = ParentTweetFetcher(infile_test, outfile_test)
    ptf.get_tweets_and_parents()             
 
