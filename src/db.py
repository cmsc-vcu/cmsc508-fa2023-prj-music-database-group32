import pymysql

conn = pymysql.connect(
    host='cmsc508.com'
    database='23FA_groups_group32'
    user='23FA_farzanrl'
    password='Shout4_farzanrl_GOME'
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()