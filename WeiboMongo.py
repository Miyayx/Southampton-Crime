#!/usr/bin/python2.7
#encoding=utf-8
import sys 
import re 
import datetime 
from pymongo import MongoClient 
from bson.objectid import ObjectId 
import json
  
class WeiboMongo:
    def __init__(self):
        
        try: 
            client = MongoClient('mdb-001.ecs.soton.ac.uk') 
            self.db = client['weibo_2012'] 
        except: 
            print "error"
      
    def encodeText(self, text): 
        text = text.encode('utf-8').strip() 
        return text 
      
    def findUsers(self): 
        times_to_tweet = {}
    
        collection = self.db['tweets']
        print 'There are ' + str(collection.count())+ ' tweets in the database'      
        runcount = 0
        tweetcount = 0
        repostcount = 0
        count = 0
      
        for item in collection.find({"text":{"$regex":"反腐"}}):
            if item.has_key('reposts_count'):
                tweetcount = item['reposts_count']
                if times_to_tweet.has_key(tweetcount):
                    times_to_tweet[tweetcount] = times_to_tweet[tweetcount]+1
                else:
                    times_to_tweet[tweetcount] = 1

        return times_to_tweet

    @staticmethod
    def parser_to_json(fre_d, tweet_d,total):
        # sorted using key
        d = sorted(fre_d.items(), key=lambda x: x[0])
        l = [{"repost_count":k,"fre":v} for k,v in d]
        for t in l:
            total = total + len(tweet_d[t["repost_count"]])
            t["tweet"] = tweet_d[t["repost_count"]]
            
        return json.dumps({"children":l,"total":total},encoding="utf-8",ensure_ascii=False)

    @staticmethod
    def get_repostscounts_json_from_file(txt, jsonfile):
        repost_to_frequency = {}
        repost_to_tweets = {}
        total = 0
        
        with open(txt) as f:
            line = f.readline()
            while line:
                if line.strip().isdigit():
                    tweetid = line.strip()
                    user = f.readline().strip()
                    gender = f.readline().strip()
                    text = f.readline().strip()
                    tweetcount = int(f.readline().strip())
                    time = f.readline().strip()
                    tweet = {"tweetid":tweetid,"user":user,"gender":gender,"text":text,"time":time}
                    total = total + 1
                    if repost_to_frequency.has_key(tweetcount):
                        repost_to_frequency[tweetcount] = repost_to_frequency[tweetcount]+1
                        if len(repost_to_tweets[tweetcount]) < 8:
                            repost_to_tweets[tweetcount].append(tweet)
                    else:
                        repost_to_frequency[tweetcount] = 1
                        repost_to_tweets[tweetcount] = []
                        repost_to_tweets[tweetcount].append(tweet)
                    for i in range(3):
                        line = f.readline()
                else: line = f.readline()
            with open(jsonfile,'w') as fw:
                fw.write(WeiboMongo.parser_to_json(repost_to_frequency, repost_to_tweets,total))

    @staticmethod
    def parsing(userID,text):
        result = []
        b = text.split('//@')
        count = -1
        
        for i in b:
            result.append(b[count])
            count -= 1
    
        prev = None
        result2 = []
        for index,pair in enumerate(result):
            if ':' in pair:
                pair = pair.split(':')
                if prev == None:
                    result2.append(pair)
                    prev = pair[0]
                else:
                    pair.insert(1,prev)
                    prev = pair[0]
                    result2.append(pair)
            else:
                pair = [userID,prev,pair]
                result2.append(pair)
        return result2

    @staticmethod
    def get_triple_json_from_file(txt, jsonfile):
        with open(txt) as f:
            line = f.readline()
            while line:
                if line.strip().isdigit():
                    user = f.readline().strip()
                    gender = f.readline().strip()
                    text = f.readline().strip()
                    tweetcount = int(f.readline().strip())
                    time = f.readline().strip()
                    tweet = {"user":user,"gender":gender,"text":text,"time":time}
                    triple = WeiboMongo.parsing(user, text)
                    for t in triple:
                        for i in t:
                            print i
                            print "************"
                    print "============="
                    for i in range(3):
                        line = f.readline()
                else: line = f.readline()
    #        with open(jsonfile,'w') as fw:
    #            fw.write(WeiboMongo.parser_to_json(repost_to_frequency, repost_to_tweets,total))

    @staticmethod
    def parse_triple_tnt_json(triple_list, tweetid_tweet):
        l = []
        j = {}
        #j= []
        for t1,t2,name in triple_list:
            # t1 is a tweet
            # t2 is prev_tweet
            # name is who repost t2 and create t1
            if t2:
                d = {"source":t2,"target":t1,"user":name}
                d["source_tweet"] = tweetid_tweet[t2]
                d["target_tweet"] = tweetid_tweet[t1]
            #else:
            #    d = {"source":"","target":t1,"user":""}
                #d["target_tweet"] = tweetid_tweet[t1]
                
            if j.has_key(t2): 
                j[t2].append(d)
            else:
                j[t2] = []
                j[t2].append(d)
           # j.append(d)

        return json.dumps(j,encoding="utf-8",ensure_ascii=False)

    @staticmethod
    def get_nametext_id(tweetid, name, text, nametext_id_d):
        texts = text.split("//@")
          
        #0是本人发表的评论
        #1是被转发的人的screen_name和评论text
        #以screen_name和text标示一个weibo
        key = name+"@@"+texts[0].strip()
        if not nametext_id_d.has_key(key):
            nametext_id_d[key] = tweetid

    @staticmethod
    def get_triple_tnt(tweetid, name, text, nametext_id_d, tnt_l):
        texts = text.split("//@")
        if len(texts) == 1:
            #Is an original tweet
            tnt_l.append([tweetid,None,name])
            return
        #0是本人发表的评论
        #1是被转发的人的screen_name和评论text
        #以screen_name和text标示一个weibo
        if ":" in texts[1]:
            try:
                [prev_name,prev_text] = texts[1].split(":",1)
            except:
                #no comment
                prev_name = texts[1].split(":")[0]
                prev_text = ""
        else:
            try:
                [prev_name,prev_text] = texts[1].split("：",1)
            except:
                #no comment
                prev_name = texts[1].split("：")[0]
                prev_text = ""

        key = prev_name+"@@"+prev_text.strip()
        if not nametext_id_d.has_key(key):
            print "Don't have the key",key
            print len(nametext_id_d)
            return
        prev_tweetid = nametext_id_d[key] 
        tnt_l.append([tweetid,prev_tweetid,name])

    @staticmethod
    def get_triple_tnt_from_file(txt, jsonfile):
        nametext_id_d = {}
        tweetid_tweet = {}
        tnt_l = []
        # get {name\ntext:tweetid} dict
        with open(txt) as f:
            line = f.readline()
            while line:
                if line.strip().isdigit():
                    tweetid = line.strip()
                    user = f.readline().strip()
                    gender = f.readline().strip()
                    text = f.readline().strip()
                    tweetcount = int(f.readline().strip())
                    time = f.readline().strip()
                    tweet = {"tweetid":tweetid,"user":user,"gender":gender,"text":text,"time":time}
                    tweetid_tweet[tweetid] = tweet
                    WeiboMongo.get_nametext_id(tweetid,user,text,nametext_id_d)
                    for i in range(3):
                        line = f.readline()
                else: line = f.readline()

        #get tweetid_name_tweetid list
        with open(txt) as f:
            line = f.readline()
            while line:
                if line.strip().isdigit():
                    tweetid = line.strip()
                    user = f.readline().strip()
                    gender = f.readline().strip()
                    text = f.readline().strip()
                    tweetcount = int(f.readline().strip())
                    time = f.readline().strip()
                    WeiboMongo.get_triple_tnt(tweetid,user,text,nametext_id_d,tnt_l)
                    for i in range(3):
                        line = f.readline()
                else: line = f.readline()

        json_data = WeiboMongo.parse_triple_tnt_json(tnt_l,tweetid_tweet)
        with open(jsonfile,'w') as fw:
            fw.write(json_data)
          
if __name__ == '__main__': 
    #run  the script 
    #w =  WeiboMongo()
    #w.fi ndUsers()
    WeiboMongo.get_repostscounts_json_from_file('smallDataset.txt','data/reposts.json')
    #WeiboMongo.get_triple_tnt_from_file('smallDataset.txt','triple_tnt_list.json')
    WeiboMongo.get_triple_tnt_from_file('smallDataset.txt','data/triple_tnt_dict.json')
          
          
