from bin.PN2025 import DBdir,AAA
from bin.PNssh import CiscoExexCommand
import pandas as pd


#v = cdp_ssh 
#IP = '10.213.1.76'
#USER = AAA[0][0]
#PASSWORD = AAA[0][1]
#enaPassword = AAA[0][1]
file_excell = 'cdp_ssh.xlsx'

def cdpsshHost(IP, USER, PASSWORD, enaPassword):
    dati = []
    try:
        cdp_ssh = str(CiscoExexCommand(IP, USER, PASSWORD, enaPassword,'show cdp neighbors detail | include Device ID|IP address|Interface:'))
#        v = cdp_ssh
#        cdp_ssh = v
        #cdp_ssh = cdp_ssh.replace('\\x08','').split('Interface         :')
        cdp_ssh = cdp_ssh.split('x08\\r\\n')
        cdp_ssh = cdp_ssh[1].split('Device ID: ')
        for riga in cdp_ssh[1:]:
            riga = riga.replace('#','').replace('\\r\\n',',').replace('  IP address: ','').replace('\\r\\nInterface: ','').replace('  Port ID (outgoing port): ','').replace('Interface: ','')
            dati.append(riga.split(','))

        return dati
               
    except:
        return ['NO-cdp_ssh']
    


def cdp_sshList(device,USER,Password, enaPassword):
    m = cdpsshHost(device[1], USER, Password, enaPassword)
    df = pd.DataFrame(m)
    df.insert(0,'device',device[0])
    df.insert(1,'IP',device[1])
    return df


def salvaDataframeExcel(df, nomeFile, DBdir=DBdir):
    try:
        df.to_excel(DBdir+nomeFile, index=False)
    except Exception as error:
        print("An exception occurred:", type(error).__name__, "–", error)

elecoDevices = pd.read_excel(DBdir+'ip.xlsx')



Mlist = pd.DataFrame()
for device in elecoDevices.values:
    if device[8] == 'x':
        print(device)
        Mdevice = cdp_sshList(device, AAA[device[2]][0], AAA[device[2]][1], AAA[device[2]][2])
        Mlist = pd.concat([Mlist, Mdevice], axis = 0)
        salvaDataframeExcel(Mlist, 'tmp_'+file_excell)
            

salvaDataframeExcel(Mlist, file_excell)
Mlist.to_excel(DBdir+file_excell, index=False)