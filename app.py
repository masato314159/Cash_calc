from flask import Flask, render_template,request,session
from datetime import timedelta

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
 
   


@app.route("/",methods=["get"])
def index():
  return render_template ("index.html")

        
@app.route("/slot_calc",methods=["POST"])       
def calc():
  slot_safeNums = ["sa", "sb"]

  for slot_safeNum in slot_safeNums:
    bill_1k = int(request.form[slot_safeNum + "_1k"])
    bill_10k = int(request.form[slot_safeNum + "_10k"])
    bill_5k  = int(request.form[slot_safeNum + "_5k"])
    globals()[slot_safeNum] = Billcount(bill_1k, bill_10k, bill_5k)
    
  slot_all = int(request.form["slot_all"])
  slot_sum = 0
  
  slot_sumNums = [sa.sum, sb.sum]
  for slot_sumNum in slot_sumNums:
    slot_sum += slot_sumNum
  
  # session.permanent = True
  # session["slot_sum"] = slot_sum
  # session[]
  return render_template ("slot_calc.html",slot_all = slot_all, slot_sum = slot_sum) 

@app.route("/pachi_calc",methods=["POST"])   
def pachi_calc():
  pachi_safeNums = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10"]
  for pachi_safeNum in pachi_safeNums:
    bill_1k = int(request.form[pachi_safeNum + "_1k"])
    bill_10k = int(request.form[pachi_safeNum + "_10k"])
    bill_5k = int(request.form[pachi_safeNum + "_5k"])
    globals()[pachi_safeNum] = Billcount(bill_1k, bill_10k, bill_5k)
  pachi_all = int(request.form["pachi_all"])
  
  pachi_sum = 0
  pachi_sumNums = [p1.sum, p2.sum, p3.sum, p4.sum, p5.sum,
                   p6.sum, p7.sum, p8.sum, p9.sum, p10.sum
                   ]
  for pachi_sumNum in pachi_sumNums:
    pachi_sum += pachi_sumNum
  print(pachi_sum)
  
  return render_template ("pachi_calc.html", pachi_sum = pachi_sum ,pachi_all = pachi_all) 


@app.route("/seisan_calc",methods=["POST"])
def seisan_calc():    
  seisan_1k = int(request.form["seisan_1k"])
  seisan_500 = int(request.form["seisan_500"])
  seisan_100 = int(request.form["seisan_100"])
  seisan_sum = seisan_1k * 1000 + seisan_500 * 500 + seisan_100 * 100
  seisan_all = int(request.form["seisan_all"])
  return render_template ("seisan_calc.html", seisan_sum = seisan_sum, seisan_all = seisan_all)

 
if __name__ == '__main__':
	app.run()