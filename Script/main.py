from path import Path
import json

logPath = "../Script/Log"
logFilesPath = "../Script/LogUpload"
loginTried = 0
loginSuccess = 0
usedCommands = set()
cowrieCommandInput = []
srcIps = set()
timeConnection = []

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
            if(j % 2 == 0): files.append(tmp[j]);

    return sorted(files)

def getUploadedFiles():

    uploadedFiles = []
    d = Path(logFilesPath)
    
    for i in d.files("*"):
        tmp = []
        if(i.size >= 1024):
            tmp.append(str(i.name))
            tmp.append(i.size)
            uploadedFiles.append(tmp)

    return sorted(uploadedFiles)

def renderLog(current):
    logFiles = getFileLogs()
    global loginSuccess
    global loginTried

    with open(logPath + '/' + current) as myFile:
        data = [
            json.loads(line)
            for line in open(logPath + '/' + current, 'r')
        ]

        for i in data:
            # Contagem de logins com sucesso
            if i["eventid"] == 'cowrie.login.success':
                loginSuccess += 1

            # Contagem de tentativas de login
            if i["eventid"] == 'cowrie.login.success' or i["eventid"] == "cowrie.login.failed":
                loginTried += 1

            # Armazenamento de comandos
            if i["eventid"] == 'cowrie.command.input':
                cowrieCommandInput.append(i)
                usedCommands.add(i["input"])

            # Coleta de IPs 
            if i["eventid"] == 'cowrie.session.connect':
                srcIps.add(i["src_ip"])

            # Armazenamento do tempo de sessão
            if i["eventid"] == "cowrie.log.closed":
                timeConnection.append(i["duration"])

            



def runRenderLog():
    foo = getFileLogs()

    for i in range(0, len(foo)):
        renderLog(foo[i])

if __name__ == '__main__':
    runRenderLog()

    print(f'Número total de ataques: {loginTried}')
    print(f'Número de ataques bem sucedidos: {loginSuccess}')
    
    '''
    print(f'Número total de ataques: {loginTried}')
    print(f'Número de ataques bem sucedidos: {loginSuccess}')
    
    for i in usedCommands:
        print(f"Comando: {i}\n")
        
    for i in srcIps:
        print(i)
    
    for i in timeConnection:
        print(i) 
        '''