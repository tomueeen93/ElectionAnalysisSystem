#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,os
sys.path.append('./lib')

from requests_oauthlib import OAuth1Session
import csv
import json
import os
import MeCab
import time

### MeCabの設定
MECAB_MODE = '-Ochasen'
PARSE_TEXT_ENCODING = 'utf-8'

### アクセストークンの設定
oath_key_dict = {
    "consumer_key": "k7whxKvglFTW2M4A5p84FwkAY",
    "consumer_secret": "ivTDxzf48lCNhGoWbG1xghYaUvtgIla3mhGS3PHzbQhrxbdrB1",
    "access_token": "550939620-aUvLCdpSyhBMStRNRwQ93iJlu4SOuz3P9SL8gfD6",
    "access_token_secret": "s7tlpDGzM2apzvLRZnG7kxpV1Jbx9vKp0ptTyfd1PnMSX"
}

## 辞書の設定
dictionary = {} # 単語(漢字)と点数の辞書
dictionary2 = {} # 単語(ひらがな)と点数の辞書


f = open("C:/Users/admin/Documents/research/workspace/tweet_data/tweetdata1.csv","a")
time.sleep(1.0)
### Functions
def main():
    # tweetの取得
    tweets = tweet_search(u"自民党", oath_key_dict)

    # Mecabの取得
    mt = MeCab.Tagger("-Ochasen")

    # 辞書の作成
    dictionary = generate_dictionary()
    print "----------------------------------"
    ## 全ツイートを解析
    for tweet in tweets["statuses"]:
        ## ツイートの中身を取得
        text = tweet[u'text']
        text = text.replace('\n','')
        ## ツイートを表示
        print type(text)
        ## sumを表示
        result_sum = calcrate_sum(text)
        print result_sum
        result = text + u"," + unicode(result_sum) + u"\n"
        print result
        f.write(result.encode('utf-8'))
        print "----------------------------------"
    return

## ツイートの点数を計算
def calcrate_sum(tweet_text):
    # 合計点
    sum = 0

    ## 解析するテキストの設定
    sample_u = tweet_text;
    ## MeCabによる形態素解析
    words_dict = parse(sample_u.encode('utf-8'))
    ## 解析結果を配列に変更
    words = []
    words ="All:",",".join(words_dict['all']).split(",")

    # 辞書の確認(速度低下)
    # print len(dictionary)
    #for k, v in dictionary.items():
        #print k, v
    
    # 全ての単語を調べる
    for word in words[1]:
        # 辞書にkeyが含まれていたら
        if word in dictionary:
            # 辞書に書いてある点数を合計点に足す
            sum += float(dictionary[word]) 
            print word.decode('utf-8'),dictionary[word]
    print "calcrated sum"
    return sum

## 辞書の生成
def generate_dictionary():
    dict_data = {}

    ## 辞書を開く
    f = open('japan2.csv','rb')
    dataReader = csv.reader(f)
    print "loaded csv data"

    for row in dataReader:
        # 辞書の生成
        dictionary[row[0]]= row[3]
        # ひらがな用
        # dictionary2[row[1]]= row[3]

    print "created word dictionary"

    return dict_data

## 形態素解析の実行
def parse(unicode_string):
    tagger = MeCab.Tagger('-Ochasen')
    # str 型じゃないと動作がおかしくなるので str 型に変換
    text = unicode_string
    node = tagger.parseToNode(text)

    words = []
    nouns = []
    verbs = []
    adjs = []
    while node:
        pos = node.feature.split(",")[0]
        # unicode 型に戻す
        word = node.surface
        if pos == "名詞":
            nouns.append(word)
        elif pos == "動詞":
            verbs.append(word)
        elif pos == "形容詞":
            adjs.append(word)
        words.append(word)
        node = node.next
    parsed_words_dict = {
        "all": words[1:-1], # 最初と最後には空文字列が入るので除去
        "nouns": nouns,
        "verbs": verbs,
        "adjs": adjs
        }
    return parsed_words_dict

## セッションの作成
def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )
    return oath

# tweetの取得
def tweet_search(search_word, oath_key_dict):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": search_word,
        "lang": "ja",
        "result_type": "recent",
        "count": "30"
        }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    tweets = json.loads(responce.text)
    return tweets

### 実行用
if __name__ == "__main__":
    main()
