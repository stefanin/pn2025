from bin.PN2025 import DBdir,AAA
import pandas as pd
from bin.PNssh import CiscoExexCommand
import re


def CiscoIntStatus(IP, USER, PASSWORD, enaPassword):
    try:
        intStatus = str(CiscoExexCommand(IP, USER, PASSWORD, enaPassword,'sh int status'))
        intStatus = intStatus.replace('connected','#connected')
        intStatus = intStatus.replace('notconnect','#notconnect')
        intStatus = intStatus.replace('disabled','#disabled')
        intStatus = intStatus.replace('err-disabled','#err-disabled')   
        intStatus = intStatus.replace('inactive','#inactive')
        intStatus = intStatus.replace('sfpAbsent','#sfpAbsent')
        intStatus = intStatus.replace('suspended','#suspended')
        intStatus = intStatus.split('Duplex  Speed Type')
        intStatus = intStatus[1].replace('\\r','') #rimuove i caratteri di ritorno a capo
        intStatus = intStatus.split('\\n')[:-1]
        elencoPorte = []
        for i in intStatus:
            #print(i)
            r=i
            if r[0:13] != '':

                a = b = []
                try:
                    a = r.split('#')
                    b = a[1].split()
                    a = [a[0][0:13].replace(' ',''),a[0][13:32]]
                    a.extend(b)
                    elencoPorte.append(a)
                except:
                    pass
#        for s in elencoPorte:
#            print(s)
    
        return elencoPorte
               
    except:
        return ['NO-IntStatus']

def IntStatusList(ip,USER,Password, enaPassword):
    m = CiscoIntStatus(ip, USER, Password, enaPassword)
    df = pd.DataFrame(m)
    df.insert(0,'device',ip)
    return df


elecoDevices = pd.read_excel(DBdir+'ip.xlsx')



Mlist = pd.DataFrame()
for x in elecoDevices.values:
    if x[5] == 'x':
        print(x)
        Mdevice = IntStatusList(x[1], AAA[x[2]][0], AAA[x[2]][1], AAA[x[2]][2])
        Mlist = pd.concat([Mlist, Mdevice], axis = 0)


Mlist.to_excel(DBdir+'IntStatus.xlsx', index=False)