import socketio

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    # Send a test message
    sio.emit('message', 'Hello Server!')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('message')
def on_message(data):
    print('Received message:', data)

# Connect to the Flask-SocketIO server
sio.connect('http://localhost:5000')
sio.wait() 