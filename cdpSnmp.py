import datetime
from  bin.PNsnmp2025 import SnmpCDP, rimuoviIPnonInRange
import numpy as np
import pandas as pd
from bin.PN2025 import DBdir,AAA


def removeDevice(cdpMaster):
    '''
    rimuove i device non necessari  
    '''
    device_remove = [
        'cisco C9130AXE-E',
        'cisco C9136I-E',
        'cisco C9124AXD-E',
        'Cisco IP Phone 6901',
        ]
    return cdpMaster[[x not in device_remove for x in cdpMaster['cdpPeerPlatform']]]







def SnmpCDPMasterScan(cdpMaster, ipList, SNMPComunity):
    cdpAll=cdpMaster
    for devices in ipList:
        try:
            print(devices)
            cdpDevice=SnmpCDP(devices,SNMPComunity)
            cdpAll = pd.concat([cdpAll, cdpDevice])
        except:
            print(devices,' errore!!')
    return cdpAll


def CiscoSnmpCDP2(DeviceCore, SNMPComunity, FiltroIP=''):
    '''
    DeviceCore = ip del device di riferimento 
    SNMPComunity = comunity snmp 
    FiltroIP = radice della network es. 172.17.1.
    #2025032 array che rimuove i device non necessari

    '''

    print('-------------------- CDP Master -------------------------')
    cdpMaster=SnmpCDP(DeviceCore,SNMPComunity)
    #rimuove le righe nell array

    cdpMaster = removeDevice(cdpMaster)    #primo elenco ip
    prima=cdpMaster['cdpPeerIp'].unique()
    #scan primo elenco ip
    print('-------------------- CDP 1 -------------------------')
    cdpAll=SnmpCDPMasterScan(cdpMaster, prima, SNMPComunity)
    #cdpAll.to_excel('cdpAll1.xlsx')
    conta=2
    while True:
        print('-------------------- CDP ',conta,' -------------------------')
        dopo = removeDevice(cdpAll) #rimuove i device non necessari
        dopo = cdpAll['cdpPeerIp'].unique()
        #rimuovi master
        dopo=np.array(dopo)
        dopo=dopo[dopo !=DeviceCore]
        differenza=np.setdiff1d(dopo,np.array(prima))
        if len(differenza) == 0:
            print('-------------------- END CDP Scanning -------------------------')
            break
        else:
            cdpAll=SnmpCDPMasterScan(cdpAll,differenza, SNMPComunity)
            prima=dopo
            conta+=1

    return cdpAll



elecoDevices = pd.read_excel(DBdir+'ip.xlsx')



Mlist = pd.DataFrame()
for x in elecoDevices.values:
    if x[7] == 'x':
        print(x)
        Mdevice = CiscoSnmpCDP2(x[1], x[6], '')
        Mlist = pd.concat([Mlist, Mdevice], axis = 0)


Mlist.to_excel(DBdir+'cdpSnmp.xlsx', index=False)