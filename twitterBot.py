import requests
import json
import tweepy
import time
import random as rd

timeToWait = 300
threshold = 1000

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

def getLatestTransactionsFromSyntExchanges(sinceLastTime):
        url = "https://api.thegraph.com/subgraphs/name/synthetixio-team/synthetix-exchanges"
        payload= "{\"query\":\"{synthExchanges(orderBy: timestamp, orderDirection: desc, where:{timestamp_gte:" + \
                                                                                                str(sinceLastTime) + "})\
                                                                                                {account fromCurrencyKey \
                                                                                                fromAmount fromAmountInUSD\
                                                                                                toCurrencyKey toAmount \
                                                                                                toAmountInUSD}}\",\"variables\":{}}"
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()['data']['synthExchanges'] 

def getTextToPost(rawTransactionData):
    textToPost = ''
    response = ''
    try:
        API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-1.3B"
        headers = {"Authorization": "Bearer API_KEY_HUGGINGFACE"}
        seeds = {"head": ["New transaction", "New trade", "Trade"], "verb":["has occured", "is done"],"tail":["on a blockchain", "with help of smart contract", "on ethereum", "with synth asset"]}
        payload = {"inputs": seeds['head'][rd.randrange(0, len(seeds['head']))] + " " +  \
                   seeds['verb'][rd.randrange(0, len(seeds['verb']))] + " " + \
                   seeds['tail'][rd.randrange(0, len(seeds['tail']))], \
                   "parameters": {"max_new_tokens": 50}, "options": {"use_cache": False}}
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        textToPost = json.loads(response.content.decode("utf-8"))[0]['generated_text'] + \
                                "\nAnyway here are details https://etherscan.io/address/" +str(rawTransactionData['account']) + \
                                " From " + str(int(rawTransactionData['fromAmount'])/1e18) + " " + \
                                bytes.fromhex(rawTransactionData['fromCurrencyKey'][2:]).decode() + \
                                " To " + str(int(rawTransactionData['toAmount'])/1e18) + " " +\
                                bytes.fromhex(rawTransactionData['toCurrencyKey'][2:]).decode()
    except Exception as e:
        textToPost = "New trade\nWallet\n" + "https://etherscan.io/address/" + str(rawTransactionData['account']) + \
                     " From " + str(int(rawTransactionData['fromAmount'])/1e18) + " " + \
                     bytes.fromhex(rawTransactionData['fromCurrencyKey'][2:]).decode() + \
                     " To " + str(int(rawTransactionData['toAmount'])/1e18) + " " + \
                     bytes.fromhex(rawTransactionData['toCurrencyKey'][2:]).decode()
    return textToPost

def sendTweet(text):
    print(api.update_status(text))


while True:
    transactionsToTweet = getLatestTransactionsFromSyntExchanges(int(time.time()) - timeToWait)
    for transactionData in transactionsToTweet:
        if int(transactionData['fromAmountInUSD'])/1e18 > threshold:
            print("sending tweet")
            sendTweet(getTextToPost(transactionData))
            time.sleep(5)
    print("nothing to post")
    time.sleep(timeToWait)
    
