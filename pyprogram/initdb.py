#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

from dbconn import db_cursor

def create_db():
    sqlstr = """
    DROP TABLE IF EXISTS student;

    CREATE TABLE IF NOT EXISTS student (
        sno   INTEGER,      --学号
        sname   TEXT,       --姓名
        sage     TEXT,      --年龄
        ssex     TEXT,      --性别
        sspecialty TEXT,    --专业
        sdepart  TEXT,      --系别
        sdromitory TEXT,    --宿舍区
        notes    TEXT,
        PRIMARY KEY(sno)
    );
    -- CREATE UNIQUE INDEX idx_course_no ON course(cou_no);

    CREATE SEQUENCE seq_sno 
        START 10000 INCREMENT 1 OWNED BY student.sno;

    """
    with db_cursor() as cur :
        cur.execute(sqlstr) # 执行SQL语句
    
def init_data():
    sqlstr = """
    DELETE FROM student;

    INSERT INTO student  VALUES 
        (101, '王二',20,'男','人力','管院','西苑7号楼'), 
        (102, '张三',19,'男','信息','管院','西苑7号楼'),
        (103, '李四',20,'女','信息','管院','西苑5号楼');

    """
    with db_cursor() as cur :
        cur.execute(sqlstr)    

if __name__ == '__main__':
    create_db()
    init_data()
    print('数据库已初始化完毕！')

