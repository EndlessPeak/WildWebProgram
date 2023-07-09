import pymysql
import json

def get_db_config():
    with open('./static/config.json','r') as file:
        # Warning: json file must enclose name in double quotes
        config = json.load(file)
    return config
    
# Access the data base handle
db_config = get_db_config()

def connect_sql():
    db_handle = pymysql.connect(
        host = db_config['host'],
        port = db_config['port'],
        user = db_config['user'],
        password = db_config['password'],
        db = db_config['database'],
        charset = 'utf8')
    return db_handle

def check_user_login(username,password):
    SQL = "select * from user where username='%s' and password='%s'" % (username, password)
    print(SQL)
    db_handle = connect_sql()
    db_cursor = db_handle.cursor()
    db_cursor.execute(SQL)
    result = db_cursor.fetchall()
    print(result[0][0])
    print(result[0][1])
    print(result[0][2])
    # print(result)
    db_cursor.close()
    db_handle.close()
        
if __name__ == "__main__":
    check_user_login(username='leesin',password='leesin123')
