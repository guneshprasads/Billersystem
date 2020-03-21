from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId     
from pymongo import MongoClient    
import os    
import logging
import time
import pdb

    
app = Flask(__name__)    
title = "Biller system"    
heading = "Biller system"    
    
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb    
todos = db.todo    
    
def redirect_url():    
    return request.args.get('next')

@app.route("/") 
@app.route("/create")
def create():    
    todos_l = todos.find()
    a1="active"    
    return render_template('create.html',a1=a1,todos=todos_l,t=title,h=heading)

  
@app.route("/list")
def lists ():    
    todos_l = todos.find()    
    a1="active"

    print(todos_l)
    return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)
  
   
@app.route("/uncompleted")    
def tasks ():    
    todos_l = todos.find({"done":"no"})    
    a2="active"    
    return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)    
  
  
@app.route("/completed")    
def completed ():        
    todos_l = todos.find({"done":"yes"})    
    a3="active"    
    return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)    
  
@app.route("/done")    
def done ():    
    #Done-or-not ICON    
    id=request.values.get("_id")    
    task=todos.find({"_id":ObjectId(id)})    
    if(task[0]["done"]=="yes"):    
        todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})    
    else:    
        todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})    
    redir=redirect_url()        
    
    return redirect(redir)    
  
@app.route("/action", methods=['POST'])    
def action ():    
    name=request.values.get("name")    
    phonenumber=request.values.get("phonenumber")
    amount=request.values.get("Amount")

    bills = [
        {
            "amount": amount,
            "created_on": int(time.time())
        }
    ]
    todos.insert({ "name":name, "phonenumber":phonenumber, "bills":bills, "done":"no"})
    return redirect("/create")
  
@app.route("/remove")    
def remove ():    
    key=request.values.get("_id")    
    todos.remove({"_id":ObjectId(key)})    
    return redirect("/list")    
  
@app.route("/update")    
def update ():    
    id=request.values.get("_id")    
    task=todos.find({"_id":ObjectId(id)})    
    return render_template('update.html',tasks=task,h=heading,t=title)
  
@app.route("/action3", methods=['POST'])    
def action3 ():
    amount=request.values.get("amount")
    reciept_id=request.values.get("_id")

    task=todos.find_one({"_id":ObjectId(reciept_id)})

    billObject = {
        "name": request.values.get("name"),
        "phonenumber": request.values.get("phonenumber"),
        "bills": task["bills"],
        "done": task["done"]
    }

    if "bills" in task and not len(task["bills"]):
        return render_template("/completed.html", billObject=billObject, reciept_id=reciept_id)

    reciept_amout = int(task["bills"][0]["amount"]) - int(amount)

    if reciept_amout <= 0:
        billObject["bills"] = []
        billObject["done"] = "yes"
    else:
        billObject["bills"][0]["amount"] = str(reciept_amout)

    todos.update({"_id":ObjectId(reciept_id)}, {'$set':{"bills": billObject["bills"], "done": billObject["done"]}})

    return render_template("/completed.html", billObject=billObject, reciept_id=reciept_id, t=title,h=heading)
  
@app.route("/search", methods=['GET'])    
def search():    
    key=request.values.get("search_query")
    refer=request.values.get("refer")
    todos_l = todos.find({refer:key})

    print(todos_l)
    return render_template('searchlist.html',todos=todos_l,t=title,h=heading)    

 

    
if __name__ == "__main__":    
    
    app.run(debug=True)

