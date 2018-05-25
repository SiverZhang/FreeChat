from twilio.rest import Client


# Your Account SID from twilio.com/console
account_sid = "ACcf340d2fe07d1e3ee7339564520d6de8"
# Your Auth Token from twilio.com/console
auth_token  = "c24d192f74e45a86a2cddeaebbbd1940"

client = Client(account_sid, auth_token)

'''
message = client.messages.create(
    to="+86 186-9617-8080", 
#     to="+1 808-518-6110", 
    from_="+1 808-518-6110",
#     from_="+86 186-9617-8080",
    body="Message2 -- Hello from Python!")

print(message.sid)
'''


call = client.calls.create(
    to="+8618696178080", 
    from_="+1 808-518-6110",
    url="https://demo.twilio.com/welcome/voice/"
)

print(call.sid)
