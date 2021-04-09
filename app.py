#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 01:15:12 2021

@author: adsorbentkarma
"""
from flask import Flask,request,redirect,render_template
import json
from pymongo import MongoClient
from datetime import datetime
mongo =  MongoClient("mongodb+srv://#:#@cluster0.vg8zq.mongodb.net/?retryWrites=true&w=majority")
db = mongo["#"]
app=Flask(__name__)
@app.route("/")
def home():
    try:
        data = db.Github.find()
        fenddata = []
        for x in data:
            tl=[]
            for i,j in x.items():
                if i == "request_id":
                    tl.append(j)
                elif i=="author":
                    tl.append(j)
                elif i=="action":
                    tl.append(j)
                elif i=="from_branch":
                    tl.append(j)
                elif i=="to_branch":
                    tl.append(j)
                elif i=="time":
                    d=j.split("T")
                    print(d)
                    date = datetime.strptime(d[0], '%Y-%m-%d')
                    month=date.strftime("%B")
                    weekday=date.strftime("%A")
                    day=date.strftime("%d")
                    year=date.strftime("%Y")
                    s= weekday+", "+day+", "+month+", "+year
                    t=d[1].split(":")
                    if int(t[0])<12:
                        s=s+" "+d[1]+"AM"
                    else:
                        s=s+" "+d[1]+"PM"
                    tl.append(s)
            if tl[2]=="Push":
                b=tl[4].split("/")
                s1=tl[1]+" pushed to "+b[-1]+" on "+tl[-1]
            if tl[2]=="Pull_Request":
                s1=tl[1]+" submitted a pull request from "+tl[3]+" to "+tl[4]+" on "+tl[-1]
            if tl[2]=="Merge":
                b=tl[4].split("/")
                o=tl[3].split("/")
                s1=tl[1]+" merged branch "+o[-1]+" to "+b[-1]+" on "+tl[-1]
            tl.append(s1)
            fenddata.append(tuple(tl))
        return render_template("home.html",d=fenddata)
    except:
        return render_template("home.html",d=[])
        

@app.route('/hookactivity',methods=['GET','POST'])
def webhooks():
    #print(request.json)
    data = request.json
    typ=data.get("pull_request","Push")
    if typ=="Push":
        branch=data['ref']
        other_repo=data['base_ref']
        a=data['head_commit']
        author=data["pusher"]
        author_name=author['name']
        i_d= a["id"]
        time=a["timestamp"]
        if other_repo == None:
            db.Github.insert_one({"request_id":i_d ,'author':author_name,'action':typ,"from_branch":other_repo,"to_branch":branch,"time":time})
        else:
            db.Github.insert_one({"request_id":i_d ,'author':author_name,'action':"Merge","from_branch":other_repo,"to_branch":branch,"time":time})
    
    else:
        i_d=typ["id"]
        a=typ["user"]
        author=a["login"]
        action="Pull_Request"
        b=typ["head"]
        branch=b["ref"]
        othb=typ["base"]
        other_repo=othb['ref']
        time=typ["created_at"]
        db.Github.insert_one({"request_id":i_d ,'author':author,'action':action,"from_branch":branch,"to_branch":other_repo,"time":time})
    return json.dumps({"Status":"OK"})

if __name__=='__main__':
    app.run(port=2729,debug=True)
    
