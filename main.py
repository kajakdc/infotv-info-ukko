import os
import time
import requests
from slackclient import SlackClient

def run(command):

	if command == "help":
		return "motd: txt <text>, img <url>, showTxt <text>, showImg <url>, showId <id>, delete <id>, list, listId <id>\nnote: add <text>, delete <id>, list, listId <id>, priority <id> <priority>, show <id> <state>"

	splitted = command.split(" ", 2)
	
	if len(splitted) < 2:
		return "Command not complete"
	
	syntaxTree = {"motd": {"txt": 1, "img": 1, "showTxt": 1, "showImg": 1, "showId": 1, "delete": 1, "list": 0, "listId": 1}, "note": {"add": 1, "delete": 1, "list": 0, "listId": 1, "priority": 2, "show": 2}}
	
	# list = GET
	# listId = GET /id
	# txt = POST data 1
	# img = POST data 0
	# showTxt = PUT data 1
	# showImg = PUT data 0
	# showId = PUT /id
	# delete = DELETE /id

	# list = GET
	# listId = GET /id
	# add = POST data
	# show = PUT /id active
	# priority = PUT /id priority
	# delete = DELETE /id

	
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
	id = ""
	method = ""
	params = {}
	
	print parameters
	
	if parameters[0] == "list":
		method = "GET"

	elif parameters[0] == "listId":
		method = "GET"
		id = parameters[1]
	
	elif parameters[0] == "txt":
		method = "POST"
		params = {"Data": parameters[1], "Type": "0"}
		
	elif parameters[0] == "img":
		method = "POST"
		params = {"Data": parameters[1], "Type": "1"}
		
	elif parameters[0] == "showTxt":
		method = "PUT"
		params = {"Data": parameters[1], "Type": "0"}
		
	elif parameters[0] == "showImg":
		method = "PUT"
		params = {"Data": parameters[1], "Type": "1"}
		
	elif parameters[0] == "showId":
		method = "PUT"
		id = parameters[1]
		
	elif parameters[0] == "delete":
		method = "DELETE"
		id = parameters[1]

	print method
	print id
	print params
		
	response = makeRequest(method, "motd", id, params)
		
	print response
		
	return response
	
def runNote(parameters):
	id = ""
	method = ""
	params = {}
	
	print parameters
	
	if parameters[0] == "list":
		method = "GET"
		
	elif parameters[0] == "listId":
		method = "GET"
		id = parameters[1]
	
	elif parameters[0] == "add":
		method = "POST"
		params = {"Data": parameters[1], "Active": "1", "Priority": "0"}
		
	elif parameters[0] == "show":
		method = "PUT"
		id = parameters[1]
		params = {"Active": parameters[2]}
	
	elif parameters[0] == "priority":
		method = "PUT"
		id = parameters[1]
		params = {"Priority": parameters[2]}
		
	elif parameters[0] == "delete":
		method = "DELETE"
		id = parameters[1]
	
	print method
	print id
	print params
		
	response = makeRequest(method, "note", id, params)
		
	print response
		
	return response
	
def makeRequest(method, target, id, params):

	url = "http://" + os.environ["API_IP"] + ":" + os.environ["API_PORT"] + "/api/" + target + "/" + id

	print url
	
	if method == "GET":
		 r = requests.get(url)
	elif method == "POST":
		r = requests.post(url, data=params)
	elif method == "DELETE":
		r = requests.delete(url)
	elif method == "PUT":
		r = requests.put(url, data=params)
	else:
		return ""
		
	return r.text
	
slackToken = os.environ["SLACK_API_TOKEN"]
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
