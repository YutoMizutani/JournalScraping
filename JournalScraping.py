# (C) 2017 Yuto Mizutani
# coding: UTF-8

# --- Licenses (This software) ---
SOFTWARE_TITLE = "JournalScraping.py-Program"
SOFTWARE_VERSION = "Ver.1.0.3"
# created by Yuto Mizutani on 2017 Aug 18.
# Copyright © 2017年 Yuto Mizutani. All rights reserved.

# --- Development environment ---
# MacBook Pro (Retina, 13-inch, Mid 2015)
# macOS Serria version 10.12.6
# Python 3.6.1
# PyCharm Community Edition 2017.1.5

# --- References ---
# * Web scraping
#       http://qiita.com/Azunyan1111/items/9b3d16428d2bcc7c9406
# * Gmail sending
#       http://qiita.com/HirofumiYashima/items/1b24397c2e915658c984

# --- notes ---
# [BeautifulSoupライブラリのインストール]
# $ pip install beautifulsoup4
# [urllib2.urlopen()のPython3での構文エラー]
# *** import文 urllib2 は Python 3 にて urllib.request に変更 ***
# [使用不可なサイト]
# * ログインが必要なサイト


# --- Information ---
# Gmail側の設定 (2017/08/17時点)
# *** この方法はセキュリティ上問題がありそうなので，新しく専用のgoogleアカウントを作成することをおすすめします。 ***
# 1) Googleアカウントを作成
# 2) POPとIMAPの設定
#   2-1) Gmailを開き，受信トレイ画面の右上の歯車マークより，[設定]画面に移動
#   2-2) [メール転送と POP/IMAP]タブに移動する
#   2-3) [POP ダウンロード:]の[1. ステータス: POP 無効]のラジオボタンを[POP を有効にする]の選択肢からどちらか選択
#   2-4) [IMAP アクセス:]の[ステータス: IMAP 無効]のラジオボタン[IMAP を有効にする]を選択
#   2-5) 下部のボタン[変更を保存]を押す
#   2-6) 自動で受信トレイに遷移した後，再び[設定][メール転送と POP/IMAP]に移動し，3-1)，3-2)のステータスが有効になっていることを確認
# 3) セキュリティの設定
#   3-1) 右上のサムネイルの表示を押下し，[アカウント]を押し，[アカウント情報]ページに移動する
#   3-2) [ログインとセキュリティ]を押す
#   3-3) 左側のサイドバーよりログインとセキュリティの項にある[Googleへのログイン]を選択
#   3-4) [パスワードとログイン方法]の[2段階認証プロセス]を[オフ]にする
#   3-5) [ログインとセキュリティ]を押す
#   3-6) 再び左側のサイドバーよりログインとセキュリティの項にある[接続済みのアプリとサイト]を選択(下スクロールでも可)
#   3-7) [安全性の低いアプリの許可: 無効]を[有効]にする


# --Import--------------------------------------------------------------------------------------------------------------

# Repeat実行関係
from datetime import datetime
import time

# Web scraping関係
import urllib.request
from bs4 import BeautifulSoup
import re

# Gmail送信関係
import smtplib
from email.mime.text import MIMEText


# --Search text funcs---------------------------------------------------------------------------------------------------

def decisionIncludeKeyword(text, searchWord):
    if text == "":
        return False
    """[text]から[searchWordを検索] -> Bool """
    # print(searchWord in text)
    return searchWord in text


# ----BeautifulSoup4 funcs----------------------------------------------------------------------------------------------

def getUrl(url):
    # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
    return urllib.request.urlopen(url)


def convertBeautifulSoup(html):
    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    return soup


def pickupHref(soup, hrefNameString):
    href = soup.find_all(href=re.compile(hrefNameString))
    # print(href)
    # print(f"\n{len(href)}")
    return href


def findLoopFromArray(href, keywordString):
    # print("start loop!")
    count = 1
    count2 = 1
    for tag in href:
        # print(count)
        # print(tag)
        count += 1
        # 存在しない場合はNoneが返される。
        rawText = tag.get('title')
        if rawText is not None:
            # print(f"raw({count2}): {rawText}")
            count2 += 1
            if decisionIncludeKeyword(rawText, keywordString):
                print("指定された単語の存在を確認！")
                print(f"発見された単語({count}番目): {rawText}")
                return rawText
    return ""


def sraipingUsingBeautifulSoup4(url, classNameString, keywordString):
    result = findLoopFromArray(
        pickupHref(
            convertBeautifulSoup(
                getUrl(url)
            ),
            classNameString),
        keywordString
    )
    if result != "":
        resultText = f"指定された単語の存在を確認しました！: {result}"
    else:
        resultText = "指定された単語の存在は認められませんでした。"
    print(resultText)
    return result


# ----Gmail class-------------------------------------------------------------------------------------------------------

class sendGmail:
    def __init__(self, username, password, to, sub, body):
        host, port = 'smtp.gmail.com', 465
        msg = MIMEText(body)
        msg['Subject'] = sub
        msg['From'] = username
        msg['To'] = to

        smtp = smtplib.SMTP_SSL(host, port)
        smtp.ehlo()
        smtp.login(username, password)
        smtp.mail(username)
        smtp.rcpt(to)
        smtp.data(msg.as_string())
        smtp.quit()


# ----main funcs-------------------------------------------------------------------------------------------------------


def MainFunc01_WebScraping():
    RESULT = sraipingUsingBeautifulSoup4(URL, HREF_NAME_STRING, KEYWORD_STRING)
    return [URL, RESULT]


def MainFunc02_SendGmail(url, webScrapingResult):
    global SOFTWARE_TITLE
    global SOFTWARE_VERSION
    SUB = "[PythonWebScraping]変更を検知しました。"
    SOFTWARE = SOFTWARE_TITLE + "(" + SOFTWARE_VERSION + ")"
    BODY = f'{SOFTWARE}にて更新指定したキーワードがWebScrapingにて発見されました。\n\n検索URL: {url}\n発見されたキーワード: {webScrapingResult}'

    print(f"From: {GMAIL_LOGIN_ADDRESS}")
    print(f"To: {TO}")
    print(f"Subject: {SUB}")
    print(f"Body: {BODY}")

    sendGmail(GMAIL_LOGIN_ADDRESS, GMAIL_PASSWORD, TO, SUB, BODY)


# ----Parameters--------------------------------------------------------------------------------------------------------

"""ここを変更して設定してください。"""

# URL: アクセスするURL(String型)
# e.g. URL = "https://www.journals.elsevier.com/behavioural-brain-research/recent-articles"
URL = ""
# href: ブラウザから抽出したい部分を範囲選択し，指定部分をInspect。
#           表示されたhtmlタグから抽出したい href=""共通部分を記述。
#           リンク先に飛べる文字を取得し，そのジャーナルタイトルを検索
HREF_NAME_STRING = "http://www.sciencedirect.com/science/article/pii/"
# Keyword: 更新されたか探すテキスト(論文タイトル)。
# ここをキーワードにするとそのキーワードが含まれるジャーナルの更新を監視することが可能。
# e.g. KEYWORD_STRING = "Operant Models of Relapse in Zebrafish"
KEYWORD_STRING = ""

# 送信元のGmailアドレス
GMAIL_LOGIN_ADDRESS = "xxxxxxxxxxxxxxxxx@gmail.com"
# 送信元のGmailログインパスワード
GMAIL_PASSWORD = "xxxxxxxxxxxxxxxxx"
# 送信先（通知を受信したいメールアドレス）
TO = "xxxxxxxxxxxxxxxxxx@xxxxxxxxxx.xxxx"

# テストの際にはTrueに指定して即時実行
IS_TEST = False

# 時間指定(EXPAND_HOUR時EXPAND_MINUTES分を基準にTIME_INTERVALS_HOUR時間おき)
# *** TIME_INTERVALS_HOUR は1以上を指定してください。***
EXPAND_HOUR = 0
EXPAND_MINUTES = 30
TIME_INTERVALS_HOUR = 1


# ----main--------------------------------------------------------------------------------------------------------------


# main

print(f"{SOFTWARE_TITLE}({SOFTWARE_VERSION}) Copyright 2017 Yuto Mizutani")
print(f"[URL: {URL}]より[文字列: {KEYWORD_STRING}]を定期探索し，発見した場合にGmailに向けて送信します。")
print("start....")

print(f"TEST_MODE: {IS_TEST}")

if not IS_TEST:
    print(f"定期更新処理を開始しました。この処理は{EXPAND_HOUR}時{EXPAND_MINUTES}分を基準に{TIME_INTERVALS_HOUR}時間毎に実行されます。")
    # 永久に実行させます
    while True:
        # 現在時刻の取得
        nowHour = datetime.now().hour
        # 現在時刻が基準時刻を下回っていれば+24hで調整。
        if nowHour < EXPAND_HOUR:
            nowHour += 24
        # 0分指定の場合，-1分でなく-1h59mとなるため，if文で分ける。
        if EXPAND_MINUTES == 0:
            # 指定時間の1分前[(X-1):59]以外は58秒間時間を待機する
            if ((nowHour - EXPAND_HOUR) % TIME_INTERVALS_HOUR != TIME_INTERVALS_HOUR-1) or (datetime.now().minute != 59):
                # 59分ではないので1分(58秒)間待機します(誤差がないとは言い切れないので58秒です)
                time.sleep(58)
                continue
        else:
            # 指定時間の1分前[(X-1):59]以外は58秒間時間を待機する
            if ((nowHour - EXPAND_HOUR) % TIME_INTERVALS_HOUR != 0) or (datetime.now().minute != EXPAND_MINUTES-1):
                # 59分ではないので1分(58秒)間待機します(誤差がないとは言い切れないので58秒です)
                time.sleep(58)
                continue

        # 59分になりましたが正確な時間に測定をするために秒間隔で59秒になるまで抜け出せません
        while datetime.now().second != 59:
            # 00秒ではないので1秒待機
            time.sleep(1)
        # 処理が早く終わり二回繰り返してしまうのでここで一秒間待機します
        time.sleep(1)

        print(f"{datetime.now()}: web scraping running...")
        rawResult = MainFunc01_WebScraping()
        if rawResult[1] != "":
            # 発見されたらGmailにて通知を行い，処理を終了する
            print(f"キーワード: [{KEYWORD_STRING}]が発見されました。")
            MainFunc02_SendGmail(rawResult[0], rawResult[1])
            break
        else:
            continue
else:
    print(MainFunc01_WebScraping())
