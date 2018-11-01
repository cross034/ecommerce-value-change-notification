from html.parser import HTMLParser
import urllib.request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import os


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = 0

    def error(self, message):
        print("Error:", message)

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for attr in attrs:
                if attr[0] == 'class':
                    if attr[1] == '_1vC4OE _37U4_g':
                        MyHTMLParser.found = 1

    def handle_data(self, data):
        if self.found == 1:
            data = data.replace(",", "")
            if represents_int(data):
                int(data)
                global saved_price
                print("")
                if data != saved_price:
                    saved_price = data
                    send_mail(data)
                print(data + " at " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))

    def handle_endtag(self, tag):
        if tag == "div":
            MyHTMLParser.found = 0


def represents_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def send_mail(new_price):
    my_address = "my_email_address"
    my_password = "my_password"
    s = smtplib.SMTP(host="smtp.gmail.com", port=587)
    s.starttls()
    s.login(my_address, my_password)
    msg = MIMEMultipart()
    message = "New price: " + new_price
    msg['From'] = my_address
    msg['To'] = my_address
    msg['Subject'] = "Laptop price change"
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    s.quit()
    print("Mail sent")


saved_price = 0

if not os.path.isfile("price.txt"):
    with open("price.txt", "w") as file:
        file.write(str(0))

with open("price.txt") as file:
    saved_price = int(file.read())
    try:
        response = urllib.request.urlopen(
            '''https://www.flipkart.com/acer-nitro-5-core-i5-7th-gen-8-gb-1-tb-hdd-windows-10-home-2-gb-graphics-
            an515-51-gaming-laptop/p/itmf3s32dw3bhpgt?pid=COMEZZBCEGB6PZFM&srno=s_1_1&otracker=search&lid=LSTCOME
            ZZBCEGB6PZFMYZMRYC&fm=SEARCH&iid=a9e8fad2-4f0a-4ffc-b285-b50cb9c04926.COMEZZBCEGB6PZFM.SEARCH&ppt=Sea
            rch%20Page&ppn=Search%20Page&ssid=rn26xvf4f40000001525266016113&qH=6a476f61ea33f248'''
        )
        html_content = response.read()
        parser = MyHTMLParser()
        parser.feed(str(html_content))
    except Exception:
        print("Error at " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))

# <div class="_1vC4OE _37U4_g">\xe2\x82\xb9<!-- -->57,990</div>
