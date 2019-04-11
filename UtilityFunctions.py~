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
        return "Numele de utilizator deja există!"
    if len(password) < 8:
        return "Parola trebuie sa aibă cel puțin 8 caractere!"
    if len(sir_name) == 0 or len(given_name) == 0 or len(profile) == 0 or len(email) == 0 or len(username) == 0:
        return "Completați toate datele!"
    if (' ' in sir_name) or (' ' in given_name) or (' ' in profile) or (' ' in email) or (' ' in username):
        return "Spatiile nu sunt admise!"
    if sir_name.isalnum() == False or given_name.isalnum() == False or username.isalnum() == False or password.isalnum() == False:
        return "Folositi doar caractere alfanumerice"
    return "OK"

def RegisterData(username,password,sir_name,given_name,profile,email,teacher):
    manager.addUser(username,password,sir_name,given_name,profile,email,teacher)

def AddDataToSession(username,session):
    manager.AddDataToSession(username,session)

def UpdateSession(session):
    manager.UpdateSession(session)

def RegisterGroupValid(username,name):
    if len(name) == 0:
        return "Trebuie să dați un nume grupului!"
    if manager.groupExists(name,username):
        return "Grupul deja există!"
    return "OK"

def RegisterGroup(username,name):
    manager.addGroup(name,username)

def DeleteGroup(name,owner):
    manager.deleteGroup(name,owner)

def addMemberToGroup(name,owner,members):
    if manager.usernameExists(members):
        manager.addMembersToGroup(name,owner,members)
        return "OK"
    return "Nu există utilizatorul"

def removeMemberFromGroup(name,owner,member):
    if manager.usernameExists(member):
        manager.removeMemberFromGroup(name,owner,member)
        return "OK"
    return "Nu există utilizatorul"

def addHomeworksToGroup(name,owner,homeworkname,filename):
    manager.addHomeworksToGroup(name,owner,homeworkname,filename)

def deleteHomeworksFromGroup(homeworkfilename):
    manager.deleteHomeworksFromGroup(homeworkfilename)

def SubmitHomework(username,filename,homeworkfilename):
    manager.SubmitHomework(username,filename,homeworkfilename)

def GetSubmittedHomeworks(homeworkfilename):
    return manager.GetSubmittedHomeworks(homeworkfilename)

def getGroupMembers(name,owner):
    return sorted(manager.getGroupMembers(name,owner))

def getGroupsTheUserIsIn(username):
    return sorted(manager.getGroupsTheUserIsIn(username))

def getGivenHomeworks(name,owner):
    return manager.getGivenHomeworks(name,owner)
