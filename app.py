from flask import Flask, jsonify, redirect, render_template, request
import os

# http://localhost:5000/ to view running webpage.

app = Flask(__name__)
path = os.path.abspath(os.path.dirname(__file__))  # Directory of flask application.
listDir = os.listdir(path)  # List contents of current directory.

app.config['UPLOAD_PATH'] = path  # Path for where .log files should be stored.

current_log = 'access_log_20190520-125058'  # Default current log being processed.


@app.route('/upload', methods=['GET', 'POST'])  # Function for uploading and storing file.
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return render_template("error.html", error="Please provide a log file.")
        if file.filename[-4:] != '.log':
            return render_template("error.html", error="Please provide a log file that ends in .log")
        file.save(file.filename)
        return redirect("/")


@app.route('/input', methods=['POST'])  # Function for setting the current .log file the user wants to parse.
def userInput():
    import os
    global current_log
    funcDir = os.listdir(path)
    if not request.form['text']:
        return render_template("error.html", error="No log name provided.")
    if request.form['text'] + '.log' not in funcDir:
        return render_template("error.html", error="Log not found.")
    current_log = request.form['text']
    return redirect("/")


@app.route('/')  # Landing/Home Page with relevant information.
def home():
    document_path = current_log + ".log"
    import os
    funcDir = os.listdir(path)
    newList = []
    for name in funcDir:
        if '.log' in name:
            newList.append(name.strip(".log"))
    return render_template("index.html", List=newList, CurrentLog=document_path)


@app.route('/unique')  # Function for determining unique IPs in given .log file.
def unique():
    document_path = current_log + ".log"
    print(document_path)
    ipList = []
    with open(document_path, "r") as file:
        for line in file.readlines():
            ipList.append(line[0:15].strip("- -"))

    ipList = "Unique IPs: " + str(len(set(ipList)))
    return render_template("unique.html", List=ipList, CurrentLog=document_path)


@app.route('/requests')  # Function for determining amount of requests per IP in a given .log file.
def requests():
    document_path = current_log + ".log"
    ipDict = {}
    ipList = []
    with open(document_path, "r") as file:
        for line in file.readlines():
            ip = line.split()
            ipUnique = ip[0]
            if ipUnique not in ipDict:
                ipDict[ipUnique] = 1
            else:
                ipDict[ipUnique] += 1
    for k, v in ipDict.items():
        ipList.append("IP: " + str(k) + " amount of request(s): " + str(v))

    return render_template("requests.html", List=ipList, CurrentLog=document_path)


@app.route('/codes')  # Function for determining HTTP Status Codes distribution .log file.
def codes():
    document_path = current_log + ".log"
    codeDict = {}
    codeList = []
    with open(document_path, "r") as file:
        for line in file.readlines():
            code = line.split()
            codeUnique = code[8]
            if codeUnique not in codeDict:
                codeDict[codeUnique] = 1
            else:
                codeDict[codeUnique] += 1
    for k, v in codeDict.items():
        codeList.append("Status Code: " + str(k) + " amount of occurrence(s): " + str(v))

    return render_template("codes.html", List=codeList, CurrentLog=document_path)


@app.route('/webpages')  # Function for determining popular webpages given .log file.
def webpages():
    document_path = current_log + ".log"
    pageDict = {}
    pageList = []
    with open(document_path, "r") as file:
        for line in file.readlines():
            page = line.split()
            pageUnique = page[10]
            if pageUnique not in pageDict:
                pageDict[pageUnique] = 1
            else:
                pageDict[pageUnique] += 1
    for k, v in pageDict.items():
        pageList.append("Website: " + str(k) + " amount of occurrence(s): " + str(v))

    return render_template("webpages.html", List=pageList, CurrentLog=document_path)


@app.route('/browsers')  # Function for determining popular browsers in a given .log file.
def browsers():
    document_path = current_log + ".log"
    browserDict = {}
    browserList = []
    with open(document_path, "r") as file:
        for line in file.readlines():
            browser = line.split()
            browserUnique = browser[11].strip(".(X11;")
            browserUnique = browserUnique.strip(".(Windows")
            browserUnique = browserUnique.strip('\"')
            if browserUnique not in browserDict:
                browserDict[browserUnique] = 1
            else:
                browserDict[browserUnique] += 1
    for k, v in browserDict.items():
        browserList.append("Browser: " + str(k) + " amount of occurrence(s): " + str(v))

    return render_template("browsers.html", List=browserList, CurrentLog=document_path)


@app.route('/methods')  # Function for determining method requests distribution in a given .log file.
def os():
    document_path = current_log + ".log"
    methodDict = {}
    methodList = []
    with open(document_path, "r") as file:
        for line in file.readlines():
            method = line.split()
            methodUnique = method[5]
            methodUnique = methodUnique.strip('\"')
            if methodUnique not in methodDict:
                methodDict[methodUnique] = 1
            else:
                methodDict[methodUnique] += 1
    for k, v in methodDict.items():
        methodList.append("Method Request Type: " + str(k) + " amount of occurrence: " + str(v))

    return render_template("methods.html", List=methodList, CurrentLog=document_path)


@app.route('/api')  # Function for landing/homepage for API endpoints.
def api():
    return render_template("api.html")


@app.route('/api/unique')  # Function for "unique ips" API endpoint in a .log file.
def uniqueApi():
    document_path = current_log + ".log"
    print(document_path)
    ipList = []
    with open(document_path, "r") as file:
        for line in file.readlines():
            ipList.append(line[0:15].strip("- -"))

    return jsonify(ipList)


@app.route('/api/requests')  # Function for "finding requests per ip" API endpoint in a .log file.
def requestsApi():
    document_path = current_log + ".log"
    ipDict = {}
    with open(document_path, "r") as file:
        for line in file.readlines():
            ip = line.split()
            ipUnique = ip[0]
            if ipUnique not in ipDict:
                ipDict[ipUnique] = 1
            else:
                ipDict[ipUnique] += 1

    return jsonify(ipDict)


@app.route('/api/codes')  # Function for finding " HTTP status code distribution" API endpoint in a .log file.
def codesApi():
    document_path = current_log + ".log"
    codeDict = {}
    with open(document_path, "r") as file:
        for line in file.readlines():
            code = line.split()
            codeUnique = code[8]
            if codeUnique not in codeDict:
                codeDict[codeUnique] = 1
            else:
                codeDict[codeUnique] += 1

    return jsonify(codeDict)


@app.route('/api/webpages')  # Function for "determining popular webpages" API endpoint in a .log file.
def webpagesApi():
    document_path = current_log + ".log"
    pageDict = {}
    with open(document_path, "r") as file:
        for line in file.readlines():
            page = line.split()
            pageUnique = page[10]
            if pageUnique not in pageDict:
                pageDict[pageUnique] = 1
            else:
                pageDict[pageUnique] += 1

    return jsonify(pageDict)


@app.route('/api/browsers')  # Function for finding "popular browsers" API endpoint in a .log file.
def browsersApi():
    document_path = current_log + ".log"
    browserDict = {}
    with open(document_path, "r") as file:
        for line in file.readlines():
            browser = line.split()
            browserUnique = browser[11].strip(".(X11;")
            browserUnique = browserUnique.strip(".(Windows")
            browserUnique = browserUnique.strip('\"')
            if browserUnique not in browserDict:
                browserDict[browserUnique] = 1
            else:
                browserDict[browserUnique] += 1

    return jsonify(browserDict)


@app.route('/api/methods')  # Function for determining "request method distribution" API endpoint in a .log file.
def osApi():
    document_path = current_log + ".log"
    methodDict = {}
    with open(document_path, "r") as file:
        for line in file.readlines():
            method = line.split()
            methodUnique = method[5]
            methodUnique = methodUnique.strip('\"')
            if methodUnique not in methodDict:
                methodDict[methodUnique] = 1
            else:
                methodDict[methodUnique] += 1

    return jsonify(methodDict)


if __name__ == '__main__':
    app.run()
