import os
import random
import subprocess

regions = ['us-west2', 'southamerica-east1', 'europe-west3', 'me-west1', 'asia-east2']

def configureSourceIP():
    arg = str(input("Write your IP: "))
    os.system(f'''
                gcloud compute firewall-rules update allow-ssh-v4 \
                --source-ranges {arg} \
                --rules=tcp:2222''')
    

def getInstances():
    getInstances =  subprocess.Popen("gcloud compute instances list | awk '{print $1}' | grep -v 'NAME'", shell=True, stdout=subprocess.PIPE).stdout
    instances = getInstances.read().decode().split('\n')
    instances.pop()

    return instances

def modifyHoneypots(arg):
    instances = getInstances()
    
    for i in range(0, len(instances)):
        os.system(f'gcloud compute ssh cowrie@{instances[i]} --ssh-flag="-p 2222" --command="cowrie/bin/cowrie {arg}"')

def statusHoneypots():
    modifyHoneypots('status')

def stopHoneypots():
    modifyHoneypots('stop')

def restartHoneypots():
    modifyHoneypots('restart')

def startHoneypots():
    modifyHoneypots('start')

def configureUniqueHoneypot():
    arg = str(input('Name of instance: '))

    commandPassAuth = "sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config"
    commandPrograms = "wget git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind virtualenv python3-venv"
    commandPython = "cd cowrie && python3 -m venv cowrie-env && source cowrie-env/bin/activate && python3 -m pip install --upgrade pip && python3 -m pip install --upgrade -r requirements.txt"
    commandIPTablesSSHA = "sudo iptables -t nat -A PREROUTING -p tcp --dport 2222 -j REDIRECT --to-port 22 && sudo ip6tables -t nat -A PREROUTING -p tcp --dport 2222 -j REDIRECT --to-port 22"
    commandIPTablesSSHB = "sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222 && sudo ip6tables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222"
    commandIPTablesTELNETA = "sudo iptables -t nat -A PREROUTING -p tcp --dport 2223 -j REDIRECT --to-port 23 && sudo ip6tables -t nat -A PREROUTING -p tcp --dport 2223 -j REDIRECT --to-port 23"
    commandIPTablesTELNETB = "sudo iptables -t nat -A PREROUTING -p tcp --dport 23 -j REDIRECT --to-port 2223 && sudo ip6tables -t nat -A PREROUTING -p tcp --dport 23 -j REDIRECT --to-port 2223"
    commandConfigCFG = "wget https://raw.githubusercontent.com/r1beirin/IC-Honeypots/main/Script/script2/cowrie.cfg && mv cowrie.cfg cowrie/etc/"

    os.system(f'gcloud compute ssh {arg} --command="sudo adduser honey"')
    os.system(f'gcloud compute ssh {arg} --command="sudo usermod -aG sudo honey"')
    os.system(f'gcloud compute ssh {arg} --command="sudo mv /usr/bin/mandb /usr/bin/mandb-OFF"')
    os.system(f'gcloud compute ssh {arg} --command="sudo cp -p /bin/true /usr/bin/mandb "')
    os.system(f'gcloud compute ssh {arg} --command="sudo rm -r /var/cache/man"')
    os.system(f'gcloud compute ssh {arg} --command="{commandPassAuth}"')
    os.system(f'gcloud compute ssh {arg} --command="sudo systemctl restart ssh"')
    os.system(f'gcloud compute ssh {arg} --command="sudo apt update"')
    os.system(f'gcloud compute ssh {arg} --command="sudo apt install {commandPrograms} -y"')
    os.system(f'gcloud compute ssh {arg} --command="sudo adduser --disabled-password cowrie"')
    os.system(f'gcloud compute ssh cowrie@{arg} --command="git clone http://github.com/cowrie/cowrie"')
    os.system(f'gcloud compute ssh cowrie@{arg} --command="{commandPython}"')
    os.system(f'gcloud compute ssh cowrie@{arg} --command="{commandConfigCFG}"')
    os.system(f'gcloud compute ssh {arg} --command="{commandIPTablesSSHA}"')
    os.system(f'gcloud compute ssh {arg} --ssh-flag="-p 2222" --command="{commandIPTablesSSHB}"')
    os.system(f'gcloud compute ssh {arg} --ssh-flag="-p 2222" --command="{commandIPTablesTELNETA}"')
    os.system(f'gcloud compute ssh {arg} --ssh-flag="-p 2222" --command="{commandIPTablesTELNETB}"')
    

def configureHoneypots():
    instances = getInstances()

    commandPassAuth = "sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config"
    commandPrograms = "wget git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind virtualenv python3-venv"
    commandPython = "cd cowrie && python3 -m venv cowrie-env && source cowrie-env/bin/activate && python3 -m pip install --upgrade pip && python3 -m pip install --upgrade -r requirements.txt"
    commandIPTablesSSHA = "sudo iptables -t nat -A PREROUTING -p tcp --dport 2222 -j REDIRECT --to-port 22 && sudo ip6tables -t nat -A PREROUTING -p tcp --dport 2222 -j REDIRECT --to-port 22"
    commandIPTablesSSHB = "sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222 && sudo ip6tables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222"
    commandIPTablesTELNETA = "sudo iptables -t nat -A PREROUTING -p tcp --dport 2223 -j REDIRECT --to-port 23 && sudo ip6tables -t nat -A PREROUTING -p tcp --dport 2223 -j REDIRECT --to-port 23"
    commandIPTablesTELNETB = "sudo iptables -t nat -A PREROUTING -p tcp --dport 23 -j REDIRECT --to-port 2223 && sudo ip6tables -t nat -A PREROUTING -p tcp --dport 23 -j REDIRECT --to-port 2223"
    commandConfigCFG = "wget https://raw.githubusercontent.com/r1beirin/IC-Honeypots/main/Script/script2/cowrie.cfg && mv cowrie.cfg cowrie/etc/"

    for i in range(0, len(instances)):
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo adduser honey"')
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo usermod -aG sudo honey"')
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo mv /usr/bin/mandb /usr/bin/mandb-OFF"')
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo cp -p /bin/true /usr/bin/mandb "')
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo rm -r /var/cache/man"')
        os.system(f'gcloud compute ssh {instances[i]} --command="{commandPassAuth}"')
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo systemctl restart ssh"')
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo apt update"')
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo apt install {commandPrograms} -y"')
        os.system(f'gcloud compute ssh {instances[i]} --command="sudo adduser --disabled-password cowrie"')
        os.system(f'gcloud compute ssh cowrie@{instances[i]} --command="git clone http://github.com/cowrie/cowrie"')
        os.system(f'gcloud compute ssh cowrie@{instances[i]} --command="{commandPython}"')
        os.system(f'gcloud compute ssh cowrie@{instances[i]} --command="{commandConfigCFG}"')
        os.system(f'gcloud compute ssh {instances[i]} --command="{commandIPTablesSSHA}"')
        os.system(f'gcloud compute ssh {instances[i]} --ssh-flag="-p 2222" --command="{commandIPTablesSSHB}"')
        os.system(f'gcloud compute ssh {instances[i]} --ssh-flag="-p 2222" --command="{commandIPTablesTELNETA}"')
        os.system(f'gcloud compute ssh {instances[i]} --ssh-flag="-p 2222" --command="{commandIPTablesTELNETB}"')

def modifyInstances(arg):
    instances = getInstances()

    for i in instances:
        os.system(f'gcloud compute instances {arg} {i}')

def stopInstances():
    modifyInstances('stop')

def startInstances():
    modifyInstances('start')

def createInstances():
    count = 1
    region = 0

    for i in range(0, 15):
        if count == 4:
            count = 1
            region += 1
    
        os.system(f'''
                  gcloud compute instances create {regions[region]}-instance-0{count} \
                  --zone={regions[region]}-a \
                  --machine-type=e2-micro \
                  --image=debian-11-bullseye-v20230912 \
                  --image-project=debian-cloud \
                  --boot-disk-size=20 \
                  --subnet=subnet-{regions[region]}-{count} \
                  --stack-type=IPV4_IPV6
                  ''')
        
        count += 1

def createSubnets():
    octates = []
    while len(octates) < 15:
        octate = random.randint(0, 254)
        if octate not in octates:
            octates.append(octate)
    
    count = 1
    region = 0

    for i in range(0 , 15):
        if count == 4:
            count = 1
            region += 1

        os.system(f'''
                  gcloud compute networks subnets create subnet-{regions[region]}-{count} \
                  --network=vpc-honeypot \
                  --range=10.{octates[i]}.{octates[i]}.0/24 \
                  --stack-type=IPV4_IPV6 \
                  --ipv6-access-type=external \
                  --region={regions[region]}
                  ''')
        
        count += 1


def createRulesNetwork():
    os.system('''
              gcloud compute firewall-rules create allow-ssh-v4 \
              --network vpc-honeypot \
              --priority 1000 \
              --direction ingress \
              --action allow \
              --rules=tcp:22,tcp:2222 \
              --source-ranges 0.0.0.0/0''')
    
    os.system('''
              gcloud compute firewall-rules create allow-ssh-telnet-icmp-v6 \
              --network vpc-honeypot \
              --priority 1000 \
              --direction ingress \
              --action allow \
              --rules=tcp:22,tcp:23,tcp:2222,tcp:2223,58 \
              --source-ranges 0::/0''')

def createNetwork():
    os.system('gcloud compute networks create vpc-honeypot --bgp-routing-mode=regional --subnet-mode=custom')
    createRulesNetwork()
    createSubnets()

def createInitConfig():
    os.system('gcloud auth login')
    os.system('\ngcloud projects list')
    projectID = str(input("Write your PROJECT ID: "))
    os.system(f'gcloud config set project {projectID}')

def instances():
    print('\n1 - Start instances\n2 - Stop instances')
    option = int(input('Choose a option: '))

    if option == 1: startInstances()
    elif option == 2: stopInstances()

def honeypot():
    print('\n1 - Start honeypots\n2 - Stop honeypots\n3 - Restart honeypots\n4 - Status honeypots')
    option = int(input('Choose a option: '))

    if option == 1: startHoneypots()
    elif option == 2: stopHoneypots()
    elif option == 3: restartHoneypots()
    elif option == 4: statusHoneypots()

def run():
    print('\n1 - Configure initial option\n2 - Create network\n3 - Create instances\n4 - Configure Honeypots\n5 - Instances\n6 - Honeypots\n7 - Configure your IP to connect SSH\n8 - Configure unique honeypot')
    
    option = int(input('Choose a option: '))

    if option == 1: createInitConfig()
    elif option == 2: createNetwork()
    elif option == 3: createInstances()
    elif option == 4: configureHoneypots()
    elif option == 5: instances()
    elif option == 6: honeypot()
    elif option == 7: configureSourceIP()
    elif option == 8: configureUniqueHoneypot()

if __name__ == "__main__":
    run()
