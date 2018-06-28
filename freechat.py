from asn1crypto.cms import RoleSyntax
from flask import Flask
from flask import render_template, request, Response
from flask_socketio import *
# from pip._vendor.requests.packages.urllib3 import response
# from urllib3 import response
from random import shuffle
import re
# import requests


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'siver'
socketio = SocketIO(app, async_mode=async_mode)

global chat_session
chat_session = {}

def chatUpdate(act, message):
    if message['room'] in chat_session:
        player = message['pname']
        players = chat_session[message['room']]
        if player in players:
            return 101
        if act == "Add":
            chat_session[message['room']] += [message['pname']]
    else:
        if act == "Add":
            chat_session.update( {message['room'] : [message['pname']]} )
    return 0

@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')
    
@socketio.on('welcome')
def welcome():
    emit('welcome','welcome!')

@socketio.on('locate')
def locate_room(message):
    code = chatUpdate("Check",message)
    if code == 101:
        emit('sysmsg', {'pname' : message['pname'], 'room' : str(message['room'])})
        return False
    emit('locate',
         {'room': message['room'], 'pname':message['pname'],
          'url':'/room/' + str(message['room'])})
    
@socketio.on('clearroom')
def clear_room(message):
    chat_session[message['room']].clear()
    
#     print(chat_session)
#     leave_room(message['room'])
    
@socketio.on('join')
def join(message):
    code = chatUpdate("Add", message)
    if code == 101:
        emit('sysmsg', {'pname' : message['pname'], 'room' : str(message['room'])})
        return False

    join_room(message['room'])
    room_mates = chat_session[message['room']]
    emit('room', 
         {'room_mates' : room_mates },
         room=message['room'])

@socketio.on('leave')
def leave(message):
    try:
        chat_session[message['room']].remove(message['pname'])
        
        emit('roommsg', 
             {'pname' : "System" , "data" : message['pname'] + " has left the room..." },
             room=message['room'])
        emit('room', 
             {'room_mates' : chat_session[message['room']] },
             room=message['room'])
        
        leave_room(message['room'])
    
    except:
        pass
    
@socketio.on('roommsg')
def room_message(message):
    emit('roommsg', 
        {'pname':message['data']['pname'], 'data':message['data']['msg']}, 
         room=message['room'])

@socketio.on('gamestart')
def gamestart(message):
    roles = []
    players = {}
    werewolf = ''
    room = int(message['room'])
    pname = message['pname']
    
    roles = app_role(roles, int(message['werewolf']), 'werewolf')
    roles = app_role(roles, int(message['villager']), 'villager')
    roles = app_role(roles, int(message['seer']), 'seer')
    roles = app_role(roles, int(message['hunter']), 'hunter')
    roles = app_role(roles, int(message['witch']), 'witch')
    roles = app_role(roles, int(message['idiot']), 'idiot')

    if len(chat_session[room]) != len(roles):
        emit('roommsg', 
             {'pname': 'System', 'data': 'Player and role are not match!'}, 
             room=room)
        return False
    else:
        i = 0
        shuffle(roles)
        while i<len(roles):
            players.update( {chat_session[room][i] : roles[i]} )
            if roles[i] == 'werewolf':
                werewolf += '[' + chat_session[room][i] + '], '
            i += 1
        print(players)
        emit('players',
             {'players' : players, 'werewolf' : werewolf},
             room=room)
    

def app_role(roles,count,role):
    i = 0
    while i < count:
        i += 1
        roles.append(role)
    return roles

@socketio.on('actionmsg')
def actionmsg(message):
#     print(message)
    emit('actionmsg', 
             {'pname': message['pname'], 'room': message['room'], 'role': message['role'], 'target':message['target']}, 
             room=message['room'])


@socketio.on('wolfmsg')
def wolf_message(message):
    emit('confirmmsg', 
             {'pname': message['pname'], 'room': message['room'], 'role': message['role'], 'target':message['target']}, 
             room=message['room'])

@socketio.on('huntermsg')
def hunter_message(message):
    emit('huntermsg', 
             {'target': message['target']}, 
             room=message['room'])

@socketio.on('seermsg')
def seer_message(message):
    emit('seeract', 
             {'pname': message['pname'], 'room': message['room'], 'role': message['role'], 'target':message['target']}, 
             room=message['room'])
    
@socketio.on('seeract')
def seer_action(message):
    emit('confirmmsg', 
             {'pname': message['pname'], 'room': message['room'], 'role': message['role'], 'target':message['target'], 'ind':message['ind']}, 
             room=message['room'])

@socketio.on('endday')
def end_day(message):
    emit('endday', 
             {'msg': message['msg']}, 
             room=message['room'])

@app.route('/')
def index():
    return render_template('FreeChat.html')

@app.route('/room/<room>')
def room(room):
#     pname = request.values.get('player')
    return render_template('room.html', room = room)

if __name__ == '__main__':
#     socketio.run(app, port=5000, debug=True)
	socketio.run(app,host="0.0.0.0", port=5000)
    