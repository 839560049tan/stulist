# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_cursor

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/main.html")


class CourseListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/cou_list.html", courses = dal_list_courses())


def dal_list_courses():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT * FROM student ORDER BY sno DESC
        """
        cur.execute(s)      
        for r in cur.fetchall():
            cou = dict(sno=r[0], sname=r[1], sage=r[2],ssex=r[3],sspecialty=r[4],sdepart=r[5],sdromitory=r[6], notes=r[7])
            data.append(cou)
    print(data)
    return data

