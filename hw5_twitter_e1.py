from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:sec-002
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
# username = sys.argv[1]
# num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
# url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
# requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:

#Code for Part 3:Caching----------------------------------------------------------------
#Finish parts 1 and 2 and then come back to this
#using code from class
# on startup, try to load the cache from file
CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_tweet_id(result_dict_list):
    tweet_id = []
    for aDict in result_dict_list:
        tweet_id.append(aDict['id_str'])
    return tweet_id


def params_unique_combination(username, tweet_id_list):
    return username + "-" + "_".join(tweet_id_list)


def make_request_using_cache(baseurl, params, auth, username):
    resp = requests.get(baseurl, params, auth=auth)
    resp_list = json.loads(resp.text)
    unique_ident = params_unique_combination(username, get_tweet_id(resp_list))

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        pass ## it's a cache miss, fall through to refresh code

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file

    print("Making a request for new data...")
    # Make the request and cache the new data
    CACHE_DICTION[unique_ident] = resp_list
    dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return CACHE_DICTION[unique_ident]


#extract just the 'text' from the data structures returned by twitter api
def get_text_list(tweet_dict_list):
    atweet = []
    for adict in tweet_dict_list:
            atweet.append(adict['text'])
    return atweet

def get_tweet(username, num_tweets, auth):
    base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'screen_name': username, 'count': num_tweets}
    return make_request_using_cache(base_url, params, auth, username)

def tweet_token(alist_with_text):
    tweet_tokenize = []
    for sentence in alist_with_text:
        tweet_tokenize.append(nltk.tokenize.word_tokenize(sentence))
    return tweet_tokenize

def filted_freqDist(tokenizedList):
    stop_words = nltk.corpus.stopwords.words("english") + ["http", "https", "RT" ]
    freq_dist = nltk.FreqDist()
    for tokened_sen in tokenizedList:
        for token in tokened_sen:
            if token not in stop_words and token.isalpha():
                freq_dist[token] += 1
    return freq_dist

def join_tokenized_list(tokenizedList):
    thelist = []
    for alist in tokenizedList:
        thelist.extend(alist)
    return thelist

def find_common_freqDist(tokenizedList1, tokenizedList2):
    list1 = join_tokenized_list(tokenizedList1)
    list2 = join_tokenized_list(tokenizedList2)
    stop_words = nltk.corpus.stopwords.words("english") + ["http", "https", "RT" ]
    freq_common_dist1 = nltk.FreqDist()
    freq_common_dist2 = nltk.FreqDist()
    for token in list1:
        if token not in stop_words and token.isalpha():
            if token in list2:
                freq_common_dist1[token] += 1
    for token in list2:
        if token not in stop_words and token.isalpha():
            if token in list1:
                freq_common_dist2[token] += 1
    return freq_common_dist1, freq_common_dist2

def find_dif_freqDist(tokenizedList1, tokenizedList2):
    list1 = join_tokenized_list(tokenizedList1)
    list2 = join_tokenized_list(tokenizedList2)
    stop_words = nltk.corpus.stopwords.words("english") + ["http", "https", "RT" ]
    freq_dif_dist1 = nltk.FreqDist()
    freq_dif_dist2 = nltk.FreqDist()
    for token in list1:
        if token not in stop_words and token.isalpha():
            if token not in list2:
                freq_dif_dist1[token] += 1
    for token in list2:
        if token not in stop_words and token.isalpha():
            if token not in list1:
                freq_dif_dist2[token] += 1
    return freq_dif_dist1, freq_dif_dist2


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()

    print('----------**Result for Extra 1**----------')
    (username1, num_tweets1) = input("Please type in the first username you want to compare, and the number of tweets you want to search(with a comma in between): ").split(",")
    (username2, num_tweets2) = input("Please type in the second username you want to compare, and the number of tweets you want to search(with a comma in between): ").split(",")
    
    
    
    # base_url_part2 = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    # response_part2 = requests.get(base_url_part2, {'screen_name': username, 'count': num_tweets}, auth = auth).text
    # tweetDictList_part2 = json.loads(response_part2)
    # print(params_unique_combination(username, get_tweet_id(tweetDictList_part2)))
    try:
        tweet_whole_dictList1 = get_tweet(username1, num_tweets1, auth)
    except:
        print('Oops! Invalid username1! Please try a different one. :)')
        quit()

    try:
        tweet_whole_dictList2 = get_tweet(username2, num_tweets2, auth)
    except:
        print('Oops! Invalid username2! Please try a different one. :)')
        quit()

    tweet_text_list1 = get_text_list(tweet_whole_dictList1)
    if tweet_text_list1 != []:
        tokenized_list1 = tweet_token(tweet_text_list1)

    tweet_text_list2 = get_text_list(tweet_whole_dictList2)
    if tweet_text_list2 != []:
        tokenized_list2 = tweet_token(tweet_text_list2)

    dif_word_fq1, dif_word_fq2 = find_dif_freqDist(tokenized_list1, tokenized_list2)

    common_word_fq1, common_word_fq2 = find_common_freqDist(tokenized_list1, tokenized_list2)
    
    print("the 5 most frequent different words for {} is:".format(username1))
    print(dif_word_fq1.most_common(5))
    print("the 5 most frequent different words for {} is:".format(username2))
    print(dif_word_fq2.most_common(5))
    print("the 5 most frequent common words for {} is:".format(username1))
    print(common_word_fq1.most_common(5))
    print("the 5 most frequent common words for {} is:".format(username2))
    print(common_word_fq2.most_common(5))
    print('-----------------------------------------')
