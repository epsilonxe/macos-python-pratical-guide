# -*- coding: utf-8 -*-
import unittest
import uuid
from blinker import signal, Signal
from datetime import datetime
import webbrowser
import hashlib, binascii, os
from enum import Enum
from pymongo import MongoClient
import inflect
from bson.objectid import ObjectId
import shutil
import time
import googlemaps
from collections import defaultdict
import re
import pandas as pd


ifEngine = inflect.engine()

client = MongoClient('127.0.0.1', 27017)
db = client['teach_db']
BASEDIR = os.path.dirname(os.path.realpath(__file__))
UPDIR = BASEDIR + "/uploads/"
unittest.TestLoader.sortTestMethodsUsing = None

DT_FORMAT = '%m/%d/%Y %H:%M:%S'

GG_APIKEY = 'AIzaSyAHt2-vkBvIOrvsgYLhOm0V2puJlSS6CvY'
def humantime2minutes(s):
    d = {
      'w':      7*24*60,
      'week':   7*24*60,
      'weeks':  7*24*60,
      'd':      24*60,
      'day':    24*60,
      'days':   24*60,
      'h':      60,
      'hr':     60,
      'hour':   60,
      'hours':  60,
    }
    mult_items = defaultdict(lambda: 1).copy()
    mult_items.update(d)

    parts = re.search(r'^(\d+)([^\d]*)', s.lower().replace(' ', ''))
    if parts:
        return int(parts.group(1)) * mult_items[parts.group(2)] + humantime2minutes(re.sub(r'^(\d+)([^\d]*)', '', s.lower()))
    else:
        return 0

class SessionStatus(Enum):
    FULL = 1
    LIVE = 2
    END = 3

class PopUp:
    def __init__(self,question, choices, answer, at):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.at = at

    def ans(self, an):
        return an in self.answer


class CSession:
    def __init__(self, name, start, end):
        self.name = name
        self.uid = uuid.uuid1()
        self.start = datetime.strptime(start, DT_FORMAT)
        self.end = datetime.strptime(end, DT_FORMAT)
        self.on_live = Signal('on-live')
        self.on_end = Signal('on-end')
        self.liveURL = None
        self._teacher = None
        self.popups = []

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, t):
        self.on_live.connect(t.live_recv)
        self.on_end.connect(t.session_end_recv)
        self._teacher = t

    def live(self):
        self.on_live.send(self, msg="hello")

    def liveEnd(self):
        self.on_end.send(self, msg="bye")

    def openLive(self):
        webbrowser.open_new(self.liveURL)

class Db:
    _db = db
    _ifEngine = ifEngine
    def __init__(self):
        self.oid = None


    def colName(self):
        return self._ifEngine.plural(self.__class__.__name__.lower())

    @classmethod
    def get(cls, oid):
        o = cls._db[cls().colName()].find_one({'_id': oid})

        c = cls()
        for f in cls.fields:
            setattr(c, f, o.get(f, None))

        c.oid = o['_id']
        return c

    @classmethod
    def filter(cls, **kwargs):
        r = cls._db[cls().colName()].find(kwargs)

        l = list()
        for r0 in r:
            c = cls()

            for f in cls.fields:
                setattr(c, f, r0.get(f, None))
            l.append(c)
        return l

    @classmethod
    def remove(cls, **kwargs):
        return cls._db[cls().colName()].delete_many(kwargs)

    def save(self):

        print("fields = ", self.fields)
        temp = {}

        for f in self.fields:
            temp[f] = getattr(self, f)

        if self.oid is None:
            o = self._db[self.colName()].insert_one(temp)
            self.oid = o.inserted_id
        else:
            self._db[self.colName()].find_one_and_update({'_id': self.oid}, {'$set': temp})

        return self


class Ticket:
    def __init__(self, serve, request):
        self.request = request
        self.serve = serve
        self.uid = uuid.uuid1()
        self.use = False
        self.useTime = None

    def setTime(self, dtStr):
        self.useTime = datetime.strptime(dtStr, DT_FORMAT)

class CourseMaterial:
    def __init__(self, title, tags,  srcFile):
        self.title = title
        self.tags = tags
        self.srcFile = srcFile
        self.filepath = None

    def saveFile(self):
        fn, ext = os.path.splitext(self.srcFile)
        #dt = int(time.time())
        dt = int(round(time.time() * 1000))
        print("dt", dt)
        self.filepath = UPDIR + f"{dt}{ext}"
        shutil.copyfile(self.srcFile, self.filepath)

class CourseTopic:
    def __init__(self, title, duration, tags):
        self.title = title
        self.duration = pd.Timedelta(duration)
        self.tags = tags

    def __str__(self):
        return f"{self.title}, {self.tags}"

    def __repr__(self):
        return f"{self.title}, {self.tags}"

class Course(Db):
    fields = ('title', 'cats', 'uid', 'students', 'sessions', 'tickets')

    def __init__(self, title = None, cats = None):
        Db.__init__(self)
        self.title = title
        self.cats = cats
        self.uid = uuid.uuid1()
        self.students = []
        self.sessions = []
        self.tickets = []
        self.materials = []
        self.topics = self.adapTopics = []

    def adapt(self, prefers):
        self.adapTopics = self.topics
        ai = 0;
        for pi in range(len(prefers)):
            for ti in range(len(self.adapTopics)):
                if prefers[pi] in self.adapTopics[ti].tags:
                    self.adapTopics.insert(ai,self.adapTopics.pop(ti))
                    ai += 1



    def addStudent(self, st):
        self.students.append(st)

    def addSession(self, session):
        self.sessions.append(session)
        return session

    def addMaterial(self, cm):
        cm.saveFile()
        self.materials.append(cm)


    def searchMats(self, **kwargs):
        results = []
        for s in self.materials:
            match = True
            for k in kwargs.keys():

                if k == "title":
                    match = kwargs[k] in s.title
                if k == "tags":
                    print(kwargs[k], s.tags)
                    match = kwargs[k] in s.tags

                if match == False:
                    break
            if match == True:
                results.append(s)
        return results

    def freetimeFit(self, student):
        for f in student.frees:
            for s in self.sessions:
                if f >= s.start and f <= s.end:
                    return s
        return None

    def createTicket(self, session, student):
        found = [s for s in self.sessions if session == s]
        if len(found) == 0:
            return None
        else:
            ticket = Ticket(session, student)
            session.on_live.connect(student.live_recv)
            session.on_end.connect(student.session_end_recv)
            self.tickets.append(ticket)
            return ticket

    def useTicket(self, ticket):
        found = [t for t in self.tickets if t == ticket and t.use == False ]
        #print("found = ", found)
        #print(self.tickets, ticket)
        if len(found) == 0:
            return False
        else:
            ss = found[0].serve

            if ticket.useTime >= ss.start \
            and ticket.useTime <= ss.end:
                found[0].use = True
                return True
            else:
                return False

    def __repr__(self):
        return f"{self.uid}#{self.title}"


class BasePerson:
    fields = ('name', 'lastName', 'email', 'uid', 'frees', 'waitings', 'stored_password')
    def __init__(self, name, lastName, email=None):
        self.name = name
        self.lastName = lastName
        self.uid = uuid.uuid1()
        self.frees = []
        self.waitings = []
        self.email = email
        self.stored_password = None


    def addFreeTime(self, free):
        temp = datetime.strptime(free, DT_FORMAT)
        self.frees.append(temp)

    def live_recv(self, sender, **kwg):
        print("me = %r, sender = %r, %r" %  (self, sender, kwg))
        self.waitings.append(sender)

    def session_end_recv(self, sender, **kwg):
        print("me = %r, sender = %r, %r" %  (self, sender, kwg))
        self.waitings.remove(sender)

    def newCourseRecv(self, sender, **kwg):
        print("me = %r, sender = %r, %r" %  (self, sender, kwg))

    def newStudentRecv(self, sender, **kwg):
        print("me = %r, sender = %r, %r" %  (self, sender, kwg))

    def newTeacherRecv(self, sender, **kwg):
        print("me = %r, sender = %r, %r" %  (self, sender, kwg))


    def recordPassword(self, passwd,confirm):
        if passwd == confirm:
            self._hash_password(passwd)
            return True
        else:
            return False

    def _hash_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
				    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        self.stored_password = (salt + pwdhash).decode('ascii')

    def verify_password(self, provided_password):
        """Verify a stored password against one provided by user"""
        salt = self.stored_password[:64]
        stored_password = self.stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

class Student(BasePerson, Db):
    def __init__(self, name, lastName, email=None):
        BasePerson.__init__(self, name, lastName, email)
        Db.__init__(self)
        self.subjects = []
        self.locations = []
        self.max_per_hour = 100
        self.prefers = []

    def __str__(self):
        return f"subjects={self.subjects}, locations={self.locations}, max_per_hour={self.max_per_hour}"

    def __repr__(self):
        return f"subjects={self.subjects}, locations={self.locations}, max_per_hour={self.max_per_hour}"

class Teacher(BasePerson, Db):
    def __init__(self, name, lastName, email=None):
        BasePerson.__init__(self, name, lastName, email)
        Db.__init__(self)

class DbManager:
    @classmethod
    def commit(cls,objlist):
        for o in objlist:
            o.save()

class TSys:
    gmaps = googlemaps.Client(key=GG_APIKEY)

    def __init__(self, name):
        self.name = name
        self.courses = []
        self.cats = set()
        self.students = set()
        self.teachers = set()

        self.on_new_course = Signal('on-new-course')
        self.on_new_student = Signal('on-new-student')
        self.on_new_teacher = Signal('on-new-teacher')

    def commit(self):
        DbManager.commit(self.courses)
        DbManager.commit(self.teachers)
        DbManager.commit(self.students)
        return True

    def addCat(self, cat):
        for c in cat:
            self.cats.add(c)

    def direction(self, *args, **kwargs):
        return TSys.gmaps.directions(*args, **kwargs)

    def geocode(self, *args, **kwargs):
        return TSys.gmaps.geocode(*args, **kwargs)

    def _connectSignal(self, o):
        self.on_new_teacher.connect(o.newTeacherRecv)
        self.on_new_student.connect(o.newTeacherRecv)
        self.on_new_course.connect(o.newCourseRecv)


    def newTeacher(self,t):
        self.on_new_teacher.send(self, teacher=t)

    def newStudent(self,t):
        self.on_new_student.send(self, student=t)

    def newCourse(self,t):
        self.on_new_course.send(self, course=t)



    def addTeacher(self, t):
        self._connectSignal(t)

        found = [x for x in self.teachers if t.email == x.email]
        if len(found) == 0:
            self.teachers.add(t)
            self.newTeacher(t)
            return True
        else:
            return False


    def addStudent(self, s):
        self._connectSignal(s)

        found = [x for x in self.students if s.email == x.email]
        if len(found) == 0:
            self.students.add(s)
            self.newStudent(s)
            return True
        else:
            return False

    def studentLogin(self, email, passwd):
        found = [x for x in self.students if email == x.email]
        if len(found) > 0:
            if found[0].verify_password(passwd) == True:
                return found[0]
            else:
                return False
        else:
            return False

    def teacherLogin(self, email, passwd):
        found = [x for x in self.teachers if email == x.email]
        if len(found) > 0:
            if found[0].verify_password(passwd) == True:
                return found[0]
            else:
                return False
        else:
            return False

    def createCourse(self, course):
        self.courses.append(course)
        self.newCourse(course)

    def filter(self, cats):
        results = []
        for c in cats:
            results.extend([x for x in self.courses if c in x.cats ])
        return results

    def find_students(self, filters):
        results = []
        for s in self.students:
            match = True
            for k in filters.keys():
                if k == "subject":
                    match = filters[k] in s.subjects
                if k == "location":
                    match = filters[k] in s.locations
                if k == "per_hour":
                    if s.max_per_hour >= filters[k]:
                        match = True
                    else:
                        match = False
                if match == False:
                    break
            if match == True:
                results.append(s)
        return results

class TestTeacher(unittest.TestCase):
    def setUp(self):
        self.tsys = TSys("My Store")

        self.tsys.createCourse(Course(title="Course A", cats = ["Physic", "Math"]))
        self.tsys.createCourse(Course(title="Course B", cats = ["Math"]))

    def tearDown(self):
        Course.remove()

    def test_course_count(self):

        self.assertEqual(len(self.tsys.courses), 2)

    def test_course_find_cat(self):
        courses = self.tsys.filter(cats = ["Math"])
        print(courses)
        self.assertEqual(len(courses), 2)

        courses = self.tsys.filter(cats = ["Physic"])
        self.assertEqual(len(courses), 1)

    def test_add_student(self):
        ac = self.tsys.courses[0]
        st = Student(name="ABC", lastName="DEF")
        ac.addStudent(st)
        self.assertEqual(len(ac.students), 1)

    def test_can_learn(self):
        ac = self.tsys.courses[0]
        cs = CSession(name="Mornine", start = "03/04/2020 09:30:00",
                      end = "03/04/2020 10:30:00")
        ac.addSession(cs)

        st = Student(name="ABC", lastName="DEF")
        st.addFreeTime("03/04/2020 09:45:00")

        ac.addStudent(st)

        s1 = ac.sessions[0]
        canLearn = ac.freetimeFit(st)
        self.assertEqual(canLearn,s1)

        ac1 = self.tsys.courses[1]
        cs = CSession(name="Mornine", start = "03/04/2020 12:30:00",
                      end = "03/04/2020 13:00:00")
        ac1.addSession(cs)
        s1 = ac1.sessions[0]
        canLearn = ac1.freetimeFit(st)
        self.assertEqual(canLearn,None)

    def test_create_ticker(self):
        ac = self.tsys.courses[0]
        cs = CSession(name="Morning", start="03/04/2020 12:30:00",
                      end = "03/04/2020 12:45:00")
        s1 = ac.addSession(cs)
        student = Student(name="ABC", lastName="DEF")
        ticket = ac.createTicket(s1, student)
        ticket.setTime("03/04/2020 12:31:00")

        ticket2 = ac.createTicket(s1, student)
        ticket2.setTime("03/04/2020 14:00:00")

        self.assertEqual(ticket.request.uid, student.uid)
        self.assertEqual(ticket.serve.uid, cs.uid)
        self.assertEqual(len(ac.tickets), 2)

        self.assertEqual(ac.useTicket(ticket), True)
        self.assertEqual(ac.useTicket(ticket), False)
        self.assertEqual(ac.useTicket(ticket2), False)

    def test_add_cats(self):
        l0  = len(self.tsys.cats)

        self.tsys.addCat(["ABC"])
        self.assertEqual(len(self.tsys.cats), l0+1)

        self.tsys.addCat(["ABC"])
        self.assertEqual(len(self.tsys.cats), l0+1)

        self.tsys.addCat(["ABC","CDE"])
        self.assertEqual(len(self.tsys.cats), l0+2)

    def test_course_reminder(self):
        ac = self.tsys.courses[0]
        cs = CSession(name="Morning", start="03/04/2020 12:30:00",
                      end = "03/04/2020 12:45:00")
        s1 = ac.addSession(cs)
        student = Student(name="ABC", lastName="DEF")
        ticket = ac.createTicket(s1, student)

        cs.live()
        cs.liveURL = "https://www.youtube.com/watch?v=o-4hu7NNpGU"
        self.assertEqual(len(student.waitings) , 1)
        self.assertEqual(student.waitings[0], cs)

        #cs.openLive()
        cs.liveEnd()
        self.assertEqual(len(student.waitings) , 0)


    def test_teacher_create_course(self):
        ac = self.tsys.courses[0]
        cs = CSession(name="Morning", start="03/04/2020 12:30:00",
                      end = "03/04/2020 12:45:00")
        cs.teacher = Teacher(name="Tum", lastName="Hello")
        s1 = ac.addSession(cs)
        student = Student(name="ABC", lastName="DEF")
        ticket = ac.createTicket(s1, student)

        cs.live()
        cs.liveEnd()

    def test_alerts_tsys(self):
        self.tsys.addTeacher(Teacher(name="wow", lastName="ABC"))
        self.tsys.addTeacher(Teacher(name="wow2", lastName="ABC"))

        self.tsys.addStudent(Student(name="st1", lastName="ABC"))
        self.tsys.addStudent(Student(name="st2", lastName="ABC"))

        self.tsys.createCourse(Course(title="Course ABCD", cats = ["Physic", "Math"]))


    def test_student_login(self):
        s = Student(name="wow", lastName="ABC", email="patumos@gmail.com")
        self.assertEqual(s.recordPassword("abc", "abc"), True)
        self.assertEqual(s.recordPassword("abc", "abcd"), False)

        self.assertEqual(s.verify_password("abc"), True)
        self.assertEqual(s.verify_password("abcd"), False)

    def test_add_student_teacher_center(self):
        s = Student(name="wow", lastName="ABC", email="patumos@gmail.com")
        self.assertEqual(s.recordPassword("abc", "abc"), True)
        self.assertEqual(self.tsys.addStudent(s), True)
        self.assertEqual(self.tsys.addStudent(s), False)

        t = Teacher(name="wow", lastName="ABC", email="patumos@gmail.com")
        self.assertEqual(t.recordPassword("abc", "abc"), True)
        self.assertEqual(self.tsys.addTeacher(t), True)
        self.assertEqual(self.tsys.addTeacher(t), False)

        self.assertEqual(self.tsys.studentLogin("patumos@gmail.com", "abc"), s)
        self.assertEqual(self.tsys.studentLogin("patumos@hotmail.com", "abc"), False)

        self.assertEqual(self.tsys.teacherLogin("patumos@gmail.com", "abc"), t)
        self.assertEqual(self.tsys.teacherLogin("patumos@gmail.com", "abcde"), False)

    def test_course_save(self):
        course = Course(title="PH", cats = ["A", "B"])
        course.save()
        self.assertNotEqual(course.save(), None)

    def test_record_get_and_update(self):

        course = Course(title="PH", cats = ["A", "B"])
        c = course.save()
        print("test record ", c)
        c0 = Course.get(oid=c.oid)
        self.assertEqual(c.oid, c0.oid)
        c0.title = "PHA"
        oid = c0.oid
        c0.save()
        self.assertEqual(oid, c0.oid)

    def test_record_filter(self):

        course = Course(title="PH", cats = ["A", "B"])
        c = course.save()

        results = Course.filter(title="PH")
        self.assertEqual(len(results), 1)


        course = Course(title="PH", cats = ["A", "B"])
        c = course.save()

        results = Course.filter(title="PH")
        self.assertEqual(len(results), 2)

    def test_tsys_save(self):

        t = Teacher(name="wow", lastName="ABC", email="patumos@gmail.com")
        t.addFreeTime("03/04/2020 09:45:00")
        t.recordPassword("abc", "abc")

        self.tsys.addTeacher(t)
        self.tsys.addTeacher(Teacher(name="wow", lastName="ABC", email="patumos@hotmail.com"))
        self.tsys.addStudent(Student(name="wow", lastName="ABC", email="patumos@gmail.com"))
        self.tsys.addStudent(Student(name="wow", lastName="ABC", email="patumos@hotmail.com"))
        self.assertEqual(self.tsys.commit(), True)

#consumer canvas
'''
Main Job:
Teacher:
    - want to find students
    - want to shedule fit
    - want to manage course mats
Gain:
    - want to teach subjects that they expert
    - want to get good salary
    - near their resident
    - good internet speed
    - adapt course outline
    - make lession not boring
    - easy payment
Pains:
    - web slow
    - too few students
    - very far from their houese
    - bad feedback
    - money too low

'''
class TestTeacherJobs(unittest.TestCase):
    def setUp(self):
        self.tsys = TSys("My Store")

        self.tsys.createCourse(Course(title="Course A", cats = ["Physic", "Math"]))
        self.tsys.createCourse(Course(title="Course B", cats = ["Math"]))

    def tearDown(self):
        Course.remove()
        #pass

    def test_find_students(self):
        #self.tsys.addStudent(Student())
        st = Student(name="st1",lastName="ABC")
        st.subjects = ["A", "B"]
        st.locations = ["Chanthaburi", "Chonburi"]
        st.max_per_hour = 200

        self.tsys.addStudent(st)
        filters = {'subject': 'A', 'location': 'Chanthaburi', 'per_hour': 100}
        students = self.tsys.find_students(filters)
        self.assertEqual(len(students), 1)

        filters = {'subject': 'C', 'location': 'Chanthaburi', 'per_hour': 100}
        students = self.tsys.find_students(filters)
        print(students)
        self.assertEqual(len(students), 0)

    def test_schedule_fit(self):
        ac = self.tsys.courses[0]
        cs = CSession(name="Mornine", start = "03/04/2020 09:30:00",
                      end = "03/04/2020 10:30:00")
        ac.addSession(cs)

        st = Student(name="ABC", lastName="DEF")
        st.addFreeTime("03/04/2020 09:45:00")

        ac.addStudent(st)

        s1 = ac.sessions[0]
        canLearn = ac.freetimeFit(st)
        self.assertEqual(canLearn,s1)

        ac1 = self.tsys.courses[1]
        cs = CSession(name="Mornine", start = "03/04/2020 12:30:00",
                      end = "03/04/2020 13:00:00")
        ac1.addSession(cs)
        s1 = ac1.sessions[0]
        canLearn = ac1.freetimeFit(st)
        self.assertEqual(canLearn,None)

    def test_manage_cm(self):
        #manage course mats
        ac = self.tsys.courses[0]
        cs = CSession(name="Mornine", start = "03/04/2020 09:30:00",
                      end = "03/04/2020 10:30:00")
        ac.addSession(cs)

        cwd = os.getcwd()
        afile = cwd + "/test.txt"
        bfile = cwd + "/test2.txt"
        cm1 = CourseMaterial(title="ABC", tags=["t1", "t2", "t3"], srcFile=BASEDIR + "/test.txt")
        ac.addMaterial(cm1)
        cm2 = CourseMaterial(title="ABC", tags=["t1", "t2", "t3"], srcFile=BASEDIR + "/test2.txt")
        ac.addMaterial(cm2)

        self.assertEqual(len(ac.materials), 2)

        s1 = ac.searchMats(title="DE")
        self.assertEqual(len(s1), 0)

        s2 = ac.searchMats(tags="t1")
        self.assertEqual(len(s2), 2)

    def test_search_students(self):
        pass

    def test_minimum_income(self):
        pass

    def test_near_loc(self):
        pass
        #print(self.tsys.direction(origin='chanthaburi', destination='bangkok'))
        #print(self.tsys.geocode('Pattaya Thailand'))

    def test_adapt_course_outline(self):
        #if student request more stress on some topics outline can be adjust
        course = self.tsys.courses[0]
        course.topics = [
            CourseTopic(title='abc', duration="20min", tags=["a", "b", "ed"]),
            CourseTopic(title='abc1', duration="40min", tags=["a", "b", "cd"]),
            CourseTopic(title='abc2', duration="10min", tags=["a", "b", "jk"]),
            CourseTopic(title='abc3', duration="35min", tags=["a", "b", "cn"]),
        ]
        s1 = Student(name="S1", lastName="L1")
        s1.prefers = ["cd", "ed"]
        course.adapt(s1.prefers)

        self.assertEqual("cd" in course.adapTopics[0].tags,True)
        print(course.adapTopics)
        self.assertEqual("ed" in course.adapTopics[1].tags,True)


    def test_popup_in_session(self):
        ac = self.tsys.courses[0]
        cs = CSession(name="Mornine", start = "03/04/2020 09:30:00",
                      end = "03/04/2020 10:30:00")
        ac.addSession(cs)

        cs.popups = [
            PopUp(question="ABC ?", choices = [
                "A. aaa",
                "B. aaa",
                "C .ccc"
            ],
            answer = [1], at="10min"),
            PopUp(question="ABCD ?", choices = [
                "A. aaa",
                "B. aaa",
                "C .ccc"
            ],
            answer = [1,2], at="30min"),
        ]

        pop  = cs.popups[0]
        self.assertEqual(pop.ans(1), True)
        self.assertEqual(pop.ans(2), False)

    def test_easy_payment(self):
        #https://github.com/braintree/braintree_flask_example
        pass

    def test_min_student(self):
        pass

    def test_upper_range_location(self):
        pass

'''
Student:
Jobs:
    - study lessons
    - search courses
    - save course materials
    - find good teacher
    - ask questions to teachers
    - solve their problems
Gain:
    - course not too long
    - course price not too high
    - search text in course easily
    - get answer quickly
    - teachers near their houses
    - study with friends
Pain:
    - too long courses
    - lession is boring
    - web slow
    - not see teacher personaly
    - too difficult to learn something that not know before
'''
if __name__ == "__main__":
    unittest.main()
