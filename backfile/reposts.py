import sys 
import re 
import datetime 
from pymongo import MongoClient 
from bson.objectid import ObjectId 
  
  
  
try: 
    client = MongoClient('mdb-001.ecs.soton.ac.uk') 
except: 
    print "error"
  
db = client['weibo_2012'] 
  
  
def encodeText(text): 
    text = text.encode('utf-8').strip() 
    return text 
  
def findUsers(db): 
    times_to_tweet = {}

    collection = db['tweets']
    print 'There are ' + str(collection.count())+ ' tweets in the database'      
    runcount = 0
    tweetcount = 0
    repostcount = 0
    count = 0
  
    #for tweet in collection.find({"text" : {'$regex': "反腐"}}):
    #items = collection.find({"reposts_count" : {'$in': [tweetcount]}})
    #print 'There are ' + str(items.count()) + ' tweets that have been reposted ' + str(tweetcount) + ' times.'
    #tweetcount+=1
    result = collection.find().sort({'reposts_count': -1}).limit(1)
    #result = collection.distinct("reposts_count")
    #repostcount = result['reposts_count']
    #print repostcount
    print result


    for x in xrange (0, result+1):
        items = collection.find({"reposts_count" : {'$in': [tweetcount]}})
        print 'There are ' + str(items.count()) + ' tweets that have been reposted ' + str(tweetcount) + ' times.'
        if times_to_tweet.has_key(str(tweetcount)):
            times_to_tweet[str(tweetcount)] = times_to_tweet[str(tweetcount)]+1
        else:
            times_to_tweet[str(tweetcount)] = 1
        tweetcount+=1
    
    #while tweetcount > 0:
     #   items = collection.find({"reposts_count" : {'$in': [tweetcount]}})
      #  print 'There are ' + str(items.count()) + ' tweets that have been reposted ' + str(tweetcount) + ' times.'
       # repostcount = items.count
        #tweetcount+=1
        
    #for tweet in collection.find({"reposts_count" : {'$in': [1]}}):
     #   count+=1
      #  print str(tweet['created_at'].encode('utf-8').strip())
       # print "','"
        #print str(tweet['text'].encode('utf-8').strip())
        #print str(tweet['user:{"screen_name"}'].encode('utf-8').strip())
        #print count
        #try: 
         #   timestamp = str(tweet['created_at'].encode('utf-8').strip())
          #  tweetUser = tweet['name'].encode('utf-8').strip() 
           # tweetText = str(tweet['text'].encode('utf-8').strip()) 

        #except: 
         #   pass              
        return times_to_tweet

def parser_to_json(d):
    l = [{"name":k,"size":v} for k,v in d]
    return json.dumps(dict("children":l))
    
  
if __name__ == '__main__': 
    #run the script 
    findUsers(db) 
