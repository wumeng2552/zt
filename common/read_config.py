# -*- coding: utf-8 -*-
import os
import pandas as pd
import configparser
import datetime
import codecs

pd.set_option('display.width', 5000)  # 设置打印宽度
proDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(proDir, "config")
test_data_path = os.path.join(proDir, "test_data")


class ReadConfig:
    '''
    创建ConfigParser对象，读取config路径的配置文件
    '''

    def __init__(self):
        # self.path=config_path+file_name
        # self.conf = configparser.ConfigParser()
        self.conf = configparser.RawConfigParser()   # ini的内容中包含了%号这种特殊符号
        # self.conf.read(self.path,encoding='utf-8')
        # self.conf.read(self.path)

    def read_db_config( self, db_name_option ):
        db_config_path = config_path + "\\db_config.ini"
        # print("当前读取文件所在路径：",db_config_path)
        self.conf.read( db_config_path, encoding = 'utf-8' )
        try:
            sections_value = { i[ 0 ]: i[ 1 ] for i in self.conf.items( db_name_option ) }
            # print("当前{0}数据库信息：{1}".format(db_name_option,sections_value))
        except Exception as  e:
            # print("当前读取{0}数据库信息报错".format(db_name_option))
            sections_value = None
        return sections_value

    def read_server_config(self, server_name_option):
        server_config_path = config_path + "\\server_config.ini"
        # print("当前读取文件所在路径：",db_config_path)
        self.conf.read(server_config_path, encoding='utf-8')
        try:
            sections_value = {i[0]: i[1] for i in self.conf.items(server_name_option)}
            # print("当前{0}数据库信息：{1}".format(db_name_option,sections_value))
        except Exception as  e:
            # print("当前读取{0}数据库信息报错".format(db_name_option))
            sections_value = None
            # print(e)
        return sections_value

    def read_redis_config(self, redis_name_option):
        redis_config_path = config_path + "\\redis_config.ini"
        # print("当前读取文件所在路径：",db_config_path)
        self.conf.read(redis_config_path, encoding='utf-8')
        try:
            sections_value = {i[0]: i[1] for i in self.conf.items(redis_name_option)}
            # print("当前{0}数据库信息：{1}".format(db_name_option,sections_value))
        except Exception as  e:
            # print("当前读取{0}数据库信息报错".format(db_name_option))
            sections_value = None
            # print(e)
        return sections_value

    def read_common_config(self, mould_name, option):
        common_path = config_path + "\\common_config.ini"
        # print("当前读取文件所在路径：",common_path)
        self.conf.read(common_path)
        try:
            value = self.conf.get(mould_name, option)
            # print("当前读取common配置信息：",value)
        except Exception as e:
            value = None
            # print("读取common_config文件报错：",e)
        return value

    def read_url(self, moudl_name, option):
        '''
        :param moudl_name:
        :param option: test：匹配测试环境地址；online：匹配线上环境地址；uat：匹配UAT环境地址
        :return: 读取到则返回url地址，未读取到则返回None
        '''
        url_path = config_path + "\\url.ini"
        # print("当前读取文件所在路径：",url_path)
        self.conf.read(url_path, encoding='utf-8')
        option_name = moudl_name + '_' + option
        try:
            url = self.conf.get(moudl_name, option_name)
            # print("当前读取url地址：",url)
        except Exception as e:
            url = None
            print("读取url地址报错：", e)
        return url

    def read_excel(self, excel_name, sheetname):
        excel_path = test_data_path + excel_name
        df = pd.read_excel(excel_path, sheetname=sheetname)

        return df

    def write_file(self, file_name, txt_str):
        date1 = datetime.date.today()
        file_name = file_name + str(date1) + '.txt'
        file_path = os.path.join(proDir, "result\\" + file_name)
        f = codecs.open(file_path, 'a', 'utf8')
        f.write(str(txt_str))
        f.close()

    def read_user_verify_config(self, user_option):
        verify_config_path = config_path + "\\user_verify.ini"
        self.conf.read(verify_config_path, encoding='utf-8')
        try:
            sections_value = {i[0]: i[1] for i in self.conf.items(user_option)}
        except Exception as  e:
            sections_value = None
        return sections_value


    def read_url_config( self, url_name_option ):
        db_config_path = config_path + "\\url_config.ini"
        # print("当前读取文件所在路径：",db_config_path)
        self.conf.read( db_config_path, encoding = 'utf-8' )
        try:
            sections_value = { i[ 0 ]: i[ 1 ] for i in self.conf.items( url_name_option ) }
            # print("当前{0}数据库信息：{1}".format(db_name_option,sections_value))
        except Exception as  e:
            # print("当前读取{0}数据库信息报错".format(db_name_option))
            sections_value = None
        return sections_value


if __name__ == "__main__":
    r = ReadConfig()
    a = r.read_user_verify_config('')
    print(a)
