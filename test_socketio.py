import time
import requests
import socketio

BASE_URL = "http://localhost:8080"
EMAIL = "admin@example.com"
PASSWORD = "admin123"
CHAT_ID = 1  # подставь свой id чата

http_session = requests.Session()

login_resp = http_session.post(
    f"{BASE_URL}/api/auth/login",
    json={"email": EMAIL, "password": PASSWORD},
    timeout=10,
)
print("login:", login_resp.status_code, login_resp.text)

sio = socketio.Client(http_session=http_session, logger=True, engineio_logger=True)

@sio.event
def connect():
    print("connected")

@sio.on("joined_chat")
def on_joined(data):
    print("joined_chat:", data)

@sio.on("new_message")
def on_new_message(data):
    print("new_message:", data)

@sio.on("error")
def on_error(data):
    print("error:", data)

@sio.event
def disconnect():
    print("disconnected")

sio.connect(BASE_URL, transports=["polling", "websocket"])
sio.emit("join_chat", {"chat_id": CHAT_ID})
time.sleep(1)
sio.emit("send_message", {"chat_id": CHAT_ID, "text": "hello from websocket"})
time.sleep(2)
sio.disconnect()