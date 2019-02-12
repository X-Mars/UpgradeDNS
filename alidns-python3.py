#!/usr/bin/python3

#dependence:
'''
pip3 install aliyun-python-sdk-core-v3 (2.5.2)
pip3 install aliyun-python-sdk-alidns (2.0.7)
'''
#aliyunsdk:
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
#else:
from argparse import ArgumentParser
import json

#parser_arguments:
def main():
    parser = ArgumentParser()
    
    parser.add_argument('AccessKeyId')
    parser.add_argument('AccessKeySecret')
    parser.add_argument('Domain')
    parser.add_argument('-q' ,action = 'store_true', help = 'query domain records.')
    parser.add_argument('-u' ,metavar = '<ip>', help = 'update domain ip.')
        
    args = parser.parse_args()
    
    print(run(args.AccessKeyId, args.AccessKeySecret, args.Domain, args.u, args.q))

#module run:    
def run(access_key_id, access_key_secret, domain, update = None, query = None):
    bs = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    
    records = query_record(bs, domain)
    if update:
        if records['@'][0] == update:
            return True
        return update_record(bs, records['@'][3], update)    
    if query:
        return records
    return records['@'][0]
    
def update_record(bs, record_id, ip):
    ud = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    ud.set_accept_format('json')
    ud.set_RecordId(record_id)
    ud.set_RR('@')
    ud.set_Type('A')
    ud.set_TTL('600')
    ud.set_Value(ip)
    
    js = json.loads(bs.do_action_with_exception(ud).decode())
    #print(js)
    if js['RecordId'] == record_id:
        return True
    return False

#query record return a dictionary
def query_record(bs, domain):
    q = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    q.set_accept_format('json')
    q.set_DomainName(domain)
    js = json.loads(bs.do_action_with_exception(q).decode())
    
    ret = {}
    for x in js['DomainRecords']['Record']:
        RR = x['RR']
        Type = x['Type']
        Value = x['Value']
        RecordId = x['RecordId']
        TTL = x['TTL']

        ret[RR] = [Value, Type, TTL, RecordId]
    return ret

if __name__ == '__main__':
    main()
