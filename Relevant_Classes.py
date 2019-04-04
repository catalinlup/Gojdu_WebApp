ALL_GROUPS = []
ALL_USERS = []

class User:
    in_groups = []
    owned_groups = []
    def __init__(self,username,password,sir_name,given_name,profile,teacher=False):
        self.username = username
        self.password = password
        self.sir_name = sir_name
        self.given_name = given_name
        self.profile = profile
        self.teacher = teacher
    def createGroup(self,group_name):
        g = Group(group_name,self.username,self)
        ALL_GROUPS.append(g)
        this.owned_groups.append(g)

class Group:
    members = []
    def __init__(self,group_name,creator_username,user):
        self.group_name = group_name
        self.creator_username = creator_username
        user.in_groups.append(self.group_name)
    def addMember(self,username):
        self.members.append(username)
    def removeMember(self,username):
        if username in self.members:
            self.members.remove(username)

catalinlup = User('catalinlup','dragonul','Catalin','Lupau',)
