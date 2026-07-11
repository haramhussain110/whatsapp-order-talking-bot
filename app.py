from flask import Flask ,request
import requests
import os
import csv 
from datetime import datetime 
from dotenv import load_dotenv


load_dotenv()
BASE_DIR =os.path.dirname(os.path.abspath(__file__))
ORDER_FILE = os.path.join(BASE_DIR,"order.csv")
app = Flask(__name__)

VERIFY_TOKEN ="haram123secret"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
user_carts= {}
menu_items = {"1":{"name":"Burger","price":200},
              "2":{"name":"Pizza","price":500},
              "3":{"name":"Fries","price":150}

}

def send_message(to,message_text):
    url =f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
            "Authorization":f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
    }

    playload = {
        "messaging_product":"whatsapp",
        "to":to,
        "type" :"text" ,
        "text":{"body":message_text} 
         
    }
    response =requests.post(url,headers=headers ,json=playload)
    print(response.status_code,response.text    )

def save_order(sender,cart,total):
    file_exists = os.path.isfile(ORDER_FILE)
    with open(ORDER_FILE,"a",newline="") as f:
        writer = csv.writer(f)
        
        if not file_exists:
            writer.writerow(["Timestamp","Customer","Items","Total"])

        item_str   =",".join([item["name"] for item in cart ])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),sender , item_str,total])

@app.route('/webhook',methods =["GET","POST"])
def verify_webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge =request.args.get("hub.challenge")

        # return "webhook is working "
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge ,200
        else:
            return "verification Failed  ",403
    elif request.method =="POST":
        data = request.get_json()      
        print(data)

        try:
            entry =data["entry"][0]
            changes =entry["changes"][0]
            value =changes["value"] 


            messages =value.get("messages")
            
            if messages :
                sender =messages[0]["from"]
                text = messages[0]["text"]["body"]
                print(f"Messages from {sender}: {text}")

                # send_message(sender,f"you did write :{text}")


                # if text== "1":
                #     send_message(sender,"you selected Burger :Rs 200 ")
                # elif text =="2":
                #     send_message(sender,"you selected pizza : Rs 500")
                # elif text =="3":
                #     send_message(sender,"you selected Fries :Rs 150")

                if text in menu_items:
                    if sender not in user_carts:
                        user_carts[sender] = []

                    item= menu_items[text]
                    user_carts[sender].append(item)


                    send_message(sender,f"{item['name']} added to your cart!  \n Types another number for else order ")
                elif text.lower()== "done":
                    cart= user_carts.get(sender,[])
                    if not cart:
                        send_message(sender,"Your cart is empty!  Please selected an item first ")
                                                
                    else:
                        total =sum(item["price"] for item in cart)
                        order_summary ="your order :\n"
                        for item in cart :
                            order_summary +=f"-{item['name']} :Rs {item['price']}\n"
                        order_summary +=f"\n Total Rs:{total}\n Thankyou for your order"
                        send_message(sender,order_summary)
                        save_order(sender,cart,total)
                        user_carts[sender]= []
                else:


                    menu =(
                        "Welcome to QuickOrderBot! \n"     
                        "please choose and item by typing its number: \n\n"
                        "1. Burger - Rs 200 \n"
                        "2. pizza  - Rs 500 \n "
                        "3. Fries - Rs. 150 \n"

                    )
                    send_message(sender,menu)
        except Exception as e :
            print("Error:",e)
            

        return "OK",200
    

if __name__ == "__main__":
    app.run(port=5000)

