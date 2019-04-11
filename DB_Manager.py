import pymongo
from Configs import *
from UtilityFunctions import *
import os
class DB_Manager:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27018/")
        #self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient[DB_NAME]
        self.users = self.mydb['users']
        self.groups = self.mydb['groups']
        self.homework = self.mydb['homeworks']

    def addUser(self,username,password,sir_name,given_name,profile,email,teacher=False):
        dict = {'username':username,'password':password,'sir_name':sir_name,'given_name':given_name,'profile':profile,'email':email,'teacher':teacher}
        self.users.insert_one(dict)

    def addGroup(self,name,owner):
        dict = {'name':"{}_{}".format(owner,name),'owner':owner,'members':[],'given_homeworks':[]}
        self.groups.insert_one(dict)

    def deleteGroup(self,name,owner):
        if self.groupExists(name,owner):
            gr = self.groups.find_one({'name':"{}_{}".format(owner,name)})
            if 'given_homeworks' in gr.keys():
                for h in gr['given_homeworks']:
                    self.deleteHomeworksFromGroup(h[1])
            self.groups.delete_one({'name':"{}_{}".format(owner,name)})

    def addMembersToGroup(self,name,owner,members):
        if self.groupExists(name,owner):
            post = self.groups.find_one({'name':"{}_{}".format(owner,name)})
            originalMembers = list(post['members'])
            if originalMembers == None:
                originalMembers = []
            elif members not in originalMembers:
                originalMembers.append(members)
            post['members'] = originalMembers
            self.groups.save(post)

    def removeMemberFromGroup(self,name,owner,member):
        if self.groupExists(name,owner):
            post = self.groups.find_one({'name':"{}_{}".format(owner,name)})
            originalMembers = list(post['members'])
            if originalMembers == None:
                originalMembers = []
            elif member in originalMembers:
                originalMembers.remove(member)
            post['members'] = originalMembers
            self.groups.save(post)

    def addHomeworksToGroup(self,name,owner,homeworkname,filename):
        if self.groupExists(name,owner):
            post = self.groups.find_one({'name':"{}_{}".format(owner,name)})
            originalHomeworks = list(post['given_homeworks'])
            if originalHomeworks == None:
                originalHomeworks = []
            elif [homeworkname,filename] not in originalHomeworks:
                originalHomeworks.append([homeworkname,filename])
            post['given_homeworks'] = originalHomeworks
            filename = filename.replace('.','_')
            self.groups.save(post)

    def deleteHomeworksFromGroup(self,homeworkfilename):
        filesToDelete = []
        filesToDelete.append(homeworkfilename)

        groupList = self.groups.find()
        gName = None
        for g in groupList:
            if 'given_homeworks' not in g.keys():
                continue
            for h in g['given_homeworks']:
                if homeworkfilename in h:
                    gName = g['name']

        if gName != None:
            post = self.groups.find_one({'name':gName})
            originalHomeworks = list(post['given_homeworks'])

            for h in originalHomeworks:
                if homeworkfilename in h:
                    originalHomeworks.remove(h)
                    break
            post['given_homeworks'] = originalHomeworks

            self.groups.save(post)

        uploadedHomework = self.homework.find({'homeworkfilename':homeworkfilename})
        for h in uploadedHomework:
            filesToDelete.append(h['filename'])

        self.homework.delete_many({'homeworkfilename':homeworkfilename})
        print(filesToDelete)
        self.deleteUploadedFiles(filesToDelete)

    def deleteUploadedFiles(self,files):
        for fl in files:
            os.remove('uploadedFiles/{}'.format(fl))

    def SubmitHomework(self,username,filename,homeworkfilename):
        self.homework.update({'username':username,'homeworkfilename':homeworkfilename},{'username':username,'filename':filename,'homeworkfilename':homeworkfilename},upsert=True)

    def GetSubmittedHomeworks(self,homeworkfilename):
        ret = self.homework.find({'homeworkfilename':homeworkfilename})
        ls = []
        for work in ret:
            ls.append([work['username'],work['filename']])
        print(homeworkfilename)
        return ls

    def getGroupMembers(self,name,owner):
        if self.groupExists(name,owner):
            post = self.groups.find_one({'name':"{}_{}".format(owner,name)})
            return post['members']
        return []

    def getGivenHomeworks(self,name,owner):
        if self.groupExists(name,owner):
            post = self.groups.find_one({'name':"{}_{}".format(owner,name)})
            return post['given_homeworks']
        return []
    def getGroupsTheUserIsIn(self,username):
        groupList = self.groups.find()
        filteredGroups = []
        for gr in groupList:
            if gr['members']!= None and username in gr['members']:
                filteredGroups.append(gr['name'])
        return filteredGroups

    def AddDataToSession(self,username,session):
        if self.usernameExists(username):
            myquerry = {'username':username}
            mydoc = self.users.find_one(myquerry)
            session['username'] = mydoc['username']
            session['password'] = mydoc['password']
            session['sir_name'] = mydoc['sir_name']
            session['given_name'] = mydoc['given_name']
            session['profile'] = mydoc['profile']
            session['email'] = mydoc['email']
            session['teacher'] = mydoc['teacher']
            session['logged_in'] = True
            GroupNames = []
            grs = list(self.groups.find({'owner':username}))
            for gr in grs:
                GroupNames.append([gr['name'],gr['name'].split('_')[1]])
            session['owned_groups'] = GroupNames
            session['groups_in'] = self.getGroupsTheUserIsIn(username)


    def UpdateSession(self,session):
        self.AddDataToSession(session['username'],session)

    def usernameExists(self,username):
        myquerry = {'username':username}
        mydoc = self.users.find(myquerry)
        return (mydoc.count() != 0)

    def groupExists(self,name,owner):
        myquerry = {'name':"{}_{}".format(owner,name)}
        mydoc = self.groups.find(myquerry)
        return (mydoc.count() != 0)

    def match(self,username,password):
        if self.usernameExists(username):
            myquerry = {'username':username}
            mydoc = self.users.find_one(myquerry)
            if password == mydoc['password']:
                return True
        return False
