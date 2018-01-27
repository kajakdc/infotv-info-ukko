import os
import time
from slackclient import SlackClient

def run(command):
	splitted = command.split(" ", 2)
	
	if len(splitted) < 2:
		return "Command not complete"
		
	syntaxTree = {"motd": {"set": 1, "add": 1, "delete": 1, "list": 0}, "note": {"set": 1, "add": 1, "delete": 1, "list": 0, "priority": 2}}
	
	if not(splitted[0] in syntaxTree):
		return "Invalid target"
		
	if not(splitted[1] in syntaxTree[splitted[0]]):
		return "Invalid action"
		
	paramAmount = syntaxTree[splitted[0]][splitted[1]]
	parameters = command.split(" ", 1 + paramAmount)
	
	if len(parameters) != (2 + paramAmount):
		return "Invalid parameters"
	else:
		parameters = parameters[-(paramAmount + 1):]
		
	out = "Success"
		
	if splitted[0] == "motd":
		out = runMotd(parameters)
	elif splitted[0] == "note":
		out = runNote(parameters)
	
	return out
	
def runMotd(parameters):
	return "motd"
	
def runNote(parameters):
	return "note"
	
def post(target, action, data):
	pass

slackToken = os.environ["SLACK_API_TOKEN"]
apiIp = os.environ["API_IP"]
sc = SlackClient(slackToken)

if sc.rtm_connect(with_team_state=False):
	while True:
		time.sleep(1)
		messages = sc.rtm_read()
		if len(messages) > 0:
			for msg in messages:
				if "text" in msg and "user" in msg:
					command = msg["text"]
					respond = run(command)
					if respond != "":
						sc.rtm_send_message("D90DARZ9V", respond)
					
else:
	print "Connection to Slack failed"
