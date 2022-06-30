from flask import Flask, render_template,request,session
from datetime import timedelta

from regex import B

app = Flask(__name__)

app.secret_key = 'test'
app.permanent_session_lifetime = timedelta(minutes=300)


class Billcount:
  def __init__(self,
               bill_1k,
               bill_10k,
               bill_5k
               ):
    self.bill_1k =bill_1k
    self.bill_10k = bill_10k
    self.bill_5k = bill_5k
    self.sum = bill_1k* 1000 + bill_10k * 10000 + bill_5k * 5000

# 金庫総額
total_safe = 1500000

# 営業セット金
set_money = 1000000

@app.route("/",methods=["get"])
def index():
  return render_template ("index.html")
        
@app.route("/slot_calc",methods=["POST"])
def calc():
  slot_safeNums = ["sa", "sb"]
  bill_types = ["_1k","_10k","_5k" ]
  
  for slot_safeNum in slot_safeNums:
    bill_1k = int(request.form[slot_safeNum + "_1k"])
    bill_10k = int(request.form[slot_safeNum + "_10k"])
    bill_5k  = int(request.form[slot_safeNum + "_5k"])
    globals()[slot_safeNum] = Billcount(bill_1k, bill_10k, bill_5k)
    
    session[slot_safeNum + "_1k"] = bill_1k
    session[slot_safeNum + "_10k"] = bill_10k
    session[slot_safeNum + "_5k"] = bill_5k
    
  slot_all = int(request.form["slot_all"])
  session["slot_all"] = slot_all
  
  slot_sum = 0
  
  slot_sumNums = [sa.sum, sb.sum]
  for slot_sumNum in slot_sumNums:
    slot_sum += slot_sumNum
  return render_template ("slot_calc.html",
                          slot_all = slot_all,
                          slot_sum = slot_sum,
                          form_data = session,
                          sa = sa,
                          sb = sb
                          ) 

@app.route("/pachi_calc",methods=["POST"])   
def pachi_calc():
  pachi_safeNums = ["p1","p2","p3","p4","p5",
                    "p6","p7","p8","p9","p10"]
  for pachi_safeNum in pachi_safeNums:
    bill_1k = int(request.form[pachi_safeNum + "_1k"])
    bill_10k = int(request.form[pachi_safeNum + "_10k"])
    bill_5k = int(request.form[pachi_safeNum + "_5k"])
    globals()[pachi_safeNum] = Billcount(bill_1k, bill_10k, bill_5k)
    session[pachi_safeNum + "_1k"] = bill_1k
    session[pachi_safeNum + "_10k"] = bill_10k
    session[pachi_safeNum + "_5k"] = bill_5k
  pachi_all = int(request.form["pachi_all"])
  session["pachi_all"] = pachi_all
  
  pachi_sum = 0
  pachi_sumNums = [p1.sum, p2.sum, p3.sum, p4.sum, p5.sum,
                   p6.sum, p7.sum, p8.sum, p9.sum, p10.sum
                   ]
  for pachi_sumNum in pachi_sumNums:
    pachi_sum += pachi_sumNum
    
  return render_template ("pachi_calc.html",
                          pachi_sum = pachi_sum,
                          pachi_all = pachi_all,
                          form_data = session,
                          p1 = p1, p2 = p2, p3 = p3,
                          p4 = p4, p5 = p5, p6 = p6,
                          p7 = p7, p8 = p8, p9 = p9,
                          p10 = p10
                          ) 


@app.route("/seisan_calc",methods=["POST"])
def seisan_calc():    
  seisan_1k = int(request.form["seisan_1k"])
  seisan_500 = int(request.form["seisan_500"])
  seisan_100 = int(request.form["seisan_100"])
  seisan_sum = seisan_1k * 1000 + seisan_500 * 500 + seisan_100 * 100
  seisan_all = int(request.form["seisan_all"])
  session["seisan_1k"] = seisan_1k
  session["seisan_500"] = seisan_500
  session["seisan_100"] = seisan_100
  session["seisan_all"] = seisan_all
  session["seisan_sum"] = seisan_sum
   
  return render_template ("seisan_calc.html")

@app.route("/input_value", methods=["POST"])
def input_value():
  d = {"1":1}
  all_sum = 0
  sums = ["slot_all", "pachi_all", "seisan_sum"]
  for sum in sums:
    all_sum += session[sum]
  session["all_sum"] = all_sum
  hall_com = int(request.form["hall_com"])
  session["hall_com"] = hall_com
  if all_sum - set_money == hall_com:
    chk = True
    money =  all_sum - set_money
    bills = [10000,5000,1000,500,100]
    for bill in bills:
      num_sheet = money // bill
      money %= bill
      d[bill] = num_sheet
  else:
    chk = False
  return render_template("input_value.html", chk = chk, d = d)

@app.route("/safe_margin_calc", methods=["POST"])
def safe_margin_calc():
  var_list = ["safe_10k", "safe_5k", "safe_1k", "safe_500",
           "safe_100","y_margin", "t_margin","add_margin",
           "margin_10k", "margin_1k", "margin_100"
           ]

  for i in range(len(var_list)):
    session[var_list[i]] = int(request.form[var_list[i]])

  #locals を使うとあとで参照していない　y_margin t_margin add_margin しか変数作成されないし not defindが出る globalsでいけるけど却下
    
  # for list in var_list:
  #   locals()[list] = int(request.form[list])
  #   session[list] = int(request.form[list])
  
  # for i in range(len(var_list)):
  #   var_name = var_list[i]
  #   exec("{} = 1".format(var_name))

  # for i in range(len(var_list)):
  #  var_name = var_list[i]
  #  exec("%s = %d" % (var_name,100))
    
  safe_10k = session["safe_10k"] + 10000
  safe_5k = session["safe_5k"] + 10000
  safe_1k = session["safe_1k"] + 10000
  safe_500 *= 500
  safe_100 *= 100  
  safe_lists = [safe_10k, safe_5k, safe_1k,
                safe_500, safe_100
                ]
  for safe_list in safe_lists:
    safe_all += safe_list
  
  margin_10k *= 10000
  margin_1k *= 1000
  margin_100 *= 100 
  margin_lists = [margin_10k, margin_1k, margin_100] 
  for margin_list in margin_lists:
    margin_all += margin_list
    
  chk = True if safe_all == total_safe and y_margin + add_margin - margin_all == t_margin else False
    
  # safe_5k = int(request.form["safe_5k"])
  # safe_1k = int(request.form["safe_1k"])
  # safe_500 = int(request.form["safe_500"])
  # safe_100 = int(request.form["safe_100"])
  # y_margin = int(request.form["y_margin"])
  # margin_10k = int(request.form["margin_10k"])
  # margin_1k = int(request.form["margin_1k"])
  # margin_100 = int(request.form["margin_100"])
  
  # safe_all = safe_10k * 10000 + safe_
  
  return render_template("safe_margin_calc", chk = chk)
  
  
@app.route("/clear", methods=["POST"])
def clear():
  session.clear()
  return render_template("index.html")
  
# sessionクリアボタン　session無限

 
if __name__ == '__main__':
	app.run()