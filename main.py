import requests
from bs4 import BeautifulSoup
from mstranslator import Translator
import pinyin
import pandas
import smtplib
import random

AZURE_KEY = 'MY_KEY'
MY_EMAIL = "MY_EMAIL@gmail.com"
MY_PASSWORD = "MY_PASSWORD!"

translator = Translator(AZURE_KEY)
cankaoxiaoxi_url = "http://www.cankaoxiaoxi.com/"

cankaoxiaoxi_titles_cn = []
cankaoxiaoxi_titles_en = []
final_translations_list = []

data = pandas.read_csv("users.csv")
users_dict = {(data_row["name"], data_row["email"]): data_row for (index, data_row) in data.iterrows()}

def send_emails():
    for user in users_dict:
        final_content = " "
        final_content = final_content.join(final_translations_list)

        file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
        with open(file_path) as letter_file:
            contents = letter_file.read()
            contents = contents.replace("[NAME]", user[0])
            contents = contents.replace("[CONT]", final_content)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=user[1],
                msg=contents
            )

def return_cankaoxiaoxi():
    response = requests.get(cankaoxiaoxi_url)
    cankaoxiaoxi_html = response.text
    cankaoxiaoxi_soup = BeautifulSoup(cankaoxiaoxi_html, "html.parser")

    for main_title in cankaoxiaoxi_soup.find_all("h2"):
        main_titles_string = str(main_title.string)
        cankaoxiaoxi_titles_cn.append(main_titles_string)

    for secondary_title in cankaoxiaoxi_soup.find_all("h3"):
        secondary_title_string = secondary_title
        cankaoxiaoxi_titles_cn.append(secondary_title_string.text)

def return_text_and_translation():
    final_translations_list.append(f"NEWS FROM {cankaoxiaoxi_url}:\n\n")
    for index in range(0, len(cankaoxiaoxi_titles_cn)):
        final_translations_list.append(f'{cankaoxiaoxi_titles_cn[index]}\n')
        pinyin_text = pinyin.get(cankaoxiaoxi_titles_cn[index], format="strip", delimiter=" ")
        final_translations_list.append(f'{pinyin_text}\n')
        english_text = translator.translate(cankaoxiaoxi_titles_cn[index], lang_from='zh-CN', lang_to='en')
        final_translations_list.append(f'{english_text}\n\n')


return_cankaoxiaoxi()
return_text_and_translation()
send_emails()
