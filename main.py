from flask import Flask, request
import secrets
import time
import threading
import requests
import os

users = []

app = Flask(__name__)

def cleanup_loop():
    while True:
        time.sleep(1)
        now = int(time.time())
        global users
        users = [u for u in users if u["exp"] > now]
        channel_id = 1495458334117986417
        message_id = 1495458519845961728
        token = os.getenv("DISCORD_TOKEN")

        url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}"

        headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }

        data = {
            "content": f"# Currect Using: {len(users)}"
        }

        requests.patch(url, json=data, headers=headers)

threading.Thread(target=cleanup_loop, daemon=True).start()
@app.route("/")
def w_1():
    return "1|Hello Render or Idk twin", 200, {"Content-Type": "text/plain"}

@app.route("/currectuserusingtwin")
def w_3():
    return f"1|{len(users)}", 200, {"Content-Type": "text/plain"}

@app.route("/updatetwin")
def w_4():
    token = request.args.get("token")
    if token is None:
        return f"0|Some is None", 403, {"Content-Type": "text/plain"}
    updatetab = -1
    for i,v in enumerate(users):
        if v['token'] == token:
            updatetab = i
            break
    if updatetab is -1:
        return f"0|You not Exixts", 403, {"Content-Type": "text/plain"}
    users[updatetab]['exp'] = int(time.time()+15)
    return f"1|", 200, {"Content-Type": "text/plain"}

@app.route("/addmetwin")
def w_2():
    user = request.args.get("user")
    username = request.args.get("username")
    job = request.args.get("job")
    place = request.args.get("place")
    if user is None or username is None or job is None or place is None:
        return f"0|Some is None", 403, {"Content-Type": "text/plain"}
    for i in users:
        if i['userid'] == user or i['username'] == username:
            users.remove(i)
    token = secrets.token_hex(64)
    exp = int(time.time()+15)
    users.append({"userid": user,"username":username,"job":job,"place":place,"token": token,"exp":exp})
    return f"1|{token}|{exp}", 200, {"Content-Type": "text/plain"}

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
