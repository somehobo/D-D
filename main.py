from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField,BooleanField,SelectField,RadioField
from wtforms.validators import DataRequired
from random import randint
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# This is the object that manipulate the data. The data is a Class Attribute named probsandsols.
# The data is a list of problems and sultions.
# The data is a list of dictionaries. Each dictionary is one problem or one solutionself.
# Each dictionary has the same elements.
# You should put what ever values you want here to start your application
class ProbSol:
    isTheSol = False
    currentBaddieNumber = 1
    currentSolNumber = 1
    probsandsols = [
#MARC AND MAX
              {
                 "isSolution":True,
                 "name":"Short Sword",
                 "attribute1":"Short",
                 "attribute2":"Slash",
                 "attribute3":"Steel",
                 "imgurl":"https://vignette.wikia.nocookie.net/unrealworld/images/2/22/5492745162_cb11c44d84_z.jpg/revision/latest?cb=20140630074359",
                 "isShown":False
              },
              {
                 "isSolution":True,
                 "name":"Spike Gloves",
                 "attribute1":"Close",
                 "attribute2":"Blunt",
                 "attribute3":"Steel",
                 "imgurl":"data:image/jpeg;base64,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",
                 "isShown":False
              },
              {
                 "isSolution":True,
                 "name":"Baton",
                 "attribute1":"Close",
                 "attribute2":"Blunt",
                 "attribute3":"Wood",
                 "imgurl":"https://www.karatemart.com/images/products/large/wooden-baton.jpg",
                 "isShown":False
              },
              {
                 "isSolution":True,
                 "name":"Diamond shiv",
                 "attribute1":"Close",
                 "attribute2":"Piercing",
                 "attribute3":"Diamond",
                 "imgurl":"https://i.etsystatic.com/14765525/d/il/fe8e02/1407637834/il_340x270.1407637834_e7lp.jpg?version=0",
                 "isShown":False
              },
              {
                 "isSolution":True,
                 "name":"Short Silver Sword",
                 "attribute1":"Short",
                 "attribute2":"Slash",
                 "attribute3":"Silver",
                 "imgurl":"data:image/jpeg;base64,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",
                 "isShown":False
              },
              {
                 "isSolution":True,
                 "name":"Diamond Wand",
                 "attribute1":"Short",
                 "attribute2":"Magic",
                 "attribute3":"Diamond",
                 "imgurl":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSz5NIYj6rFpg03CPx5My2ZJMTP6JCF9YcbohqegDUpZY430838Kw",
                 "isShown":False
              },
              {
                 "isSolution":True,
                 "name":"Stick",
                 "attribute1":"Short",
                 "attribute2":"Blunt",
                 "attribute3":"Wood",
                 "imgurl":"data:image/jpeg;base64,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",
                 "isShown":False
              },
              {
                 "isSolution":True,
                 "name":"Claymore",
                 "attribute1":"Medium",
                 "attribute2":"Slash",
                 "attribute3":"Steel",
                 "imgurl":"https://cdn.reliks.com/products/2512/750x280/1.jpg",
                 "isShown":False
              },
              {
                 "isSolution":True,
                 "name":"Diamond Lance",
                 "attribute1":"Long",
                 "attribute2":"Peircing",
                 "attribute3":"Diamond",
                 "imgurl":"https://s3.amazonaws.com/bncore/wp-content/uploads/2017/07/Lance-Diamond-pointing-1260x800.jpg",
                 "isShown":False
              },
               {
                  "isSolution":True,
                  "name":"Magic Staff",
                  "attribute1":"Long",
                  "attribute2":"Magic",
                  "attribute3":"Wood",
                  "imgurl":"https://media-waterdeep.cursecdn.com/avatars/thumbnails/7/426/1000/1000/636284770809045580.jpeg",
                  "isShown":False
               },
            {
                "isSolution":True,
                "name":"Bow",
                "attribute1":"Long",
                "attribute2":"Peircing",
                "attribute3":"Wood",
                "imgurl":"https://vignette.wikia.nocookie.net/dark-heresy-rp/images/f/f4/Longbow.jpg/revision/latest?cb=20141217012807",
                "isShown":False
             },
             {
                "isSolution":True,
                "name":"Soldier's Broadsword",
                "attribute1":"Medium",
                "attribute2":"Slash",
                "attribute3":"Silver",
                "imgurl":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOfuZPt7SMirfFndpCVq8j4fHEv0AHfIUbkDHwSfZYWZYlBuuLcQ",
                "isShown":False
             },
             {
                "isSolution":True,
                "name":"Silver Knuckles",
                "attribute1":"Close",
                "attribute2":"Blunt",
                "attribute3":"Silver",
                "imgurl":"https://qph.fs.quoracdn.net/main-qimg-c6ea301ce8517b808f15062267858dcd",
                "isShown":False
             },
             {
                "isSolution":True,
                "name":"Wooden Folding Chair",
                "attribute1":"Medium",
                "attribute2":"Blunt",
                "attribute3":"Wood",
                "imgurl":"https://thumbs1.ebaystatic.com/d/l225/m/m5LMEiVYyDP9p1J_IPlhsSQ.jpg",
                "isShown":False
             },
             {
                "isSolution":True,
                "name":"Gat (pakin heat)",
                "attribute1":"Long",
                "attribute2":"Piercing",
                "attribute3":"Steel",
                "imgurl":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/GatUncockedLeft.JPG/300px-GatUncockedLeft.JPG",
                "isShown":False
             },
             {
                "isSolution":True,
                "name":"Chrome Gat (Packin Silver Heat)",
                "attribute1":"Long",
                "attribute2":"Piercing",
                "attribute3":"Silver",
                "imgurl":"https://66.media.tumblr.com/2b49d66fc2d89bcf5b2707543889564f/tumblr_oyh9wsIErb1tevf1do1_500.jpg",
                "isShown":False
             },
              {
                 "isSolution":True,
                 "name":"Boomerang",
                 "attribute1":"Long",
                 "attribute2":"Slash",
                 "attribute3":"Wood",
                 "imgurl":"https://cdn.shopify.com/s/files/1/1446/8412/products/joe-boom_2048x.jpg?v=1510135200",
                 "isShown":False
              },
             {
                "isSolution":True,
                "name":"Mace",
                "attribute1":"Medium",
                "attribute2":"Blunt",
                "attribute3":"Diamond",
                "imgurl":"http://www.poxpulse.com/images/large/diamond_mace_270x310.jpg",
                "isShown":False
             },
            {
                "isSolution":False,
                "name":"Troll",
                "attribute1":"Long",
                "attribute2":"Peircing",
                "attribute3":"Diamond",
                "imgurl":"https://www.welivesecurity.com/wp-content/uploads/2014/10/internettroll.png",
                "isShown":False
             },
             {
                 "isSolution":False,
                 "name":"Unholy Knight",
                 "attribute1":"Short",
                 "attribute2":"Blunt",
                 "attribute3":"Steel",
                 "imgurl":"http://suptg.thisisnotatrueending.com/archive/5315595/images/1249245956402.jpg",
                 "isShown":False
              },
             {
                "isSolution":False,
                "name":"Dragon",
                "attribute1":"Medium",
                "attribute2":"Magic",
                "attribute3":"Silver",
                "imgurl":"https://media.wired.com/photos/5ada3a2c1e66870735eada27/master/pass/DragonPasswordFINAL.jpg",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"T-Rex",
                "attribute1":"Long",
                "attribute2":"Slash",
                "attribute3":"Wood",
                "imgurl":"http://en.es-static.us/upl/2018/06/Screen-Shot-2018-06-27-at-2.30.15-PM.png",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Ghoul",
                "attribute1":"Short",
                "attribute2":"Slash",
                "attribute3":"Steel",
                "imgurl":"https://media-waterdeep.cursecdn.com/avatars/thumbnails/14/483/1000/1000/636364323937041514.png",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Giant",
                "attribute1":"Close",
                "attribute2":"Piercing",
                "attribute3":"Silver",
                "imgurl":"https://vignette.wikia.nocookie.net/harrypotter/images/4/4f/PottermoreGiantClutchingDeerConceptArt_-_cropped.png/revision/latest?cb=20151216132944",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Goblin",
                "attribute1":"Medium",
                "attribute2":"Slash",
                "attribute3":"Wood",
                "imgurl":"https://i.kinja-img.com/gawker-media/image/upload/s--hDW7QL00--/c_scale,f_auto,fl_progressive,q_80,w_800/hbfyp85afskxjiovmypg.png",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Lych",
                "attribute1":"Medium",
                "attribute2":"Magic",
                "attribute3":"Diamond",
                "imgurl":"https://cdnb.artstation.com/p/assets/images/images/002/855/869/large/daniel-rosa-lichking.jpg?1466511765",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Medusa",
                "attribute1":"Short",
                "attribute2":"Slash",
                "attribute3":"Silver",
                "imgurl":"https://i.ytimg.com/vi/Q9pr2Xxaagw/maxresdefault.jpg",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Minataur",
                "attribute1":"Medium",
                "attribute2":"Slash",
                "attribute3":"Steel",
                "imgurl":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4kW0u8r7PafEHYw85lLxPChWcu2tSiqeYs_f9fBRMqsZd9fpl9w",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Giant Spider",
                "attribute1":"Long",
                "attribute2":"Piercing",
                "attribute3":"Wood",
                "imgurl":"https://vignette.wikia.nocookie.net/gamelore/images/d/d6/Giant_Spider_%286ED%29.jpg/revision/latest?cb=20140911120433",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Vampire",
                "attribute1":"Close",
                "attribute2":"Piercing",
                "attribute3":"Wood",
                "imgurl":"https://vignette.wikia.nocookie.net/twilightsaga/images/8/8a/Edward-376194_429619737081258_1836140990_n.jpg/revision/latest?cb=20120728050624",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Werewolf",
                "attribute1":"Long",
                "attribute2":"Piercing",
                "attribute3":"Silver",
                "imgurl":"https://pixel.nymag.com/imgs/daily/vulture/2012/11/15/15-taylor-lautner.w700.h700.jpg",
                "isShown":False
             },
             {
                "isSolution":False,
                "name":"Zombie",
                "attribute1":"Short",
                "attribute2":"Blunt",
                "attribute3":"Wood",
                "imgurl":"https://i1.wp.com/zombieportraits.com/wp-content/uploads/2016/06/zombie-art-minions.jpg?fit=645%2C500",
                "isShown":False
             },
              {
                 "isSolution":False,
                 "name":"Ellery",
                 "attribute1":"Long",
                 "attribute2":"Blunt",
                 "attribute3":"Silver",
                 "imgurl":"https://www.bodybuilding.com/images/2017/september/the-worlds-oldest-bodybuilder-still-competes-to-win-tall-v2.jpg",
                 "isShown":False
              },
               {
                  "isSolution":False,
                  "name":"Nolan",
                  "attribute1":"Medium",
                  "attribute2":"Slash",
                  "attribute3":"Diamond",
                  "imgurl":"https://afinde-production.s3.amazonaws.com/uploads/88f13694-a5c1-42f5-a125-19cb211fa612.png",
                  "isShown":False
               },
             {
                "isSolution":False,
                "name":"Arch Demon",
                "attribute1":"Medium",
                "attribute2":"Piercing",
                "attribute3":"Diamond",
                "imgurl":"https://vignette.wikia.nocookie.net/the-demonic-paradise/images/e/e9/T6d16a94d6df6771c20505226868ca244--diablo-video-game-diablo-game.jpg/revision/latest?cb=20171213004515",
                "isShown":False
             }
        ]

    # This class does not need an init function so I just put a pass here.
    def __init__(self):
        pass

    def newProbSol(isSolution,name,attribute1,attribute2,attribute3,imgurl):
        ProbSol.probsandsols.append({
            "isSolution":isSolution,
            "name":name,
            "attribute1":attribute1,
            "attribute2":attribute2,
            "attribute3":attribute3,
            "imgurl":imgurl
        })
        return ProbSol.probsandsols[-1]

    def getProbSol(idxNum):
        return ProbSol.probsandsols[int(idxNum)]

    def editProbSol(idxNum,isSolution,name,attribute1,attribute2,attribute3,imgurl):
        # This creates the values that prepopulates the form
        ProbSol.probsandsols[int(idxNum)]['name'] = name
        ProbSol.probsandsols[int(idxNum)]['isSolution'] = isSolution
        ProbSol.probsandsols[int(idxNum)]['attribute1'] = attribute1
        ProbSol.probsandsols[int(idxNum)]['attribute2'] = attribute2
        ProbSol.probsandsols[int(idxNum)]['attribute3'] = attribute3
        ProbSol.probsandsols[int(idxNum)]['imgurl'] = imgurl
        return ProbSol.probsandsols[int(idxNum)]

    def deleteProbSol(idxNum):
        del ProbSol.probsandsols[int(idxNum)]
        return f"Deleted index {idxNum}"

    def getAllSolutions():
        solutions = []
        for solution in ProbSol.probsandsols:
            if solution['isSolution']:
                solutions.append(solution)
        return solutions

    def getAllProblems():
        problems = []
        for problem in ProbSol.probsandsols:
            if not problem['isSolution']:
                problems.append(problem)
        return problems

    def getAllProbSols():
        return ProbSol.probsandsols
#ELLERY
    def randomProb():
        problems = ProbSol.getAllProblems()
        num = randint(0,len(problems))-1
        session['randProb'] = problems[num]
        ProbSol.currentBaddieNumber = num
        ProbSol.randomSol()
        return problems[num]


    def randomSol():
        temp = 0
        while(temp < len(ProbSol.probsandsols)-1):
            ProbSol.probsandsols[temp]['isShown'] = False
            temp += 1
        solutions = ProbSol.getAllSolutions()

        num = randint(0,len(solutions))-1
        while(ProbSol.probsandsols[num]['isSolution'] == False):
            num = randint(0,len(solutions))-1

        num2 = randint(0,len(solutions))-1
        while(num == num2 or ProbSol.probsandsols[num2]['isSolution'] == False):
            num2 = randint(0,len(solutions))-1

        num3 = randint(0,len(solutions))-1
        while(num3 == num2 or num3 == num or ProbSol.probsandsols[num3]['isSolution'] == False):
            num3 = randint(0,len(solutions))-1
        #ProbSol[num].isShown = True
        coin = random.randint(1,2)
        print(coin)

        if(coin == 1):
            while((ProbSol.probsandsols[num]['attribute2'] != session['randProb']['attribute2'] and ProbSol.probsandsols[num2]['attribute2'] != session['randProb']['attribute2'] and ProbSol.probsandsols[num3]['attribute2'] != session['randProb']['attribute2']) ):
                temp = 0
                print("trying1")
                while(temp < len(ProbSol.probsandsols)-1):
                    ProbSol.probsandsols[temp]['isShown'] = False
                    temp += 1
                solutions = ProbSol.getAllSolutions()

                num = randint(0,len(solutions))-1
                while(ProbSol.probsandsols[num]['isSolution'] == False):
                    num = randint(0,len(solutions))-1

                num2 = randint(0,len(solutions))-1
                while(num == num2 or ProbSol.probsandsols[num2]['isSolution'] == False):
                    num2 = randint(0,len(solutions))-1

                num3 = randint(0,len(solutions))-1
                while(num3 == num2 or num3 == num or ProbSol.probsandsols[num3]['isSolution'] == False):
                    num3 = randint(0,len(solutions))-1
                #ProbSol[num].isShown = True
        else:
            while(not((ProbSol.probsandsols[num]['attribute1'] == session['randProb']['attribute1'] and
                ProbSol.probsandsols[num]['attribute3'] == session['randProb']['attribute3']) or
                (ProbSol.probsandsols[num2]['attribute1'] == session['randProb']['attribute1'] and
                    ProbSol.probsandsols[num2]['attribute3'] == session['randProb']['attribute3']) or
                    (ProbSol.probsandsols[num3]['attribute1'] == session['randProb']['attribute1'] and
                        ProbSol.probsandsols[num3]['attribute3'] == session['randProb']['attribute3']))):
                temp = 0
                print("trying2")
                while(temp < len(ProbSol.probsandsols)-1):
                    ProbSol.probsandsols[temp]['isShown'] = False
                    temp += 1
                    solutions = ProbSol.getAllSolutions()

                    num = randint(0,len(solutions))-1
                    while(ProbSol.probsandsols[num]['isSolution'] == False):
                        num = randint(0,len(solutions))-1

                    num2 = randint(0,len(solutions))-1
                    while(num == num2 or ProbSol.probsandsols[num2]['isSolution'] == False):
                        num2 = randint(0,len(solutions))-1

                    num3 = randint(0,len(solutions))-1
                    while(num3 == num2 or num3 == num or ProbSol.probsandsols[num3]['isSolution'] == False):
                        num3 = randint(0,len(solutions))-1



        ProbSol.probsandsols[num]['isShown'] = True
        ProbSol.probsandsols[num2]['isShown'] = True
        ProbSol.probsandsols[num3]['isShown'] = True
        return solutions[num]

#NOLAN
class ProbSolForm(FlaskForm):
    some_tuples_list = ['bal']
    isSolution = BooleanField('This is a solution and not a problem:')
    name = StringField('What is the item\'s name',validators=[DataRequired()])
    imgurl = StringField('Image URL')
    attribute1 = SelectField('Attribute 1:',choices=[('Close', 'Close'), ('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long')], validators=[DataRequired()])
    attribute2 = SelectField('Attribute 2:',choices=[('Slashing', 'Slashing'), ('Peircing', 'Peircing'), ('Blunt', 'Blunt'), ('Magic', 'Magic')], validators=[DataRequired()])
    attribute3 = SelectField('Attribute 3:',choices=[('Silver', 'Silver'), ('Diamond', 'Diamond'), ('Steel', 'Steel'), ('Wood', 'Wood')], validators=[DataRequired()])
    isShown = False
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    userName = StringField('User Name: ',validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html.j2')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    form = UserForm()
    if form.validate_on_submit():
        session['userName'] = form.userName.data
    elif 'userName' in session:
        form.userName.data = session['userName']
    else:
        session['userName'] = 'No One Yet'
    return render_template('setup.html.j2',form = form,probsols = ProbSol.getAllProbSols())

@app.route('/delprobsol/<idxNum>')
def delProbSol(idxNum):
    delProbSolObj = ProbSol.deleteProbSol(int(idxNum))
    return redirect(url_for("setup"))

# This view function manages the form for editing and creating problems and solutions
@app.route('/probsolform/<idxNum>', methods=['GET', 'POST'])
def NewEdit(idxNum=100):
    # Create instance of the form.
    form = ProbSolForm()
    # This function is run because the user clicked submit AND the form is valid.
    if form.validate_on_submit():
        if int(idxNum) < 100:
            editProbSolObj = ProbSol.editProbSol(idxNum,form.isSolution.data, form.name.data, form.attribute1.data, form.attribute2.data, form.attribute3.data, form.imgurl.data)
            return redirect(url_for("setup"))
        else:
            newProbSolObj = ProbSol.newProbSol(form.isSolution.data, form.name.data, form.attribute1.data, form.attribute2.data, form.attribute3.data, form.imgurl.data)
            flash(f"You entered {form.name.label}: {form.name.data}")
            return redirect(url_for("setup"))

    #If the function is run NOT by hitting the submit button on the form
    if int(idxNum) < 100:
        editProbSolObject = ProbSol.getProbSol(idxNum)
        form.name.data = editProbSolObject['name']
        form.imgurl.data = editProbSolObject['imgurl']
        form.attribute1.data = editProbSolObject['attribute1']
        form.attribute2.data = editProbSolObject['attribute2']
        form.attribute3.data = editProbSolObject['attribute3']
        return render_template('probsolform.html.j2', form=form, idxNum=idxNum)

    return render_template('probsolform.html.j2', form=form)

@app.route('/problem')
def problem():
    return render_template('problem.html.j2',randProb = ProbSol.randomProb(), probsols = ProbSol.getAllProbSols(), randSol = ProbSol.randomSol())

@app.route('/solution/<idxNum>')
def solution(idxNum):
    ProbSol.isTheSol = False
    session['selectedSolution'] = ProbSol.getProbSol(idxNum)
    ProbSol.currentSolNumber = idxNum
    if(session['randProb']['attribute2'] == session['selectedSolution']['attribute2']):
        ProbSol.isTheSol = True
    if(session['randProb']['attribute1'] == session['selectedSolution']['attribute1'] and session['randProb']['attribute3'] == session['selectedSolution']['attribute3']):
        ProbSol.isTheSol = True
    return render_template('solution.html.j2', solution = ProbSol.getProbSol(idxNum), overProbSol = ProbSol)

if __name__ == '__main__':
    app.run(debug=True)
