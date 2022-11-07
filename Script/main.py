from path import Path
import json
import pylab
import pandas
import requests
import time

# We need create 2 dirs inside /Script, they are "Log" and "LogUpload"
logPath = "../Script/Log"
logFilesPath = "../Script/LogUpload"
csvFilePath = "../Script/"
loginTried = 0
loginSuccess = 0
usedCommands = set()
cowrieCommandInput = []
srcIps = set()
timeConnection = []
country = set()

def getFileLogs():
    files = []
    d = Path(logPath)

    for i in d.files("*.json*"):
        tmp = []

        if i.name == "cowrie.json":
            tmp.append(i.name)
            files.append(tmp)
            continue

        tmp.append(str(i.name))
        splitString = i.name.split(".")
        tmp.append(splitString[2].replace("_", "-"))

        for j in range(0, len(tmp)):
            if(j % 2 == 0): files.append(tmp[j])

    return sorted(files)

def getDownloadedFiles():
    DownloadedFiles = []
    d = Path(logFilesPath)
    files = []
    
    for i in d.files("*"):
        tmp = []
        if(i.size >= 1024):
            tmp.append(str(i.name))
            tmp.append(i.size)
            DownloadedFiles.append(tmp)

    for i in DownloadedFiles:
        for j in range(len(i)):
            if j == 0: files.append(i[j])

    return sorted(files)

def renderLog(current):
    global loginSuccess
    global loginTried

    with open(logPath + "/" + current) as myFile:
        data = [
            json.loads(line)
            for line in open(logPath + "/" + current, "r")
        ]

        for i in data:
            # Count success login
            if i["eventid"] == "cowrie.login.success":
                loginSuccess += 1

            # Count tried login
            if i["eventid"] == "cowrie.login.failed":
                loginTried += 1

            # Command storage
            if i["eventid"] == "cowrie.command.input":
                cowrieCommandInput.append(i)
                usedCommands.add(i["input"])

            # IP storage
            if i["eventid"] == "cowrie.session.connect":
                srcIps.add(i["src_ip"])

            # Session time storage
            if i["eventid"] == "cowrie.log.closed":
                timeConnection.append(i["duration"])

def runRenderLog():
    foo = getFileLogs()

    for i in range(0, len(foo)):
        renderLog(foo[i])

def dataProcess():

    # Pie chart tried x success
    pylab.pie([loginTried, loginSuccess])
    pylab.title("Gráfico tentivas x sucessos")
    pylab.xlabel(f"Tentativas: {loginTried}\nSucesso: {loginSuccess}")
    pylab.savefig("tentativasucesso.png")

    # Export all IPs to CSV
    dfIps = pandas.DataFrame(srcIps, columns=["IPs: "])
    dfIps.to_csv("ips.csv")

    # Export all duration section to CSV
    dfTimeSession = pandas.DataFrame(timeConnection, columns=["Duração de sessão: "])
    dfTimeSession.to_csv("timeSession.csv")

    # Export all used commands to CSV
    dfCommands = pandas.DataFrame(usedCommands, columns=["Comandos: "])
    dfCommands.to_csv("commands")

    # Export countrys to CSV
    dfCountry = pandas.DataFrame(country, columns=["Países: "])
    dfCountry.to_csv("country.csv")

def ipInfoRender():
    tmp = []
    count = 0

    for i in srcIps:
        count += 1
        r = requests.get(f"http://ip-api.com/json/{i}")
        tmp.append(r.json())
        time.sleep(1.1)
        print(count)

    for i in tmp:
        country.add(i["country"])

    print(country)

if __name__ == '__main__':
    runRenderLog()
    ipInfoRender()
    dataProcess()