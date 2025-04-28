from bin.PN2025 import DBdir, AAA
from datetime import datetime
import paramiko
import time
import pandas as pd
import logging
import re


DATAORA = datetime.now().strftime("%Y%m%d%H%M")
CFGDIR = 'cfg\\'
LOGDIR = 'log\\'
logging.basicConfig(filename=LOGDIR+'PNssh.log',filemode='a',format='%(asctime)s;%(levelname)s;%(message)s', level=logging.INFO)

def log(logging,severity,messages):
    if severity=='i':
        print(messages)
        logging.info(messages)
    if severity=='w':
        print(messages)
        logging.warning(messages)



def CiscoshowRUN(IP,USER,Password,enaPassword,PORT=22):
        '''
        IP,USER,Password,enaPassword,PORT=22
        #20230427 via ssh restituisce il risultato del comado sh run o NO-CFG
        '''
        try:
            ssh = paramiko.SSHClient()
            #ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IP , port=PORT, username=USER, password=Password)
            log(logging,'i',IP+"Connected successfully")
            connection = ssh.invoke_shell()
            #print(connection.recv(1000))
            connection.send("enable\n")
            time.sleep(.5)
            connection.send(enaPassword+"\n")
            time.sleep(.5)
            #print(connection.recv(1000))
            connection.send("\n")
            time.sleep(.5)
            #connection.send("conf t\n")
            connection.send("terminal length 0\n")
            #------------------------------login
            connection.send("sh run\n")
            time.sleep(10)
            showrun = connection.recv(65535)
            connection.close()
            ssh.close()
            log(logging,'i',IP+"connection close")
            return showrun
        except:
            log(logging,'w',IP+"connection ERROR")
            return 'NO-CFG'




def CiscoExexCommand(IP,USER,Password,enaPassword,comando,PORT=22):
        '''
        IP,USER,Password,enaPassword,comando,PORT=22
        #20230712 via ssh restituisce il risultato del comado  o NO comando
        '''
        try:
            ssh = paramiko.SSHClient()
            #ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IP , port=PORT, username=USER, password=Password)
            log(logging,'i',IP+"Connected successfully")
            connection = ssh.invoke_shell()
            #print(connection.recv(1000))
            connection.send("enable\n")
            time.sleep(.5)
            connection.send(enaPassword+"\n")
            time.sleep(.5)
            #print(connection.recv(1000))
            connection.send("\n")
            time.sleep(.5)
            #connection.send("conf t\n")
            connection.send("terminal length 0\n")
            #------------------------------login
            connection.send(comando+"\n")
            time.sleep(10)
            execComand = connection.recv(65535)
            connection.close()
            ssh.close()
            log(logging,'i',IP+"connection close")
            return execComand
        except:
            log(logging,'w',IP+"connection ERROR")
            return 'NO-'+comando






def CiscoExexCommand2(IP, auth, comando):
    '''
    #20250311
    auth = [USER,Password,enaPassword]
    comando = STRING
    '''
    return CiscoExexCommand(IP, auth[0],auth[1],auth[2],comando)

def creaFileConfig(showrun, DATAORA, CFGDIR):
        '''
        showrun, DATAORA, CFGDIR
        #20230427 crea file configurazione, nome file = HOSTNAME+DATAORA
        HOSTNAME viene ricavato dalla configurazione
        '''
        for riga in showrun.split('\n'):
            if 'hostname' in riga:
                nomeFile = riga.replace('hostname ','')
                #print(nomeFile)
        #rimuove comadi 
        showrun = showrun.replace('sh run','')
        showrun = showrun.replace('terminal length 0','')
        showrun = showrun.replace('Building configuration...','')
        showrun = showrun.replace(nomeFile+'#','')
        nomeFile = (nomeFile+'_'+DATAORA+'.cfg')

        with open(CFGDIR+nomeFile, 'w') as f:
            f.write(showrun)



def MacAddressTable(IP, USER, Password, enaPassword):
     '''
     IP,USER,Password,enaPassword
     #20250225 restituisce un array con la tabella ARP 

     '''
     try :
        arpTable = str(CiscoExexCommand(IP, USER, Password, enaPassword,'sh mac address-table'))
        arpTable = re.sub(r'\s+', ' ', arpTable)
        arpTable = arpTable.replace('\\r','')
        arpTable = arpTable.split('---- ----------- -------- -----\\n')
        arpTable = arpTable[1]
        arpTable = arpTable.split('Total Mac Addresses for this criterion')[0]
        arpTable = arpTable.split('\\n')
        if arpTable[-1] == '':
            arpTable = arpTable[:-1]

     except:
        arpTable = ['NO-MacAddressTable']
     return arpTable


def CiscovlanTable(IP, USER, PASSWORD, enaPassword):
    #v = vlanTable 
    try:
        vlanTable = str(CiscoExexCommand(IP, USER, PASSWORD, enaPassword,'sh vlan brief'))
        vlanTable = re.sub(r'\s+', ' ', vlanTable)
        vlanTable = vlanTable.replace('\\r','') #rimuove i caratteri di ritorno a capo
        vlanTable = vlanTable.split('-------------------------------\\n')
        vlanTable = vlanTable[1].split('\\n')[:-1]

        aCapo = False
        
        dati = ""
        for riga in vlanTable:
            if "-default" not in riga:#elimina fddi-default
                if "active" in riga:
                    if dati == "":
                        dati = dati + riga
                    else:
                        dati = dati + "#" + riga
                else:
                    dati = dati + "," + riga
        return dati.split("#")
               
    except:
        return ['NO-VLANtable']
    