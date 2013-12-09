#!/usr/bin/python2.7

def read_data(txt):
    
    with open(txt) as f:
        line = f.readline()
        while line: #skip the head
            if line.strip().isdigit():
                tweetid = line.strip()
                user = f.readline().strip()
                gender = f.readline().strip()
                text = f.readline().strip()
                tweetcount = int(f.readline().strip())
                time = f.readline().strip()
                tweet = {"tweetid":tweetid,"user":user,"gender":gender,"text":text,"time":time}
                for i in range(3): # skip the space lines
                    line = f.readline()
            else: line = f.readline()

if __name__ == "__main__":
    read_data("smallDataset.txt")
