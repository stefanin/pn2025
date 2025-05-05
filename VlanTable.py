from bin.PN2025 import DBdir,AAA
from bin.PNssh import CiscovlanTable
import pandas as pd

def vlanTableList(ip,USER,Password, enaPassword):
    m = CiscovlanTable(ip, USER, Password, enaPassword)
    df = pd.DataFrame(m)
    df.insert(0,'device',ip)
    return df


elecoDevices = pd.read_excel(DBdir+'ip.xlsx')



Mlist = pd.DataFrame()
for x in elecoDevices.values:
    if x[4] == 'x':
        print(x)
        Mdevice = vlanTableList(x[1], AAA[x[2]][0], AAA[x[2]][1], AAA[x[2]][2])
        Mlist = pd.concat([Mlist, Mdevice], axis = 0)


Mlist.to_excel(DBdir+'VlanTable.xlsx', index=False)