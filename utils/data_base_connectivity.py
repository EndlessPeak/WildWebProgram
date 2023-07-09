import pymysql
import json

def get_db_config():
    with open('./static/config.json','r') as file:
        # Warning: json file must enclose name in double quotes
        config = json.load(file)
    return config
    
'''
Access the database configure file and try connect to database
1. First, access the data base config file
2. Second, obtain the data base handle and return
Warning:
we set the cursor type as a dictionary,
so that it can be accessed later through the fields of the dictionary.
'''
def connect_sql():
    db_config = get_db_config()
    db_handle = pymysql.connect(
        host = db_config['host'],
        port = db_config['port'],
        user = db_config['user'],
        password = db_config['password'],
        db = db_config['database'],
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor,
    )
    return db_handle

'''
Insert data to database
Return the number of rows affected by SQL statement.
'''
def insert_data(sql_sentence):
    db_handle = connect_sql()
    db_cursor = db_handle.cursor()
    db_cursor.execute(sql_sentence)
    count = cursor.rowcount 
    # when debug,this will be commented
    # db_handle.commit()
    db_cursor.close()
    db_handle.close()
    return count
    
'''
Query data from database
Num indicate how many reults should the function return
'''
def query_data(num,sql_sentence):
    db_handle = connect_sql()
    db_cursor = db_handle.cursor()
    db_cursor.execute(sql_sentence)
    if num == 1:
        results = db_cursor.fetchone()
    elif num == 0:
        results = db_cursor.fetchall()
    else:
        results = db_cursor.fetmany(num)
    db_cursor.close()
    db_handle.close()
    return results

'''
Access the database to retrieve the username and password,
then check if they are correct.
'''
def check_user_login(username,password):
    sql_sentence = "select * from user where username='%s' and password='%s'" % (username, password)
    print(sql_sentence)
    result = query_data(num=1,sql_sentence=sql_sentence)
    print(result['uid'])
    print(result['username'])
    print(result['password'])
        
if __name__ == "__main__":
    check_user_login(username='leesin',password='leesin123')
