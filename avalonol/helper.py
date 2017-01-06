# -*- coding: utf-8 -*-

class helper:
    fortest = []
    commandback = 0
    playerList = []  #等待玩家名单
    avalonIdList = []  #等待玩家id单
    gamer = []  #最终玩家名单
    superstages = ['开局','任务1','任务2','任务3','任务4','任务5','刺杀','亚瑟军获胜','莫德雷德阵营获胜']
    roundnum = 1        #全部游戏进程
    missionround = 1    #成功游戏进程
    substages = ['挑选队员','玩家投票','执行任务']
    stageindex = [0,0]
    role = {'5':{'1':'梅林', '2':'派西维尔', '3':'亚瑟的忠臣', '4':'莫甘娜', '5':'刺客'},
            '6':{'1':'梅林', '2':'派西维尔', '3':'亚瑟的忠臣', '4':'莫甘娜', '5':'刺客', '6':'亚瑟的忠臣'},
            '7':{'1':'梅林', '2':'派西维尔', '3':'亚瑟的忠臣', '4':'莫甘娜', '5':'刺客', '6':'亚瑟的忠臣', '7':'奥伯伦'},
            '8':{'1':'梅林', '2':'派西维尔', '3':'亚瑟的忠臣', '4':'莫甘娜', '5':'刺客', '6':'亚瑟的忠臣', '7':'莫德雷德的爪牙','8':'亚瑟的忠臣'},
            '9':{'1':'梅林', '2':'派西维尔', '3':'亚瑟的忠臣', '4':'莫甘娜', '5':'刺客', '6':'亚瑟的忠臣', '7':'莫德雷德','8':'亚瑟的忠臣', '9':'亚瑟的忠臣'},
            '10':{'1':'梅林', '2':'派西维尔', '3':'亚瑟的忠臣', '4':'莫甘娜', '5':'刺客', '6':'亚瑟的忠臣', '7':'莫德雷德','8':'亚瑟的忠臣', '9':'亚瑟的忠臣','10':'奥伯伦'}}
    gamermap = {}
    rolemap = {'派西维尔':{},'梅林':{},'莫甘娜':{},'刺客':{},'莫德雷德':{},'莫德雷德的爪牙':{},'Nobody':{}}
    gamerque = {}
    leaderseat = 1
    dialogue = {'梅林':'你看到坏人是',
                '派西维尔':'你看到梅林可能是',
                '莫甘娜':'你的同伙是',
                '刺客':'你的同伙是',
                '亚瑟的忠臣':'亚瑟万岁！',
                '奥伯伦':'谁是我的伙伴？',
                '莫德雷德':'你的部下是',
                '莫德雷德的爪牙':'你的同伙是'}
    notice = []
    noticelen = 0
    winlose = []
    headcount = {'5':[2,3,2,3,3],
                 '6':[2,3,4,3,4],
                 '7':[2,3,3,4,4],
                 '8':[3,4,4,5,5],
                 '9':[3,4,4,5,5],
                 '10':[3,4,4,5,5]}
    memberstodecide = []
    polls = {}
    missions = {}
    votefailnum = 0
    missionfailnum = 0
    missionsuccessnum = 0
    bekilled = ''
    release = 0

    def __init__(self, mark, seat, role):
        self.mark = mark
        self.seat = seat
        self.role = role
        self.boardround = []     #实例变量，记录玩家参与任务|投票情况

    def __unicode__(self):
        return self.mark
