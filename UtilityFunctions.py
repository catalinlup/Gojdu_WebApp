from flask import *
from DB_Manager import *
import os

manager = DB_Manager()

#returns true if the login data is valid
def LoginDataValid(username,password):
    if manager.match(username,password):
        return True
    return False

def RegistrationDataValid(username,password,sir_name,given_name,profile,email):
    if manager.usernameExists(username):
        return "Numele de utilizator deja exista!"
    if len(password) < 8:
        return "Parola trebuie sa aiba cel putin 8 caractere!"
    if len(sir_name) == 0 or len(given_name) == 0 or len(profile) == 0 or len(email) == 0:
        return "Completati toate datele!"
    return "OK"

def RegisterData(username,password,sir_name,given_name,profile,email,teacher):
    manager.addUser(username,password,sir_name,given_name,profile,email,teacher)

def AddDataToSession(username,session):
    manager.AddDataToSession(username,session)

def UpdateSession(session):
    manager.UpdateSession(session)

def RegisterGroupValid(username,name):
    if len(name) == 0:
        return "Trebuie sa dati un nume grupului!"
    if manager.groupExists(name,username):
        print("DA")
        return "Grupul deja exista!"
    return "OK"

def RegisterGroup(username,name):
    manager.addGroup(name,username)

def addMemberToGroup(name,owner,members):
    if manager.usernameExists(members):
        manager.addMembersToGroup(name,owner,members)
        return "OK"
    return "Nu exista utilizatorul"

def addHomeworksToGroup(name,owner,homeworkname,filename):
    manager.addHomeworksToGroup(name,owner,homeworkname,filename)

def deleteHomeworksFromGroup(name,owner,homeworkfilename):
    print("DA")
    manager.deleteHomeworksFromGroup(name,owner,homeworkfilename)

def SubmitHomework(username,filename,homeworkfilename):
    manager.SubmitHomework(username,filename,homeworkfilename)

def GetSubmittedHomeworks(homeworkfilename):
    return manager.GetSubmittedHomeworks(homeworkfilename)

def getGroupMembers(name,owner):
    return manager.getGroupMembers(name,owner)

def getGroupsTheUserIsIn(username):
    return manager.getGroupsTheUserIsIn(username)

def getGivenHomeworks(name,owner):
    return manager.getGivenHomeworks(name,owner)



