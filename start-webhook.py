import subprocess


from flask import Flask, request
from conf import *

app = Flask(__name__)


def print_log(date,reponame,user,fromhash,tohash):
	log = open(log_file, "a")
	record =  date+" - "+reponame+" - "+user+" - "+fromhash+" - "+tohash+"\n"
	log.write(record)
	log.close()

def print_hello():
    message = "Ibra Webhook server online! Go to http://localhost:9988"
    print message


def web_info(request):
    url_root = request.url_root
    return "".join([
            """Great Ibra Webhook server online! :) </br>""",
            """Go to <a href="https://github.com/ihalloum/bitbucket-webhook">README</a> for more info or any question</br>""",
            """ to configure your repository webhook for use this link """,
            """<a href="%swebhook">%swebhook</a>""" % (url_root, url_root)
        ])

def empty_data():
	return "HELLO CLIENT, You send EMPTY request, maybe you test webhook so its OK </br> -Ibra"

@app.route("/", methods=["GET"])
def index():
    return web_info(request)


@app.route("/webhook", methods=["GET", "POST"])
def tracking():
    if request.method == "POST":
        Data = request.get_json()
	try:
		Date= Data["date"]
		UsrName = Data["actor"]["name"]
		RepoNmae = Data["repository"]["slug"]
		FromHash = Data["changes"][0]["fromHash"]
		ToHash = Data["changes"][0]["toHash"]
		for Repo in list_repos :
			
			if RepoNmae==Repo:
				print "Call Run"
				subprocess.call(list_bash[Repo])
		print_log(Date,RepoNmae,UsrName,FromHash,ToHash)
		return "OK"
	except Exception as ex:
		print str(ex);
		return empty_data()
    else:
	 return web_info(request)


if __name__ == "__main__":
    print_hello()
    app.run(host="0.0.0.0", port=port_num, debug=False)
