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

class CourseEditHandler(tornado.web.RequestHandler):
    def get(self, sno):

        cou = None
        if sno != 'new' :
            cou = dal_get_course(sno)
        
        if cou is None:
            cou = dict(sno='new', sname='', sage='', ssex='',sspecialty='',sdepart='',sdromitory='',notes='')

        self.render("pages/cou_edit.html", student = cou)

    def post(self, sno):
       
        sname = self.get_argument('sname', '')
        sage = self.get_argument('sage' )
        ssex = self.get_argument('ssex', '')
        sspecialty = self.get_argument('sspecialty', '')
        sdepart = self.get_argument('sdepart', '')
        sdromitory = self.get_argument('sdromitory', '') 
        notes = self.get_argument('notes', '')

        if sno == 'new' :
            dal_create_course(sname,sage,ssex,sspecialty,sdepart,sdromitory, notes)
        else:
            dal_update_course(sno,sname,sage,ssex,sspecialty,sdepart,sdromitory, notes)

        self.redirect('/coulist')

class CourseDelHandler(tornado.web.RequestHandler):
    def get(self, sno):
        dal_del_course(sno)
        self.redirect('/coulist')

# -------------------------------------------------------------------------

def dal_list_courses():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT * FROM student ORDER BY sno DESC  
        """
        cur.execute(s)       
        for r in cur.fetchall():
            cou = dict(sno=r[0], sname=r[1], sage=r[2],ssex=r[3],sspecialty=r[4], sdepart=r[5],sdromitory=r[6],notes=r[7])
            data.append(cou)
    return data


def dal_get_course(sno):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT * FROM student WHERE sno=%s
        """
        cur.execute(s, (sno,))
        r = cur.fetchone()
        if r :
            return dict(sno=r[0], sname=r[1], sage=r[2],ssex=r[3],sspecialty=r[4], sdepart=r[5],sdromitory=r[6],notes=r[7])


def dal_create_course( sname,sage,ssex,sspecialty,sdepart,sdromitory, notes):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        cur.execute("SELECT nextval('seq_sno')")
        sno = cur.fetchone()
        assert sno is not None

        print('新课程内部序号%d: ' % sno)

        s = """
        INSERT INTO student 
        VALUES (%(sno)s, %(sname)s, %(sage)s,%(ssex)s,%(sspecialty)s,%(sdepart)s,%(sdromitory)s,%(notes)s)
        """
        cur.execute(s, dict(sno=sno, sname=sname, sage=sage, ssex=ssex,sspecialty=sspecialty,sdepart=sdepart,sdromitory=sdromitory,notes=notes))


def dal_update_course(sno, sname,sage,ssex,sspecialty,sdepart,sdromitory, notes):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        UPDATE student SET
          sname=%(sname)s, 
          sage=%(sage)s, 
          ssex=%(ssex)s ,
          sspecialty=%(sspecialty)s,
          sdepart=%(sdepart)s,
          sdromitory=%(sdromitory)s,
          notes=%(notes)s
        WHERE sno=%(sno)s
        """
        cur.execute(s, dict(sno=sno, sname=sname, sage=sage, ssex=ssex,sspecialty=sspecialty,sdepart=sdepart,sdromitory=sdromitory,notes=notes))


def dal_del_course(sno):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        DELETE FROM student WHERE sno=%(sno)s
        """
        cur.execute(s, dict(sno=sno))
        print('删除%d条记录' % cur.rowcount)
