from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACfe19105a3aa7d11c16d6272a0d3eccda"
# Your Auth Token from twilio.com/console
auth_token  = "cfbab195621b28a0753619e06ce95fe4"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+19144140230", 
    from_="+19707139622",
    body="this is max! i'm eating falafel HAHAHAHAHA")

print(message.sid)