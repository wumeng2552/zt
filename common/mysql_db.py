import pymysql
import pymysql.cursors
from common import read_config
import pandas as pd

rd = read_config.ReadConfig( )


# ==========================封装mysql基本操作================================================


class PandasMysqlConn( object ):

    def __init__( self, mysql_db_name ):
        self.mysql_db_name = mysql_db_name
        db_info = rd.read_db_config( mysql_db_name )
        host = db_info.get( 'host' )
        port = db_info.get( 'port' )
        user = db_info.get( 'user' )
        password = db_info.get( 'password' )
        db_name = db_info.get( 'db_name' )
        int_port = int( port )
        self.config = {
            'host': host,
            'port': int_port,  # 这里port需要为int类型
            'user': user,
            'password': password,
            'db': db_name,
            'charset': 'utf8mb4',
        }
        try:
            self.con = pymysql.connect( **self.config )
            self.cur = self.con.cursor( cursor=pymysql.cursors.DictCursor )
        except pymysql.OperationalError as e:
            print( "连接数据库失败,Mysql Error %d:%s" % (e.args[ 0 ], e.args[ 1 ]) )


    # pandas.read_sql读取数据库返回的数据的类型是DataFrame
    def pd_select(self, sql):
        pd_result = pd.read_sql(sql=sql, con=self.con)
        self.con.close()
        return pd_result



    def pd_sql_query(self, sql):
        pd_query_result = pd.read_sql_query( sql=sql, con=self.con)
        self.con.close()
        return pd_query_result

    def pd_sql_table(self, table_name):
        pd_table_result = pd.read_sql_table( table_name=table_name, con=self.con)
        self.con.close()
        return pd_table_result

    def execute_sql(self, sql):
        try:
            self.cur.execute(sql)
            self.con.commit()
            self.con.close()
            return True
        except:
            self.con.rollback()
            self.con.close()
            return False


if __name__ == '__main__':
    sql = 'SELECT * FROM evaluate.kc_batch_inspect ORDER BY created_on DESC LIMIT 50'
    P = PandasMysqlConn( "beta_yuexiu_evaluate_db_conf" )
    P.execute_sql(sql)
