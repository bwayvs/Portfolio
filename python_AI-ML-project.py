import random

#Adding font color and style to a variable
X = '\033[0m'
Bold = '\033[1;36m'

#Defining variables for use in Final Stats
winEas = loseEas = tieEas = winInt = loseInt = tieInt = winHard = loseHard = tieHard = winExp = loseExp = tieExp = winspec = losespec = tiespec = 0.0

#Machine Learning Matrix

buildTMatrix = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixL = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixT = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}

n = 3
m = 3
tMatrix = [[0] * m for i in range(n)]
tMatrixL = [[0] * m for i in range(n)]
tMatrixT = [[0] * m for i in range(n)]


probabilitiesRPS = [1/3,1/3,1/3]

intro = """
Welcome to Group 1's Rock Paper Scissors! 
There are 3 modes: (1) Beginner, (2) Intermediate and (3) Expert. 
Beginner is random. Intermediate uses AI. Expert uses Machine Learning. 
To play, type in the number corresponding to the command unless it asks for a yes or no answer.
Have fun!
"""
print(Bold)
print(intro)
print(X)

#Setting up the 3 modes

def chooseMode():
  mode = 6
  try:
    mode = int(input("What Mode do you want to play in? 1: beginner, 2: intermediate or 3: expert? Enter a number \n"))
  except ValueError:
    print("you must enter an integer. \n")

  if(mode > 3):
    print ("You must enter an integer less than four. \n")
    while(mode > 3):
      try:
        mode = int(input("What Mode do you want to play in? 1: beginner, 2: intermediate or 3: expert? Enter a number. \n"))
      except ValueError:
        print("you must enter an integer. \n")
  return mode

def easyMode():
  choices = ["Rock","Paper","Scissors"]
  continuePlaying = True
  continueGame = ""
  try:
      choice = int(input("0: Rock, 1: Paper, 2: Scissors \n"))
  except ValueError:
    print("you must enter an integer. \n")
  if(choice > 2 or choice < 0):
    #print ("You must enter an integer less than three and greater than 0  \n")
    while(choice > 2 or choice < 0):
      print ("You must enter an integer less than three and greater than 0. \n")
      try:
        choice = int(input("0: Rock, 1: Paper, 2: Scissors \n"))
      except ValueError:
        print("you must enter an integer. \n")
  machineChoice = random.randint(0, 2)
  result = checkWin(choice,machineChoice,1)
  print ("You chose %s" % choices[choice])
  print ("The machine chose %s" % choices[machineChoice])
  print("You %s" % result)
  
  while(continuePlaying):
    try:
      choice = int(input("0: Rock, 1: Paper, 2: Scissors, 4: exit \n"))
    except ValueError:
      print("you must enter an integer \n")

    if((choice > 2 or choice < 0) and choice != 4):
      #print ("LINE 76 - You must enter an integer less than three and greater than or equal to 0 or choose 4 to exit.  \n")
      while((choice > 2 or choice < 0) and choice != 4):
        print ("You must enter an integer less than three and greater than or equal to 0 or choose 4 to exit.\n")
        try:
          choice = int(input("0: Rock, 1: Paper, 2: Scissors \n"))
        except ValueError:
          print("you must enter an integer. \n")
    if (choice == 4):
      print ("Thanks for Playing!")
      continuePlaying = False
    else:
      machineChoice = random.randint(0, 2)
      result = checkWin(choice,machineChoice,1)

      print ("You chose %s" % choices[choice])
      print ("The machine chose %s" % choices[machineChoice])
      print("You %s" % result)

def intermediateMode():
	choices = ["Rock", "Paper", "Scissors"]
	continuePlaying = True
	continueGame = ""
	prevChoice = ""
	prevMachineChoice = ""
	result = ""
	streak = 0
	won = 0
	alt = 0
	numoff = 0
	choice = 3

	try:
		choice = int(input("0: Rock, 1: Paper, 2: Scissors \n"))
	except ValueError:
		print("you must enter an integer. \n")

	if (choice > 2 or choice < 0):
		print(
		    "You must enter an integer less than three and greater than or equal to 0. \n")
		while (choice > 2 or choice < 0):
			try:
				choice = int(input("0: Rock, 1: Paper, 2: Scissors \n"))
			except ValueError:
				print("you must enter an integer. \n")
	machineChoice = random.randint(0, 2)
	result = checkWin(choice, machineChoice, 2)
	if (result == "Win!"):
		won += 1
	else:
		numoff += 1
		if (numoff == 3):
			won -= 3
			numoff = 0
		if (won < 0):
			won = 0

	print("You chose %s" % choices[choice])
	print("The machine chose %s" % choices[machineChoice])
	print("You %s" % result)

	prevChoice = choice
	prevMachineChoice = machineChoice
	streak += 1

	while (continuePlaying):
		try:
			choice = int(input("0: Rock, 1: Paper, 2: Scissors, 4: exit \n"))
		except ValueError:
			print("you must enter an integer. \n")

		if ((choice > 2 or choice < 0) and choice != 4):
			#print("LINE 148 - You must enter an integer less than three and greater than or equal to 0. Or put 4 to exit \n")
			while ((choice > 2 or choice < 0) and choice != 4):
				try:
					print("You must enter an integer less than three and greater than or equal to 0. Or put 4 to exit. \n")
					choice = int(input("0: Rock, 1: Paper, 2: Scissors \n"))
				except ValueError:
					print("you must enter an integer. \n")

		if (choice == 4):
			print("Thanks for Playing!")
			continuePlaying = False
		else:
			if (prevChoice == choice):
				streak += 1
			else:
				streak -= 1
				if (streak < 0):
					streak = 0
			if (streak > 3):
				machineChoice = prevChoice - 2
				if (machineChoice < 0):
					machineChoice += 3
			elif (won > 9):
				print(
				    "Oh, you think you are clever, do you? Stop cheating, mortal!"
				)
				machineChoice = random.randint(0, 2)
			elif (won > 3 and won < 10):
				machineChoice = prevChoice
			else:
				if (result == "Win!"):
					machineChoice = prevChoice - 2
					if (machineChoice < 0):
						machineChoice += 3
				elif (result == "Lose!"):
					machineChoice = prevChoice + 1
					if (machineChoice > 2):
						machineChoice -= 3
					machineChoice -= 2
					if (machineChoice < 0):
						machineChoice += 3
				else:
					machineChoice = random.randint(0, 2)

			result = checkWin(choice, machineChoice, 2)

			if (result == "Win!"):
				won += 1
			else:
				won -= 2
				if (won < 0):
					won = 0

			print("You chose %s" % choices[choice])
			print("The machine chose %s" % choices[machineChoice])
			print("You %s" % result)
			prevChoice = choice

def expertMode():
  global probabilitiesRPS
  choices = ["Rock","Paper","Scissors"]
  choi = ['r','p','s']
  continuePlaying = True
  prevChoice = ""
  choice = 3
  probRock = 0
  probPaper = 0
  probScissors = 0

  try:
      choice = int(input("0: Rock, 1: Paper, 2: Scissors \n"))
  except ValueError:
    print("you must enter an integer. \n")

  if((choice > 2 or choice < 0)):
    #print ("You must enter an integer less than three and greater than or equal to 0  \n")
    while((choice > 2 or choice < 0)):
      print ("You must enter an integer less than three and greater than or equal to 0. \n")
      try:
        choice = int(input("0: Rock, 1: Paper, 2: Scissors \n"))
      except ValueError:
        print("you must enter an integer. \n")

  machineChoice = random.randint(0, 2)
  result = checkWin(choice,machineChoice,3)
  print ("You chose %s" % choices[choice])
  print ("The machine chose %s" % choices[machineChoice])
  print("You %s" % result)

  prevChoice = choice

  while(continuePlaying):
    choice = 3
    try:
      choice = int(input("0: Rock, 1: Paper, 2: Scissors, 4: exit \n"))
    except ValueError:
      print("you must enter an integer. \n")

    if((choice > 2 or choice < 0) and choice != 4):
      #print ("LINE 250 - You must enter an integer less than three and greater than or equal to 0 or choose 4 to exit.  \n")
      while((choice > 2 or choice < 0) and choice != 4):
        print ("You must enter an integer less than three and greater than or equal to 0 or choose 4 to exit.\n")
        try:
          choice = int(input("0: Rock, 1: Paper, 2: Scissors, 4: exit \n"))
        except ValueError:
          print("you must enter an integer. \n")
    if (choice == 4):
      print("Thanks for Playing!\n")
      continuePlaying = False
    else:
      transMatrix = buildTransitionProbabilities(prevChoice,choice,result)
      machineChoice = random.randint(1, 100)
      probabilitiesRPS[0] = transMatrix[prevChoice][0]
      probabilitiesRPS[1] = transMatrix[prevChoice][1]
      probabilitiesRPS[2] = transMatrix[prevChoice][2]
      rangeR = probabilitiesRPS[0] * 100
      rangeP = probabilitiesRPS[1] * 100 + rangeR
      if (machineChoice <= rangeR):
        machineChoice = 1
      elif (machineChoice <= rangeP):
        machineChoice = 2
      else:
        machineChoice = 0

      result = checkWin(choice,machineChoice,3)
      prevChoice = choice
      print ("You chose %s" % choices[choice])
      print ("The machine chose %s" % choices[machineChoice])
      print("You %s" % result)


def buildTransitionProbabilities(pC,c,winloss):
  global buildTMatrix
  global buildTMatrixL
  global buildTMatrixT
  choi = ['r','p','s']

  if winloss == "Win!":
    for i, x in buildTMatrix.items():
      if ('%s%s' % (choi[pC],choi[c]) == i):
        buildTMatrix['%s%s' % (choi[pC], choi[c])] += 1
  elif winloss == "Tied!":
    for i, x in buildTMatrixT.items():
      if ('%s%s' % (choi[pC],choi[c]) == i):
        buildTMatrixT['%s%s' % (choi[pC], choi[c])] += 1
  else:
    for i, x in buildTMatrixL.items():
      if ('%s%s' % (choi[pC],choi[c]) == i):
        buildTMatrixL['%s%s' % (choi[pC], choi[c])] += 1

  return buildTransitionMatrix(winloss)

def buildTransitionMatrix(winlosstwo):
  global tMatrix
  global tMatrixL
  global tMatrixT

  if winlosstwo == "Win!":
    rock = buildTMatrix['rr'] + buildTMatrix['rs'] +buildTMatrix['rp']
    paper = buildTMatrix['pr'] + buildTMatrix['ps'] +buildTMatrix['pp']
    scissors = buildTMatrix['sr'] + buildTMatrix['ss'] +buildTMatrix['sp']
    choi = ['r','p','s']
    for row_index, row in enumerate(tMatrix):
      for col_index, item in enumerate(row):
          a = int(buildTMatrix['%s%s' % (choi[row_index],choi[col_index])])
          if (row_index == 0):
            c = a/rock
          elif (row_index == 1):
            c = a/paper
          else:
            c = a/scissors
          row[col_index] = float(c)
    return (tMatrix)
  elif winlosstwo == "Tied!":
    rock = buildTMatrixT['rr'] + buildTMatrixT['rs'] +buildTMatrixT['rp']
    paper = buildTMatrixT['pr'] + buildTMatrixT['ps'] +buildTMatrixT['pp']
    scissors = buildTMatrixT['sr'] + buildTMatrixT['ss'] +buildTMatrixT['sp']
    choi = ['r','p','s']
    for row_index, row in enumerate(tMatrixT):
      for col_index, item in enumerate(row):
          a = int(buildTMatrixT['%s%s' % (choi[row_index],choi[col_index])])
          if (row_index == 0):
            c = a/rock
          elif (row_index == 1):
            c = a/paper
          else:
            c = a/scissors
          row[col_index] = float(c)
    return (tMatrixT)

  else:
    rock = buildTMatrixL['rr'] + buildTMatrixL['rs'] +buildTMatrixL['rp']
    paper = buildTMatrixL['pr'] + buildTMatrixL['ps'] +buildTMatrixL['pp']
    scissors = buildTMatrixL['sr'] + buildTMatrixL['ss'] +buildTMatrixL['sp']
    choi = ['r','p','s']
    for row_index, row in enumerate(tMatrixL):
      for col_index, item in enumerate(row):
          a = int(buildTMatrixL['%s%s' % (choi[row_index],choi[col_index])])
          if (row_index == 0):
            c = a/rock
          elif (row_index == 1):
            c = a/paper
          else:
            c = a/scissors
          row[col_index] = float(c)
    return (tMatrixL)

# Setting up a way to track wins/losses

def checkWin(user, machine, mode):
    win = False
    tie = False
    if (mode == 73):
        if (user == 0):
            if (machine == 2 or machine == 3):
                win = True
                tie = False
            elif (machine == 1 or machine == 4):
                win = False
                tie = False
            elif (machine == 0):
                tie = True
            else:
                print ("Something wierd happened and machine was: %s" % machine)
        elif (user == 1):
            if (machine == 0 or machine == 4):
                win = True
                tie = False
            elif (machine == 2 or machine == 3):
                win = False
                tie = False
            elif (machine == 1):
                tie = True
            else:
                print ("Something wierd happened and machine was: %s" % machine)
        elif (user == 2):
            if (machine == 1 or machine == 3):
                win = True
                tie = False
            elif (machine == 0 or machine == 4):
                win = False
                tie = False
            elif (machine == 2):
                tie = True
            else:
                print ("Something wierd happened and machine was: %s" % machine)
        elif (user == 3):
            if (machine == 4 or machine == 1):
                win = True
                tie = False
            elif (machine == 2 or machine == 0):
                win = False
                tie = False
            elif (machine == 3):
                tie = True
            else:
                print ("Something wierd happened and machine was: %s" % machine)
        else:
            if (machine == 2 or machine == 0):
                win = True
                tie = False
            elif (machine == 1 or machine == 3):
                win = False
                tie = False
            elif (machine == 4):
                tie = True
            else:
                print ("Something wierd happened and machine was: %s" % machine)
    else:
        if (user == 0):
            if (machine == 2):
                win = True
                tie = False
            elif (machine == 1):
                win = False
                tie = False
            elif (machine == 0):
                tie = True
            else:
                print ("Something wierd happened and machine was: %s" % machine)
        elif (user == 1):
            if (machine == 0):
                win = True
                tie = False
            elif (machine == 2):
                win = False
                tie = False
            elif (machine == 1):
                tie = True
            else:
                print ("Something wierd happened and machine was: %s" % machine)
        else:
            if (machine == 1):
                win = True
                tie = False
            elif (machine == 0):
                win = False
                tie = False
            elif (machine == 2):
                tie = True
            else:
                print ("Something wierd happened and machine was: %s" % machine)

    if (tie == True):
        checkStats(2, mode)
        return "Tied!"
    elif (win):
        checkStats(0, mode)
        return "Win!"
    else:
        checkStats(1, mode)
        return "Lose!"


#Defining the flow of the game through user choice
def main():
  playAgain = True
  notyesorno = True

  while (playAgain):
    notyesorno = True
    playAgain = False
    chosenMode = chooseMode()
    if(chosenMode == 1):
      easyMode()
      #print(HighB)
      print ("Your stats:")
      print(X)
      displaystats(winEas,loseEas,tieEas,"Easy Mode")
      displayOtherModes("Easy Mode")
    elif (chosenMode == 2):
      intermediateMode()
      #print(HighB)
      print ("Your stats:")
      print(X)
      displaystats(winInt,loseInt,tieInt,"Intermediate Mode")
      displayOtherModes("Intermediate Mode")
    elif (chosenMode == 3):
      expertMode()
      #print(HighB)
      print ("Your stats:")
      print(X)
      displaystats(winExp,loseExp,tieExp,"Expert Mode")
      displayOtherModes("Expert Mode")
    else:
      print ("I guess we will move on to whether or not ya wanna play again...\n")

    while(notyesorno):
      continueGame = input("Do you wanna play again? Type Yes or No \n")
      if (continueGame.lower() == "yes"):
        print ("Great! \n")
        notyesorno = False
        playAgain = True
      elif (continueGame.lower() == "no"):
        print ("Ok, that's fine. :( \n")
        finalstats()
        notyesorno = False
        playAgain = False
      else:
        print ("That's not an acceptable answer. Please type Yes or No")
        notyesorno = True

#Creating the final stats

def finalstats():
  global winEas,loseEas,tieEas,winInt,loseInt,tieInt,winHard,loseHard,tieHard,winExp,loseExp,tieExp,winspec,losespec,tiespec,hiddenfound
  #print(HighB)
  print ("These are your final stats:")
  print (X)
  #Easy Mode
  if(winEas+loseEas+tieEas != 0):
    percentWonE = "{percent:.2%}".format(percent=(winEas / (winEas+loseEas+tieEas)))
  else:
    percentWonE = "{percent:.2%}".format(percent= 0)
  #Intermediate Mode
  if(winInt+loseInt+tieInt != 0):
    percentWonI = "{percent:.2%}".format(percent=(winInt / (winInt+loseInt+tieInt)))
  else:
    percentWonI = "{percent:.2%}".format(percent= 0)
  #Expert Mode
  if(winExp+loseExp+tieExp != 0):
    percentWonEx = "{percent:.2%}".format(percent=(winExp / (winExp+loseExp+tieExp)))
  else:
    percentWonEx = "{percent:.2%}".format(percent= 0)
  print(Bold)
  print ("You have a %s win rate on %s!" % (percentWonE,"Easy Mode"))
  print ("You have a %s win rate on %s!" % (percentWonI,"Intermediate Mode"))
  print ("You have a %s win rate on %s!" % (percentWonEx,"Expert Mode"))
  

def displaystats(wmode,lmode,tmode,mode):
  print ("\nYou won %d times!\n" % int(wmode))
  print ("You lost %d times!\n" % int(lmode))
  print ("You tied %d times!\n" % int(tmode))
  if(wmode+lmode+tmode != 0):
    percentWon = "{percent:.2%}".format(percent=(wmode / (wmode+lmode+tmode)))
  else:
    percentWon = "{percent:.2%}".format(percent= 0)
    print ("You have a %s win rate on %s! \n" % (percentWon,mode))

def displayOtherModes(mode):
  global winEas,loseEas,tieEas,winInt,loseInt,tieInt,winHard,loseHard,tieHard,winExp,loseExp,tieExp,winspec,losespec,tiespec
  modes = ["Easy Mode", "Intermediate Mode","Expert Mode"]
  #print(HighB)
  print ("Your stats in other modes:")
  print(X)
  for m in modes:
    if (m != mode):
        print(Bold)
        print (m)
        print(X)
        if (m == "Easy Mode"):
            displaystats(winEas,loseEas,tieEas,"Easy Mode")
        if (m == "Intermediate Mode"):
            displaystats(winInt,loseInt,tieInt,"Intermediate Mode")
        if (m == "Expert Mode"):
            displaystats(winExp,loseExp,tieExp,"Expert Mode")

#Setting up yes/no answer

def continueGameCheck(ans):
  if (ans.lower() == "yes"):
    return "Yes"
  elif (ans.lower() == "no"):
    return "No"
  else:
    return "Wrong input"  

#Defining Scores

def checkStats(wlt,modeChosen):
  global winEas
  global loseEas
  global tieEas
  global winInt
  global loseInt
  global tieInt
  global winExp
  global loseExp
  global tieExp


  if (modeChosen == 1):
    if (wlt == 0):
      winEas += 1
    elif (wlt == 1):
      loseEas += 1
    else:
      tieEas += 1
  elif (modeChosen == 2):
    if (wlt == 0):
      winInt += 1
    elif (wlt == 1):
      loseInt += 1
    else:
      tieInt += 1
  else: 
    if (wlt == 0):
      winExp += 1
    elif (wlt == 1):
      loseExp += 1
    else:
      tieExp += 1
  
main()