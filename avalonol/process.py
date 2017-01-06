import random
import time
from .helper import helper
from .models import User

def opening():  #total is an integer
    gamerIdList = helper.gamer
    total = len(helper.gamer)
    raw = [1,2,3,4,5,6,7,8,9,10]
    seats = raw[:total]
    roles = raw[:total]
    random.shuffle(seats)     #随机安排座位
    random.shuffle(roles)      #随机安排身份
    rolelist = helper.role[str(total)]    #获取对应人数的角色分配
    gamer1 = helper('gamer1', str(seats[0]), rolelist[str(roles[0])])
    gamer2 = helper('gamer2', str(seats[1]), rolelist[str(roles[1])])
    gamer3 = helper('gamer3', str(seats[2]), rolelist[str(roles[2])])
    gamer4 = helper('gamer4', str(seats[3]), rolelist[str(roles[3])])
    gamer5 = helper('gamer5', str(seats[4]), rolelist[str(roles[4])])
    helper.gamermap[gamerIdList[0]] = gamer1   #avalon_id到玩家代号、座位、身份的映射
    helper.gamermap[gamerIdList[1]] = gamer2
    helper.gamermap[gamerIdList[2]] = gamer3
    helper.gamermap[gamerIdList[3]] = gamer4
    helper.gamermap[gamerIdList[4]] = gamer5
    if total >= 6:
        gamer6 = helper('gamer6', str(seats[5]), rolelist[str(roles[5])])
        helper.gamermap[gamerIdList[5]] = gamer6
        if total >= 7:
            gamer7 = helper('gamer7', str(seats[6]), rolelist[str(roles[6])])
            helper.gamermap[gamerIdList[6]] = gamer7
            if total >= 8:
                gamer8 = helper('gamer8', str(seats[7]), rolelist[str(roles[7])])
                helper.gamermap[gamerIdList[7]] = gamer8
                if total >= 9:
                    gamer9 = helper('gamer9', str(seats[8]), rolelist[str(roles[8])])
                    helper.gamermap[gamerIdList[8]] = gamer9
                    if total == 10:
                        gamer10 = helper('gamer10', str(seats[9]), rolelist[str(roles[9])])
                        helper.gamermap[gamerIdList[9]] = gamer10
    else:
        pass
    helper.gamerque = que()
    return True

def que():
    gamerquetmp = {}
    for id,ins in helper.gamermap.items():
        gamerquetmp[int(ins.seat)] = User.objects.get(id=id).displayname
    return gamerquetmp

def rolemapping():
    '''将gamermap映射成为rolemap'''
    rolemaptmp = []
    for i,g in helper.gamermap.items():
        rolemaptmp.append((g.role,i))
    for (r,i) in rolemaptmp:
        if r == "梅林":
            helper.rolemap['派西维尔'][r] = i
        elif r == "莫德雷德":
            helper.rolemap['莫甘娜'][r] = helper.rolemap['刺客'][r] = helper.rolemap['莫德雷德的爪牙'][r] = i
        elif r == "莫甘娜":
            helper.rolemap['梅林'][r] = helper.rolemap['派西维尔'][r] = helper.rolemap['莫德雷德'][r] = helper.rolemap['刺客'][r] = helper.rolemap['莫德雷德的爪牙'][r] = i
        elif r == "刺客":
            helper.rolemap['莫甘娜'][r] = helper.rolemap['梅林'][r] = helper.rolemap['莫德雷德'][r] = helper.rolemap['莫德雷德的爪牙'][r] = i
        elif r == "莫德雷德的爪牙":
            helper.rolemap['莫甘娜'][r] = helper.rolemap['梅林'][r] = helper.rolemap['莫德雷德'][r] = helper.rolemap['刺客'][r] = i
        elif r == "奥伯伦":
            helper.rolemap['梅林'][r] = i
        else:
            helper.rolemap['Nobody'][r] = i
    return True

def message(id):
    rolemapping()
    role = helper.gamermap[id].role
    answer = helper.dialogue[role]
    if role not in ['亚瑟的忠臣','奥伯伦']:
        for r,i in helper.rolemap[role].items():
            answer = answer + User.objects.get(id=i).displayname + " "
    return answer

def board():
    boardtmp = {}
    for id,ins in helper.gamermap.items():
        subboardtmp = {}
        subboardtmp['Seat'] = ins.seat
        subboardtmp['Name'] = User.objects.get(id=id).displayname
        if int(ins.seat) == helper.leaderseat:
            subboardtmp['Leader'] = '/static/png/leader_token.png'
        else:
            subboardtmp['Leader'] = ''
        subboardtmp['Rounds'] = ins.boardround
        boardtmp[int(ins.seat)] = subboardtmp
    return boardtmp

def recordmember(members):
    helper.memberstodecide = members[:]
    for i,ins in helper.gamermap.items():
        if User.objects.get(id=i).displayname in helper.memberstodecide:
            ins.boardround.append(['1',' '])
        else:
            ins.boardround.append(['0',' '])
    substagechange()

def counting(aid,poll):
    helper.noticelen = len(helper.notice)    #更新通知长度
    pollnum = 0
    helper.polls[helper.roundnum][aid] = poll
    if len(helper.polls[helper.roundnum]) == len(helper.gamer):
        if helper.stageindex[0] == 1:
            helper.commandback = 0     #以防其他人从hall页面自动跳转
        for n,p in helper.polls[helper.roundnum].items():
            pollnum += int(p)
        if pollnum <= len(helper.gamer)/2:
            votefail()
        else:
            votesuccess()

def votefail():
    helper.votefailnum += 1
    for i,g in helper.gamermap.items():
        g.boardround.pop()
    votefailnotice()
    if helper.votefailnum >= 5:
        helper.stageindex[0] = 8    #######################final condition#######################
        return
    helper.roundnum += 1
    helper.polls[helper.roundnum] = {}
    substagechange('T')
    leaderchange()

def votefailnotice():
    vfnn = ""
    vfny = ""
    for i,p in helper.polls[helper.roundnum].items():
        if p == '0':
            vfnn += User.objects.get(id=i).username + ' '
        else:
            vfny += User.objects.get(id=i).username + ' '
    helper.notice.append("【任务"+str(helper.missionround)+"】反对："+ vfnn + ";支持："+ vfny )

def votesuccess():
    helper.votefailnum = 0
    for i,p in helper.polls[helper.roundnum].items():
        helper.gamermap[i].boardround[-1][1] = str(p)
    substagechange()
    helper.missions[helper.roundnum] = {}

def mission(aid,execu):
    missionpollnum = 0
    helper.missions[helper.roundnum][aid] = execu
    if len(helper.missions[helper.roundnum]) == helper.headcount[str(len(helper.gamer))][helper.missionround - 1]:
        for n, m in helper.missions[helper.roundnum].items():
            if m == '0':
                missionpollnum += 1
        if missionpollnum == 0:
            missionsuccess()
        elif len(helper.gamer) > 6 and helper.missionround == 4 and missionpollnum == 1:
            missionsuccess(str(missionpollnum))
        else:
            missionfail(str(missionpollnum))

def missionfail(fail):
    helper.winlose.append(fail)
    helper.missionfailnum += 1
    if helper.missionfailnum >= 3:
        helper.stageindex[0] = 8    #######################final condition#######################
        return
    helper.roundnum += 1
    helper.polls[helper.roundnum] = {}
    helper.missionround += 1
    superstagechange()
    substagechange()
    leaderchange()

def missionsuccess(fail='0'):
    if fail == '0':
        helper.winlose.append('W')
    else:
        helper.winlose.append(fail)
    helper.missionsuccessnum += 1
    if helper.missionsuccessnum >= 3:
        helper.stageindex[0] = 6
        return    #####################Assassination#######################
    helper.roundnum += 1
    helper.polls[helper.roundnum] = {}
    helper.missionround += 1
    superstagechange()
    substagechange()
    leaderchange()

def assassinate(one):
    helper.bekilled = one
    if helper.gamermap[User.objects.get(displayname=one).id].role == '梅林':
        helper.stageindex[0] = 8    #######################final condition#######################
    else:
        helper.stageindex[0] = 7    #######################final condition#######################
    return

def gameover():
    helper.gamer = []
    helper.roundnum = 1
    helper.missionround = 1
    helper.stageindex = [0,0]
    helper.rolemap = {'派西维尔':{},'梅林':{},'莫甘娜':{},'刺客':{},'莫德雷德':{},'莫德雷德的爪牙':{},'Nobody':{}}
    helper.gamerque = {}
    helper.leaderseat = 1
    helper.winlose = []
    helper.polls = {}
    helper.missions = {}
    helper.votefailnum = 0
    helper.missionfailnum = 0
    helper.missionsuccessnum = 0
    helper.gamermap = {}

def superstagechange():
    helper.stageindex[0] += 1

def substagechange(reset='F'):
    if reset == 'F'and helper.stageindex[1] != 2:
        helper.stageindex[1] += 1
    else:
        helper.stageindex[1] = 0

def leaderchange():
    if helper.leaderseat == len(helper.gamer):
        helper.leaderseat = 1
    else:
        helper.leaderseat += 1
