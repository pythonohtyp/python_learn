# -*- coding:utf-8 -*-
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import AuthorizeSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import RevokeSecurityGroupRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import ModifySecurityIpsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceIPArrayListRequest
import aliyunsdkdds.request.v20151201.ModifySecurityIpsRequest
import re


class alis:
    def __init__(self,accesskey,accesssecret,regionid):
        self.accesskey = accesskey
        self.accesssecret = accesssecret
        self.regionid = regionid
    def clt(self):
        clt = AcsClient(self.accesskey,self.accesssecret,self.regionid)
        return clt
    def authorizeSecurityGroupRequest(self,SecurityGroupID,IpProtocol,PortRange,SourceCidrIp,Priority,Description):
        '''授权安全组内规则'''
        request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        request.set_SecurityGroupId(SecurityGroupID)
        request.add_query_param('RegionId','cn-shenzhen')   #需改为华东1（cn-hangzhou
        request.set_IpProtocol(IpProtocol)
        request.set_PortRange(PortRange)
        request.set_SourceCidrIp(SourceCidrIp)
        request.set_Priority(Priority)
        request.set_Description(Description)
        request.set_accept_format('json')
        return request
    def revokeSecurityGroupRequest(self,SecurityGroupID,IpProtocol,PortRange,SourceCidrIp,Priority):
        '''撤销安全组内规则'''
        request = RevokeSecurityGroupRequest.RevokeSecurityGroupRequest()
        request.set_SecurityGroupId(SecurityGroupID)
        request.add_query_param('RegionId', 'cn-shenzhen')  #需改为华东1（cn-hangzhou
        request.set_IpProtocol(IpProtocol)
        request.set_PortRange(PortRange)
        request.set_SourceCidrIp(SourceCidrIp)
        request.set_Priority(Priority)
        request.set_accept_format('json')
        return request
    def describeDBInstances(self):
        '''Mysql数据库实例列表'''
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_accept_format('json')
        request.add_query_param('RegionId','cn-shenzhen')
        return request
    def modifySecurityIps(self,DBInstanceId,SecurityIps,DBInstanceIPArrayName):
        '''Mysql数据库白名单修改'''
        request = ModifySecurityIpsRequest.ModifySecurityIpsRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_SecurityIps(SecurityIps)
        request.set_DBInstanceIPArrayName(DBInstanceIPArrayName)
        return request
    def modifySecurityIps_dds(self,DBInstanceId,SecurityIps,ModifyMode):
        '''MongoDB数据库白名单修改'''
        request = aliyunsdkdds.request.v20151201.ModifySecurityIpsRequest.ModifySecurityIpsRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_SecurityIps(SecurityIps)
        request.set_ModifyMode(ModifyMode)
        return request
    def describeDBInstanceIPArrayListRequest(self,DBInstanceId):
        '''查看RDS实例IP白名单'''
        request = DescribeDBInstanceIPArrayListRequest.DescribeDBInstanceIPArrayListRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(DBInstanceId)
        return request
if __name__ == '__main__':
    ali = alis('LTAIZhlYZ8QUhvMd','VbBW1j1IxE8PmPWvUEOJYgv6jtXhBo','cn-shenzhen')   #需改为华东1（cn-hangzhou
    clt = ali.clt()
    tuple_port = ['80/80','9876/9876','9877/9877','3717/3717','22024/22024','8888/8888','52001/52005','51000/51005',
                  '22024/22024','50000/50010','50015/50095','843/843','3389/3389','4018/4018']
    tuple_priority = ['2','50','51','52','80','1','2','50','80','1','6','7','50','99']
    tuple_description = ['fmy-website-online','fmy-website-admin','smart-sso-srever','mongodb-agent','linux-ssh','fmy-game-service(n0)',
                         'fmy-game-service(n1-n5)','fmy-game-admin(n1-n5)','linux-ssh','-','多服端口','flash跨域服务','windows远程桌面','-']
    try:    #ECS
        for i in range(14):
            if i < 5:
                ali_add_rules_1 = ali.authorizeSecurityGroupRequest('sg-23v92s1b5', 'tcp', tuple_port[i], '113.215.177.111', tuple_priority[i],tuple_description[i])
                ali_rvk_rules_1 = ali.revokeSecurityGroupRequest('sg-23v92s1b5','tcp',tuple_port[i], '113.215.177.102', tuple_priority[i])
                '''SG_AS_OfficialWebsite'''
                print clt.do_action_with_exception(ali_add_rules_1)
                print clt.do_action_with_exception(ali_rvk_rules_1)
            elif 8 >= i >= 5:
                ali_add_rules_2 = ali.authorizeSecurityGroupRequest('sg-23r562xqj', 'tcp', tuple_port[i], '113.215.177.111', tuple_priority[i],tuple_description[i])
                ali_rvk_rules_2 = ali.revokeSecurityGroupRequest('sg-23r562xqj','tcp',tuple_port[i], '113.215.177.102', tuple_priority[i])
                '''SG_AS_GameJavaWeb'''
                print clt.do_action_with_exception(ali_add_rules_2)
                print clt.do_action_with_exception(ali_rvk_rules_2)
            else:
                ali_add_rules_3 = ali.authorizeSecurityGroupRequest('sg-23ltyskj3', 'tcp', tuple_port[i], '113.215.177.111', tuple_priority[i],tuple_description[i])
                ali_rvk_rules_3 = ali.revokeSecurityGroupRequest('sg-23ltyskj3','tcp',tuple_port[i], '113.215.177.102', tuple_priority[i])
                '''SG_AS_GameServer'''
                print clt.do_action_with_exception(ali_add_rules_3)
                print clt.do_action_with_exception(ali_rvk_rules_3)
    except Exception, e:
        print Exception, ":", e
    try:    #RDS
        dbinstance = ali.describeDBInstances()
        ask = clt.do_action_with_exception(dbinstance)
        b = re.findall(r'"DBInstanceId":"(.*?)","ZoneId"',ask)
        for i in b:
            ali_rds_IP = ali.modifySecurityIps(i,'113.215.177.102','company_public_ip')
            print clt.do_action_with_exception(ali_rds_IP)
    except Exception, e:
        print Exception, ":", e
    try:    #DDS
        ali_dds_add_IP = ali.modifySecurityIps_dds('dds-bp1d76757b10d784','113.215.177.102','Add')
        '''DDS添加新IP白名单'''
        ali_dds_del_IP = ali.modifySecurityIps_dds('dds-bp1d76757b10d784','113.215.177.149','Delete')
        '''DDS删除旧IP白名单'''
        print clt.do_action_with_exception(ali_dds_add_IP)
        print clt.do_action_with_exception(ali_dds_del_IP)

    except Exception, e:
        print Exception, ":", e

