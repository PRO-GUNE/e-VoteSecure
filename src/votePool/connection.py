import pymysql

def get_db_connection():
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="secondarydb",
        host="mysql-39341dcb-cmggun456-1c5e.g.aivencloud.com",
        password="AVNS_b9CCV1O_xsp-dKGn1OT",
        read_timeout=timeout,
        port=12530,
        user="avnadmin",
        write_timeout=timeout,
        autocommit=True,
    )

    return connection


def get_target_db_connection():
    """
    Establish a connection to the target database where the data will be migrated.
    """
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="mysql-39341dcb-cmggun456-1c5e.g.aivencloud.com",
        password="AVNS_b9CCV1O_xsp-dKGn1OT",
        read_timeout=timeout,
        port=12530,
        user="avnadmin",
        write_timeout=timeout,
        autocommit=True,
    )
    return connection