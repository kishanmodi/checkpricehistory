import telebot,time,os
from selenium import webdriver
from flask import Flask ,request

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"))

bot_token ="1322904062:AAGdsI7O7uNG4f1rhDmUriDuJFOQ40_3uTY"
bot = telebot.TeleBot(token=bot_token)

server = Flask(__name__)

kishan="https://t.me/kishanmodi/"
browser.get(r'https://pricehistory.in/')

def Check_price(product_url):
    #browser.get(r'https://pricehistory.in/')
    #time.sleep(5)
    search_item = browser.find_element_by_css_selector('body > div.w-full.mx-auto.bg-orange-200.dark\:bg-purple-800 > div > div > div > div:nth-child(4) > div.md\:flex.mt-2 > input')
    search_item.send_keys(product_url)
    #search_item.submit()
    time.sleep(5)
    click_on_your_product = browser.find_element_by_css_selector('#trackPriceBtn')
    click_on_your_product.click()
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
    #req = requests.post(browser.current_url, headers=headers)
    #req.raise_for_status()
    time.sleep(7)
    product_n= browser.find_element_by_css_selector('#name').text
    lowest_price =  browser.find_element_by_css_selector('#lowestPrice').text
    highest_price = browser.find_element_by_css_selector('#highestPrice').text
    current_price = browser.find_element_by_css_selector('#currentPrice').text
    if current_price=="Checking...":
        time.sleep(15)
        current_price = browser.find_element_by_css_selector('#currentPrice').text
    else:
        pass

    return current_price,lowest_price,highest_price,product_n


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Send Any Products Links from \n\"Flipkart, Amazon, Myntra, Chroma, AJIO.\"\nThis Bot will Provide Products Price History.\nWait For About 15 Seconds After sending The link")
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,'If You Find any problem or bug in this bot Contact\n' +kishan+"\nThank You")


@bot.message_handler(func = lambda msg: msg.text!=" ")
def at_answer(message):
    url = message.text
    #flipkart = "www.flipkart.com"
    #amazon = "www.amazon.in"
    #myntra = "www.myntra.com"
    #chroma = "www.chroma.com"
    #ajio = "www.ajio.com"

    #website_list=["www.flipkart.com","www.amazon.in","www.myntra.com","www.chroma.com","www.ajio.com"]
    #for website in website_list:    
    if "www" not in url:
        bot.reply_to(message,'Please Enter valid url')
    else:
        cur_price,low_price, max_price,product_name =Check_price(url)
        print(cur_price)
        print(low_price)
        fnamee=message.from_user.first_name
        #lname=message.from_user.last_name
        bot.reply_to(message,'\tThe Price Histroy For the Product\n'+product_name+'\n****************************\nCurrent Price is '+ cur_price +'\nLowest Price was '+ low_price +'\nHighest Price was '+ max_price+'\n****************************')
        bot.send_message(chat_id=418305384, text = fnamee + " used the Price History Bot For \n" + product_name +"\nMessage Id="+ str(message.chat.id) )


@server.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200   

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://price-tracker-amazon.herokuapp.com/' + bot_token)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))



'''
while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)

'''