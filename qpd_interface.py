from qpd import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

# Global variables
strategies = ['','']
entanglement = None
roundsInt = None
results = None
scoreA, scoreB = 0,0


# Window config
root = tk.Tk()
root.title("Quantum Prisoners' Dilemma Game")
root.configure(background="#046D85")
width = int(root.winfo_screenwidth() * 0.8)
height = int(root.winfo_screenheight() * 0.8)
root.geometry(f'{width}x{height}')
root.resizable(width=False, height=False)
  
# Show background image using label
bg = ImageTk.PhotoImage(Image.open("images/bg.png"))  
bgl = tk.Label(root, image = bg)
bgl.place(x = 0, y = 0)

# ~Main Frame
mf = tk.Frame(root, bd = 10, relief = tk.RAISED, bg = "#83A2A8") #LightGoldenrod4
mf.place(x=width/2, y=height/2, anchor="center")

# ~Title Frame
tf = tk.Frame(mf, bd = 5, relief = tk.SUNKEN)
tf.grid(row=0,column=0,pady=30,padx=30)

titleLabel = tk.Label(tf, text = "Quantum Prisoners' Dilemma", font = ("Helvetica", 50), fg="#223952")
titleLabel.grid(row=0,column=0,padx=10,pady=10)

# ~Control Frame
cf = tk.Frame(mf, bd = 5, relief = tk.SUNKEN, bg = "#83A2A8")
cf.grid(row=1,column=0,pady=10)

# ~Entanglement Frame
ef = tk.Frame(cf, bd = 5, relief = tk.SUNKEN)
ef.grid(row=1,column=0,pady=10)

efLabel = tk.Label(ef, text = "Pick an entanglement factor:", font = ("Helvetica", 24), fg="#223952")
efLabel.grid(row=0,column=0)

entanglement = tk.DoubleVar()
entanglementScale = tk.Scale(ef, variable = entanglement, from_ = 0, to = 100, orient = tk.HORIZONTAL, cursor = "hand2", length = 200, tickinterval=50) 
entanglementScale.grid(row=1,column=0)

# ~Strategy Frame
sf = tk.Frame(cf, bd = 5, relief = tk.SUNKEN)
sf.grid(row=2,column=0,pady=10)

strategyLabel = tk.Label(sf, text = "Pick a strategy for players A and B:", font = ("Helvetica", 24), fg="#223952")
strategyLabel.grid(row=0,column=0,columnspan=4)

# Strategy Buttons
def strategyCA() :
    strategies[0] = 'C'
    enableA()
    CA.config(state="disabled")
    canvasA.create_image(50,50, anchor=tk.CENTER, image=cooperateImage) 

def strategyDA() :
    strategies[0] = 'D'
    enableA()
    DA.config(state="disabled")
    canvasA.create_image(50,50, anchor=tk.CENTER, image=defectImage) 

def strategyQA() :
    strategies[0] = 'Q'
    enableA()
    QA.config(state="disabled")
    canvasA.create_image(50,50, anchor=tk.CENTER, image=quantumImage) 

def strategyCB() :
    strategies[1] = 'C'
    enableB()
    CB.config(state="disabled")
    canvasB.create_image(50,50, anchor=tk.CENTER, image=cooperateImage) 

def strategyDB() :
    strategies[1] = 'D'
    enableB()
    DB.config(state="disabled")
    canvasB.create_image(50,50, anchor=tk.CENTER, image=defectImage) 

def strategyQB() :
    strategies[1] = 'Q'
    enableB()
    QB.config(state="disabled")
    canvasB.create_image(50,50, anchor=tk.CENTER, image=quantumImage) 

def enableA() : # Enable all of Player A's strategy buttons
    CA.config(state="normal")
    DA.config(state="normal")
    QA.config(state="normal")

def enableB() : # Enable all of Player B's strategy buttons
    CB.config(state="normal")
    DB.config(state="normal")
    QB.config(state="normal")

# Create all strategy buttons
CA = tk.Button(sf, text ="Cooperate", command = strategyCA)
CA.grid(row=1,column=1)

DA = tk.Button(sf, text ="Defect", command = strategyDA)
DA.grid(row=2,column=1)

QA = tk.Button(sf, text ="Quantum", command = strategyQA)
QA.grid(row=3,column=1)

CB = tk.Button(sf, text ="Cooperate", command = strategyCB)
CB.grid(row=1,column=2)

DB = tk.Button(sf, text ="Defect", command = strategyDB)
DB.grid(row=2,column=2)

QB = tk.Button(sf, text ="Quantum", command = strategyQB)
QB.grid(row=3,column=2)

# Create image displays for selected strategies
canvasA = tk.Canvas(sf, width = 100, height = 100)      
canvasA.grid(row=1,column=0,rowspan=3)

canvasB = tk.Canvas(sf, width = 100, height = 100)      
canvasB.grid(row=1,column=3,rowspan=3)

cooperateImage = ImageTk.PhotoImage(Image.open("images/cop.png"))      
defectImage = ImageTk.PhotoImage(Image.open("images/def.png"))    
quantumImage = ImageTk.PhotoImage(Image.open("images/quan.png"))    


# ~Final Frame
ff = tk.Frame(cf, bd = 5, relief = tk.SUNKEN)
ff.grid(row=3,column=0,pady=10)

roundsLabel = tk.Label(ff, text = "Pick the number of rounds you would like to play for:", font = ("Helvetica", 24), fg="#223952")
roundsLabel.grid(row=0,column=0,columnspan=2)

roundsStringVar = tk.StringVar()
roundsSpinbox = ttk.Spinbox(ff, from_=0, to=10, textvariable=roundsStringVar) # , command=record
roundsSpinbox.grid(row=1,column=0)



def submitGame() :
    global scoreA, scoreB # Stores the total scores of both players

    print("ROUNDS:", roundsStringVar.get())
    roundsInt = int(roundsStringVar.get()) # Integer number of rounds taken from spinbox

    if roundsInt > 0:

        roundsSpinbox.config(state="disabled")
        entanglementScale.config(state="disabled")

        # Runs quantum game using quantum circuit defined in QPD.py and returns score results
        results = QPD(strategies[0], strategies[1], (entanglement.get() / 100) * (np.pi / 2))
        
        print(results)
        resultsLabel.config(text=str(results))

        # Appends scores to the total
        scoreA += round(results[0], 2)
        scoreB += round(results[1], 2)
        scoreA = round(scoreA, 2)
        scoreB = round(scoreB, 2)

        resultsLabelTotal.config(text=f"{scoreA}, {scoreB}")

        roundsInt -= 1
        roundsStringVar.set(str(roundsInt)) # Updates spinbox

    if roundsInt <= 0:

        print(f"Player A's total reward is: {scoreA}")
        print(f"Player B's total reward is: {scoreB}")

        resultsLabelTotal.config(text=f"{scoreA}, {scoreB}")

        scoreA, scoreB = 0,0

        roundsSpinbox.config(state="normal")
        entanglementScale.config(state="normal")

submitButton = tk.Button(ff, text ="Submit", command = submitGame)
submitButton.grid(row=1,column=1)

# ~Results Frame
rf = tk.Frame(mf, bd = 5, relief = tk.SUNKEN, bg = "#83A2A8")
rf.grid(row=2,column=0,pady=10)

resultsTitleLabel = tk.Label(rf, text = "Results of this game:", font = ("Helvetica", 24), fg="#223952")
resultsTitleLabel.grid(row=0,column=0)

resultsLabel = tk.Label(rf, text = str(results), font = ("Helvetica", 24), fg="#223952")
resultsLabel.grid(row=1,column=0)

resultsTitleLabelTotal = tk.Label(rf, text = "Total result:", font = ("Helvetica", 24), fg="#223952")
resultsTitleLabelTotal.grid(row=0,column=1)

resultsLabelTotal = tk.Label(rf, text = f"{scoreA}, {scoreB}", font = ("Helvetica", 24), fg="#223952")
resultsLabelTotal.grid(row=1,column=1)

root.mainloop()