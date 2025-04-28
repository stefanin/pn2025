# PN release 2023 S.Cornelli
# pip uninstall pyasn1
# pip install pyasn1==0.4.8
import bin.PN2025
import pandas as pd
from pysnmp.hlapi import *
import os


def rimuoviIPnonInRange(ipList,stringRange):
    '''
    rimuove ip adress nell array ipList che non appartine e a stringRange
    '''
    dVl1=[]
    for ipnet in ipList:
        if stringRange in ipnet:
            print(ipnet)
            dVl1.append(ipnet)
    return dVl1 

def snmpwalk(Comunity,ip,oid):
        '''
        Comunity = snmp comunity; ip = ip host; oid = SNMP OID
        '''
        x=1
        ritorno=[]
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData(Comunity),
                                  UdpTransportTarget((ip, 161)),
                                  ContextData(),
                    ObjectType(ObjectIdentity(oid))):


            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for varBind in varBinds:
                    if str(varBind[0]).find(oid)!=-1:
                                    ritorno.append(varBind[1].prettyPrint())
                    else:
                        return ritorno
                        break

        return ritorno
def snmpwalkBB(Comunity,ip,oid):
        '''
        Comunity = snmp comunity; ip = ip host; oid = SNMP OID
        '''
        x=1
        ritorno=[]
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData(Comunity),
                                  UdpTransportTarget((ip, 161)),
                                  ContextData(),
                    ObjectType(ObjectIdentity(oid))):


            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for varBind in varBinds:
                    if str(varBind[0]).find(oid)!=-1:
                                    ritorno.append(varBind[1])
                    else:
                        return ritorno
                        break

        return ritorno

def snmpwalkB(ip,Comunity,oid):
    '''20220222
    the same snmpwalk but different paramiters position
    '''
    return snmpwalk(Comunity,ip,oid)

def SnmpHostName(ip,comunity):
        '''
        20230206 Hostname query ip= ipadress, comunity= snmp comunity
        '''
        try:
             return snmpwalk(comunity,ip, '1.3.6.1.2.1.1.5')[0]
        except:
             return None

def SnmpCDP(ip,comunity, writeFile=True):
        '''
        20230206 CDP query ip= ipadress, comunity= snmp comunity, writeFile= create a XLSX file, default True
        '''
        HostName=snmpwalk(comunity,ip, '1.3.6.1.2.1.1.5')[0]
        #CDP 
        cdpPeerName=snmpwalk(comunity,ip, '1.3.6.1.4.1.9.9.23.1.2.1.1.6')
        cdpPeerIp=[]
        cdpMaster=[]

        for IPpeers in snmpwalk(comunity, ip,'1.3.6.1.4.1.9.9.23.1.2.1.1.4'):
            IPpeersV=IPpeers.replace('0x','')
            ipPeer=str(int(IPpeersV[0]+IPpeersV[1], base=16))+'.'+str(int(IPpeersV[2]+IPpeersV[3], base=16))+'.'+str(int(IPpeersV[4]+IPpeersV[5], base=16))+'.'+str(int(IPpeersV[6]+IPpeersV[7], base=16))
            cdpPeerIp.append(ipPeer)
            cdpMaster.append(HostName)
        cdpPeerPlatform=snmpwalk(comunity,ip, '1.3.6.1.4.1.9.9.23.1.2.1.1.8')
        cdpPeerPort=snmpwalk(comunity,ip, '1.3.6.1.4.1.9.9.23.1.2.1.1.7')
        #len(cdpPeerName)
        #len(cdpPeerIp)
        #len(cdpPeerPlatform)
        #len(cdpPeerPort)
        cdpTable = pd.DataFrame()
        cdpTable = cdpTable.assign(cdpMaster=cdpMaster,cdpPeerName=cdpPeerName,cdpPeerIp=cdpPeerIp,
                                    cdpPeerPlatform=cdpPeerPlatform,cdpPeerPort=cdpPeerPort)
        if writeFile:                            
            cdpTable.to_excel(percorso_file+HostName+'.CDP.xlsx',index=False)
        return cdpTable


def snmpArpTable(ip,comunity):
    '''
    20250319 ARP table query ip= ipadress, comunity= snmp comunity
    Retrurn ARP table array [[PhysAddress,NetAddress],...]
    '''
    try:

        atPhysAddress = snmpwalk(comunity,ip,'1.3.6.1.2.1.4.22.1.2')
        atNetAddress = snmpwalk(comunity,ip,'1.3.6.1.2.1.4.22.1.3')
        ArpTable = pd.DataFrame()
        ArpTable['PhysAddress'] = atPhysAddress
        ArpTable['PhysAddress'] = ArpTable['PhysAddress'].apply(lambda x: x.replace('0x',''))
        ArpTable['NetAddress'] = atNetAddress
        return ArpTable.values
    except:
        return [['NO-ARPtable']]
    



def snmpGet_vaolre_len(snmp,ip,oid):
     '''
        20250331 restituisce il valore di un OID e la sua lunghezza
        ip = ip address
        snmp = snmp comunity
        oid = mib OID da analizzare
    
     '''
     risultato_snmpQuery = snmpwalkB(ip,snmp,oid)
     return risultato_snmpQuery, len(risultato_snmpQuery)


