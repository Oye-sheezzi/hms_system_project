import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="HospitalManagement"
    )

#Comment out if your driver i cx_oracle and remove all above
"""
import cx_oracle

def connect_to_db():
    return cx_oracle.connect(
        username="hr",
        password="12345678",
        dsn='localhost/xe'
    )
"""

#Comment out if your driver i oracledb and remove all above
"""
import oracledb as cx_oracle

def connect_to_db():
    return cx_oracle.connect(
        username="hr",
        password="12345678",
        dsn='localhost/xe'
    )
"""
