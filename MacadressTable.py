from bin.PN2025 import DBdir,AAA
from bin.PNssh import MacAddressTable
import pandas as pd

def MacaddressList(ip,USER,Password, enaPassword):

    m = MacAddressTable(ip, USER, Password, enaPassword)
    df = pd.DataFrame(m)
    df.insert(0,'device',ip)
    df['device']=ip
    return df


elecoDevices = pd.read_excel(DBdir+'ip.xlsx')



Mlist = pd.DataFrame()
for x in elecoDevices.values:
    if x[3] == 'x':
        print(x)
        Mdevice = MacaddressList(x[1], AAA[x[2]][0], AAA[x[2]][1], AAA[x[2]][2])
        Mlist = pd.concat([Mlist, Mdevice], axis = 0)


Mlist.to_excel(DBdir+'MacadressTable20250505.xlsx', index=False)