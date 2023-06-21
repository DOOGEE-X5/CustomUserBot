from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from time import sleep

api_id = 0
api_hash = ""
Text = ""

def MainMenu():
    global api_id 
    global api_hash

    try:
        with open('Config.ini', 'r') as File:
            lines = File.readlines()
            api_id = lines[1].strip().split("api_id = ", maxsplit=1)[1]
            api_hash = lines[2].strip().split("api_hash = ", maxsplit=1)[1] 
            print("Run ...") 

    except FileNotFoundError:
        print("Login ty Pyrogram")
        api_id = input("api_id = ")
        api_hash = input("api_hash = ")

        with open('Config.ini', 'w') as File:
            File.write("[pyrogram]\n")
            File.write("api_id = {}\n".format(api_id))
            File.write("api_hash = {}\n".format(api_hash))        
            print("Run ...")

    except Exception as e:
        print("Close ...\n Error: ",e)
        close()

MainMenu()

app = Client("my_account", api_id=api_id, api_hash=api_hash)


#############################################################################################
#                               команда /Users                                              #
#############################################################################################

@app.on_message(filters.command("Users", prefixes="/") & filters.me)
def Users(client, msg):
    count =0;
    TARGET = msg.text.split("/Users ", maxsplit=1)[1] # очистив команду от "/Users " тим самим оставив токо цель(id чата)    
    User = app.get_me()
    UserID = User.id
    
    with open(f"Results/ResultTarget{TARGET}.txt", "w") as File:
        with open(f"UserBase/UserBase{TARGET}", "w") as Users:
            for member in app.get_chat_members(TARGET): 
                if member.user.id != UserID: 
                    File.write("ID: {}\n".format(member.user.id))
                    if member.user.username is not None:
                        File.write("Username: {}\n".format(member.user.username))
                        Users.write("@{}\n".format(member.user.username))
                    else: 
                        File.write("First_name {}\n".format(member.user.first_name))
                        File.write("Last_name {}\n".format(member.user.last_name))
                    if member.user.phone_number is not None: 
                        File.write("Phone: {}\n".format(member.user.phone_number))
                        count = count + 1;
                    else: 
                        File.write("Phone: {}\n".format(member.user.phone_number))
                    File.write("Status: {}\n".format(member.user.status))
                    File.write("============================\n")

    # отправка файла-результата...    
    ChatID = msg.chat.id
    with open(f"Results/ResultTarget{TARGET}.txt", "rb") as File:
        app.send_document(ChatID, File)
        
    msg.reply_text("Записей с номером телефона: " + str(count))

#############################################################################################
#                                команда /Message                                           #
#############################################################################################

@app.on_message(filters.command("Message", prefixes="/") & filters.me)
def MessageAll(_, msg):
    global Text
    UserList = ""
    TARGET = msg.text.split("/Message ", maxsplit=1)[1]

    with open(f"UserBase/UserBase{TARGET}", "r") as File:
        for line in File:
            UserList = UserList + line.rstrip() + " "
    
    Message = app.send_message(chat_id=TARGET, text=UserList, disable_notification=True)   
    app.edit_message_text(chat_id=TARGET, message_id=Message.id, text=Text)
    
    
#############################################################################################
#                                    команда /Help                                          #
#############################################################################################

@app.on_message(filters.command("Help", prefixes="/") & filters.me)
def NumberPhone(_, msg):
    msg.reply_text("=> /Help - Визов справки\n=> /Users (ID чата-цели) - Сканирование чата\n=> /Message (ID чата-цели) - Отправка сообщения\n=> /SaveMessage (Текст сообщения) - Сохранить в файл текст сообщения\n=> /SetMessage (текст сообщения) - Задать текст сообщения\n=> /LoadMessage - Загрузить текст с файла", quote=True)    


############################################################################################# 
#                                 команда /SaveMessage                                      #
#############################################################################################

@app.on_message(filters.command("SaveMessage", prefixes="/") & filters.me)
def NumberPhone(_, msg):
    global Text
    
    Text = msg.text.split("/SaveMessage ", maxsplit=1)[1]
    with open(f"TextMessage/Message", "w") as File:       
        File.write(Text)
    msg.reply_text("Текст сохранен и задан", quote=True)

        

#############################################################################################
#                                 команда /SetMessage                                       #           
#############################################################################################

@app.on_message(filters.command("SetMessage", prefixes="/") & filters.me)
def NumberPhone(_, msg):
    global Text
    
    Text = msg.text.split("/SetMessage ", maxsplit=1)[1]
    msg.reply_text("Текст задан", quote=True)

#############################################################################################
#                                 команда /ShowMessage                                      #           
#############################################################################################

@app.on_message(filters.command("ShowMessage", prefixes="/") & filters.me)
def NumberPhone(_, msg):
    global Text
    
    if Text != "":
        msg.reply_text(Text, quote=True)
    else:
        msg.reply_text("Текст не задан", quote=True)


#############################################################################################
#                                 команда /LoadMessage                                      #           
#############################################################################################

@app.on_message(filters.command("LoadMessage", prefixes="/") & filters.me)
def NumberPhone(_, msg):
    global Text
    
    try:
        with open('TextMessage/Message', 'r') as File:
            Text = file.read()
            msg.reply_text("Загружено: " + Text, quote=True)    
    except FileNotFoundError:
        msg.reply_text("Файл не найден", quote=True) 
    except Exception as e:
        msg.reply_text("Произошла ошибка при открытии файла", quote=True) 
             

app.run()

