#coding:utf-8
#Auther：火星小刘
#Email：xtlyk@163.com
#转载请保留出处


from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainsRequest,DescribeDomainRecordsRequest,UpdateDomainRecordRequest
import json,urllib,re


#替换以下参数
ID="xxxxx"
Secret="xxxxx"
RegionId="cn-hangzhou"
DomainName="xxxx.com"
#想要自动修改的主机名和域名类型
HostNameList = ['www','@']
Types = "A"

clt = client.AcsClient(ID,Secret,RegionId)

#获取公网ip
def GetLocalIP():
    IPInfo = urllib.urlopen("https://api.ipify.org/?format=json").read()
    IP = IPInfo['ip']
    return IP

#获取域名列表（暂时无用）
def GetDomainList():
    DomainList = DescribeDomainsRequest.DescribeDomainsRequest()
    DomainList.set_accept_format('json')
    DNSListJson = json.loads(clt.do_action_with_exception(DomainList))
    print DNSListJson

#更新域名ip
def EditDomainRecord(HostName, RecordId, Types, IP):
    UpdateDomainRecord = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    UpdateDomainRecord.set_accept_format('json')
    UpdateDomainRecord.set_RecordId(RecordId)
    UpdateDomainRecord.set_RR(HostName)
    UpdateDomainRecord.set_Type(Types)
    UpdateDomainRecord.set_TTL('600')
    UpdateDomainRecord.set_Value(IP)
    UpdateDomainRecordJson = json.loads(clt.do_action_with_exception(UpdateDomainRecord))
    print UpdateDomainRecordJson

#获取域名信息
def GetAllDomainRecords(DomainName, Types, IP):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(clt.do_action_with_exception(DomainRecords))
    for HostName in HostNameList:
        for x in DomainRecordsJson['DomainRecords']['Record']:
            RR = x['RR']
            Type = x['Type']
            if RR == HostName and Type == Types:
                RecordId = x['RecordId']
                print RecordId
                EditDomainRecord(HostName, RecordId, Types, IP)

IP = GetLocalIP()
GetDomainList()
GetAllDomainRecords(DomainName, Types, IP)


