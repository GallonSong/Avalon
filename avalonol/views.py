# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

# import urllib.parse

from .models import User

from .helper import helper
from . import process

# Create your views here.
def login(request):
    if 'avalon_id' in request.session:
        user = User.objects.get(id = request.session['avalon_id'])
        return HttpResponseRedirect('/avalonol/hall/')
    else:
        if 'username' in request.POST:
            if len(User.objects.filter(username__exact=request.POST['username']))==1:
                user = User.objects.get(username=request.POST['username'])
                if user.password == request.POST['password']:
                    request.session['avalon_id'] = user.id
                    return HttpResponseRedirect('/avalonol/hall/')
                else:
                    return render(request,'avalonol/login.html',{'errormsg':'密码错误！'})
            else:
                return render(request,'avalonol/login.html',{'errormsg':'用户名错误！'})
        else:
            return render(request,'avalonol/login.html',{'errormsg':'请先登录！'})

def logout(request):
    if 'avalon_id' in request.session:
        try:
            helper.playerList.remove(User.objects.get(id=request.session['avalon_id']).displayname)
            helper.avalonIdList.remove(request.session['avalon_id'])
        except:
            pass
        del request.session['avalon_id']
    return HttpResponseRedirect('/avalonol/login/')

def hall(request):
    if 'avalon_id' in request.session:
        user = User.objects.get(id = request.session['avalon_id'])
        if user.displayname not in helper.playerList:
            helper.playerList.append(user.displayname)
            helper.avalonIdList.append(user.id)
        else:
            pass
        return render(request,'avalonol/hall.html',{'user':user,'playerList':helper.playerList,'length':len(helper.playerList),'allingame':0})
    else:
        return HttpResponseRedirect('/avalonol/login/')

def players(request):
    return render(request,'avalonol/players.html',{'playerList':helper.playerList,'length':len(helper.playerList)})

def instance(request):
    if request.GET['command'] == '1':
        helper.commandback = 1
        helper.gamer = helper.avalonIdList[:]  #最终游戏玩家id单
        helper.playerList = []          #
        helper.avalonIdList = []        #清空hall内等待玩家名单
        helper.polls[helper.roundnum] = {}
    return HttpResponse(helper.commandback)

def game(request):
    if 'avalon_id' in request.session:
        if request.session['avalon_id'] in helper.gamer:
            if request.session['avalon_id'] in helper.gamermap:
                message = '你回到了游戏中。'
            else:
                process.opening()   #玩家实例化（安排位置与身份）
                message = '欢迎来到阿瓦隆！'
            return render(request, 'avalonol/game.html', {'message':message, 'gamer':helper.gamermap[request.session['avalon_id']],'que':helper.gamerque})
        else:
            return HttpResponse("对不起，您不在游戏中。")
    else:
        return HttpResponseRedirect('/avalonol/login/')

def message(request):
    message = process.message(request.session['avalon_id'])
    if helper.stageindex[0] == 0:
        process.superstagechange()
    elif helper.stageindex[0] == 6:
        message = "英勇的亚瑟军即将面临最后的危险！"
    elif helper.stageindex[0] == 7:
        message = "刺客趁乱挣脱开亚瑟军，给"+helper.bekilled+"了致命一击！亚瑟军胜利了！！"
    elif helper.stageindex[0] == 8:
        if helper.missionfailnum == 3:
            message = "莫德雷德阵营胜利了！！！"
        elif helper.missionsuccessnum == 3:
            message = "刺客趁乱挣脱开亚瑟军，给"+helper.bekilled+"了致命一击！莫德雷德阵营胜利了！！"
        elif helper.votefailnum == 5:
            message = "莫德雷德阵营成功地搅乱了亚瑟军的计划，胜利！！"
    return HttpResponse(message)

def stage(request):
    stageinfo = [helper.stageindex[0],helper.superstages[helper.stageindex[0]],helper.stageindex[1],helper.substages[helper.stageindex[1]]]
    return JsonResponse(stageinfo, safe=False)

def board(request):
    board = process.board()
    if request.GET['over'] == '1':
        helper.release += 1
        if helper.release == len(helper.gamer):
            process.gameover()
    return render(request, 'avalonol/board.html',{'board':board,'winlose':helper.winlose})

def notice(request):
    if len(helper.notice) > helper.noticelen:
        return HttpResponse(helper.notice[-1])
    else:
        return HttpResponse('0')

def chooseopen(request):
    if helper.stageindex[1] == 0 and helper.stageindex[0] < 6 and helper.gamermap[request.session['avalon_id']].seat == str(helper.leaderseat):
        return HttpResponse(helper.headcount[str(len(helper.gamer))][helper.missionround-1])
    elif helper.stageindex[0] == 6 and helper.gamermap[request.session['avalon_id']].role == '刺客':
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def choose(request):
    rawmembers = request.GET['members'].replace("=on","").split('&')
    helper.fortest = rawmembers
    members = []
    for e in rawmembers:
        pass
        # members.append(urllib.parse.unquote(e))
    if helper.stageindex[0] < 6:
        process.recordmember(members)
    elif helper.stageindex[0] == 6:
        process.assassinate(members[0])
    return HttpResponse(members[0])    #返回无意义

def voteopen(request):
    if helper.stageindex[1] == 1 and request.session['avalon_id'] not in helper.polls[helper.roundnum]:
        return HttpResponse('open')
    elif helper.stageindex[1] == 2 and User.objects.get(id=request.session['avalon_id']).displayname in helper.memberstodecide:
        if request.session['avalon_id'] not in helper.missions[helper.roundnum]:
            return HttpResponse('open')
        else:
            return HttpResponse('close')
    else:
        return HttpResponse('close')

def vote(request):
    if helper.stageindex[1] == 1:
        whichvote = process.counting(request.session['avalon_id'],request.GET['vote'])
    elif helper.stageindex[1] == 2:
        whichvote = process.mission(request.session['avalon_id'],request.GET['vote'])
    return HttpResponse("Nothing")    #返回无意义

def backtohall(request):
    return HttpResponseRedirect('/avalonol/hall/')

def test(request):
    ttt = request.GET['test']
    return HttpResponse(eval(ttt))
