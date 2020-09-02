# _*_ coding:utf-8 _*_
import json

import requests
import re, time

from tool.login_token import TokenApp
from common import read_config
from common.mysql_db import PandasMysqlConn

rd = read_config.ReadConfig()


class GetWorkflowId:
    def __init__(self, tenantcode, environment, title, businessType, approvalStatus):
        self.tenantcode = tenantcode
        self.environment = environment
        self.title = title
        self.businessType = businessType
        self.approvalStatus = approvalStatus
        self.url_name_option = self.environment + "_" + self.tenantcode + "_" + "url"
        self.token = TokenApp(self.tenantcode, environment, self.tenantcode, "cz@123456").get_token()[1]

    def get_kc_inspect_id(self):   # 获取批量资质考察，批量现场考察k2 id
        db_name = self.environment + "_" + self.tenantcode + "_" + "evaluate_db_conf"
        # db_name = 'beta_yuexiu_evaluate_db_conf'
        mysql_db = PandasMysqlConn(db_name)
        if self.businessType == "supplier_qualification_inspect" or self.businessType == "supplier_real_inspect":
            sql = 'SELECT id FROM kc_travel WHERE title = "{title}" AND is_deleted = 0 ORDER BY created_on DESC LIMIT 1'.format(title=self.title)        # 获取资质考察，现场考察 k2 id
            print(sql)
        elif self.businessType == "supplier_real_batch_inspect" or self.businessType == "supplier_qualification_batch_inspect":
            sql = 'SELECT id FROM kc_batch_inspect WHERE title = "{title}" AND is_deleted = 0 ORDER BY ' \
                      'created_on DESC LIMIT 1'.format(title=self.title)     # 获取批量资质考察，批量现场考察k2 id
        result = mysql_db.pd_select(sql=sql)
        print(result)
        business_id = result['id'].values[0]
        # print(business_id)
        db_name = self.environment + "_" + self.tenantcode + "_" + "basic_db_conf"
        # db_name = 'beta_yuexiu_basic_db_conf'
        mysql_db = PandasMysqlConn(db_name)
        if business_id:
            sql = 'SELECT id FROM d_basic_workflow_record WHERE business_id = "{id}" AND  title = "{title}" ' \
                  'AND is_deleted = 0'.format(id=business_id, title=self.title)
            result = mysql_db.pd_select(sql=sql)
            k2_id = result['id'].values[0]
            # print(k2_id)
        else:
            sql = 'SELECT id FROM d_basic_workflow_record WHERE title = "{title}" AND is_deleted = 0 ORDER BY ' \
                  'created_on DESC LIMIT 1'.format(title=self.title)
            result = mysql_db.pd_select(sql=sql)
            k2_id = result['id'].values[0]
        return k2_id

    def get_supplier_k2_id(self):   # 获取信息变更，拉黑，锁定k2 id
        db_name = self.environment + "_" + self.tenantcode + "_" + "supplier_db_conf"
        mysql_db = PandasMysqlConn(db_name)
        if self.businessType == "monopoly_approve":
            sql = 'SELECT id FROM d_monopoly WHERE monopoly_name = "{monopoly_name}"'.format(monopoly_name=self.title)
            print(sql)
        elif self.businessType == "extentStore" or self.businessType == "lock" or self.businessType == "blacklist" or \
                self.businessType == "warn":
            sql = 'SELECT id FROM d_supplier WHERE supplier_name = "{supplier_name}"'.format(supplier_name=self.title)
        result = mysql_db.pd_select(sql=sql)
        supplier_id = result['id'].values[0]
        print(supplier_id)
        if self.businessType == "monopoly_approve":
            db_name = self.environment + "_" + self.tenantcode + "_" + "basic_db_conf"
            mysql_db = PandasMysqlConn(db_name)
            sql = 'SELECT id FROM d_basic_workflow_record WHERE business_id ="{business_id}" '.format(
                business_id=supplier_id)
            print(sql)
            result = mysql_db.pd_select(sql=sql)
            id = result['id'].values[0]
        if self.businessType == "extentStore" or self.businessType == "lock" or self.businessType == "blacklist" or \
                self.businessType == "warn":
            db_name = self.environment + "_" + self.tenantcode + "_" + "supplier_db_conf"
            mysql_db = PandasMysqlConn(db_name)
            sql = 'SELECT batch_num FROM d_supplier_temp_dispose_record WHERE supplier_id = "{supplier_id}" AND ' \
                  'is_deleted = 0 AND type = "{type}" ORDER BY created_on DESC LIMIT 1'.format(supplier_id=supplier_id,type=self.businessType)   # 获取信息变更，拉黑，锁定k2 batch_num
            result = mysql_db.pd_select(sql=sql)
            print(result)
            batch_num = result['batch_num'].values[0]
            db_name = self.environment + "_" + self.tenantcode + "_" + "basic_db_conf"
            mysql_db = PandasMysqlConn(db_name)
            sql = 'SELECT id FROM d_basic_workflow_record WHERE business_id ="{business_id}" '.format(business_id=batch_num)
            print(sql)
            result = mysql_db.pd_select(sql=sql)
            id = result['id'].values[0]
        return id

    def change_k2_travel_status(self):
        id = self.get_kc_inspect_id()
        header = {
            "Content-Type": "application/json",
            "token": "{token}".format(token=self.token),
            "o": "{tenantcode}".format(tenantcode=self.tenantcode)
        }
        url_info = rd.read_url_config(self.url_name_option)
        k2_url = url_info.get("k2_url")
        data = {
                "data": {
                    "businessId": "{id}".format(id=id),
                    "businessType": "{businessType}".format(businessType=self.businessType),
                    "approvalStatus": "{approvalStatus}".format(approvalStatus=self.approvalStatus)
                },
                "timestamp": "{timestamp}".format(timestamp=time.localtime(time.time())),
                "token": "{token}".format(token=self.token),
                "o": "{tenantcode}".format(tenantcode=self.tenantcode)
        }
        req = requests.post(url=k2_url, data=json.dumps(data), headers=header, verify=False)
        print(req.json())
        if req.json()['result'] is True:
            flag = 'success'
        else:
            flag = 'fail'
        result = [flag, req.json()]
        print(result)
        return result

    def change_supplier_status(self):
        id = self.get_supplier_k2_id()
        header = {
            "Content-Type": "application/json",
            "token": "{token}".format(token=self.token),
            "o": "{tenantcode}".format(tenantcode=self.tenantcode)
        }
        url_info = rd.read_url_config(self.url_name_option)
        k2_url = url_info.get("k2_url")
        if self.businessType == 'monopoly_approve':
            data = {
                "data": {
                    "businessId": "{id}".format(id=id),
                    "businessType": "{businessType}".format(businessType=self.businessType),
                    "approvalStatus": "{approvalStatus}".format(approvalStatus=self.approvalStatus)
                },
                "timestamp": "{timestamp}".format(timestamp=time.localtime(time.time())),
                "token": "{token}".format(token=self.token),
                "o": "{tenantcode}".format(tenantcode=self.tenantcode)
            }
        else:
            data = {
                "data": {
                    "businessId": "{businessId}".format(businessId=id),
                    "approvalStatus": "{approvalStatus}".format(approvalStatus=self.approvalStatus),
                }
            }
        req = requests.post(url=k2_url, data=json.dumps(data), headers=header, verify=False)
        print(req.json())
        if req.json()['result'] is True:
            flag = 'success'
        else:
            flag = 'fail'
        result = [flag, req.json()]
        print(result)
        return result


if __name__ == "__main__":
    s = GetWorkflowId("", "", "", "blacklist", "locking")
    s.change_supplier_status()
