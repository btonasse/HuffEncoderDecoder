import string as st
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile, asksaveasfilename
import os
import sys

CWDPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

allASCII = st.printable

theKey = '''Congue comprehensam eam id, utroque forensibus ad quo, pertinax sensibus dissentias vim at. Cu brute reprimique dissentiunt duo. Nullam platonem intellegam ea eam. Quo ei numquam qualisque consetetur, hinc mediocrem cu pri. Sea id paulo facilisis iracundia, sea ad civibus principes splendide, nam oportere contentiones signiferumque te. Te per semper intellegam. Ex vis unum elitr aperiam.
Pro at vidit vocibus, an laboramus reprimique efficiantur nec. His ignota vivendum recteque ut, ad eam paulo recteque. Nominavi iracundia quo te, eu sit viderer assentior? Sed at torquatos mediocritatem, diam quodsi et mea, mollis oblique scripserit ut per! Quando incorrupte pri ex, eruditi sententiae sit an! Eum ex natum consul dolorem!
Qui et accusamus definitiones, nam dicat quodsi et, liber iracundia has in. At mea eleifend petentium, eu quodsi nostrud reprimique vix. Per ludus prompta consequuntur et, ei sit ludus evertitur, atqui electram pri no. Discere percipitur ne pri! Delenit accusam facilisi eum no, in mea malis suscipit!
Mel alii purto viris ut, nostrum incorrupte vituperatoribus eu usu, eu petentium conclusionemque nec. Omnes honestatis an vis, eros posse eu est, no mei solet democritum interpretaris. Vix vero forensibus te, nostrum convenire adolescens eu vim! Vim te ignota vituperata consequuntur.
Error aperiri adversarium an est, vel id dicat denique. Ei nec ipsum mediocritatem, detraxit posidonium nec ea! Duis iuvaret admodum est eu, sea at partem periculis dignissim! Te mel ullum persequeris! Graeci eleifend vel ad, cu facilisi rationibus est. Pro ex facilis indoctum.
Ea vim nostrud suavitate, reque quando consequat eu vim. Nam mnesarchum complectitur cu, cum ne elit argumentum, fabulas ullamcorper vim ad. Vis tation graece eripuit ex, dolor vocent at usu. Veniam doctus legendos ea cum. In eos unum contentiones, ea duo sale harum soluta.
Amet modus ceteros eam an. Te amet esse mel, vim vero appareat ex. Pri ex modo scripta indoctum. Splendide sadipscing no pro, eripuit splendide te sed. Per legimus partiendo ei, erat epicuri ad vim! Veritus suscipiantur te vel.
Vidit natum delenit mea ad, ex pro maiorum platonem! Dolorem assueverit efficiantur eu vim. Eum id probatus disputationi, duo molestie qualisque no. Nam vide rationibus cu. Illum facer verterem ei has!
Et appetere complectitur quo. Ex magna utroque efficiendi pro. Sed ei partem persequeris, eu amet graecis vivendo ius. Enim suscipit efficiantur pro te, iisque argumentum quo ex! Ut noster impetus pri. Vix an sumo errem atomorum! Id tale error vel.
Alienum persecuti id eum, et eum enim autem molestie. Vulputate theophrastus delicatissimi ei his, ei pro odio putent pertinacia? Vim eu posse verear. Cu quo enim voluptatum appellantur, eos et volumus eligendi, alia legere menandri his ut! Cu pro etiam mazim petentium, est ex exerci scripserit.'''

def complete_Key(keystring):
	'''
	Returns a list of characters contained in the keystring so the program raises exceptions whenever you try to encode a message containing unmapped characters.
	If some ascii characters are missing, they are added at the end of the string.
	'''
	origChars = set(keystring)
	
	if any(char not in allASCII for char in origChars):
		messagebox.showerror("Error","currentKey.txt contains non ASCII characters. Program will terminate.")
		sys.exit()

	charsToAdd = [char for char in allASCII if char not in origChars]
	stringToAdd = ''.join(charsToAdd)
	finalKey = keystring + stringToAdd
	return finalKey
	
def count_Frequency(keystring):
    '''
    Returns a sorted dictionary containing all ASCII characters and their frequencies in the keystring.
    '''
    completeKey = complete_Key(keystring)
    freqDict = {}
    for char in set(completeKey):
        freqDict[char] = completeKey.count(char)
    freqDict = sort_FreqDict(freqDict)
    return freqDict

def sort_FreqDict(dic):
	'''
	Sorts chars dictionary by frequency. Ties are broken by 'alphabetical' order to ensure sorting consistency.
	'''
	if type(dic) is list:
		toDict = dict(dic)
		sortedDict = sorted(toDict.items(), key=lambda x: x[1], reverse=True)
	else:
		sortedDict = dict(sorted(dic.items(), key=lambda x: (x[1],x[0]), reverse=True))
	return sortedDict

def code_Gen(tree):
	'''
	Generates the code mapping and returns a dictionary
	'''
	root = max(tree.keys(),key=lambda x: len(x)) #gets the root key of the tree
	codeDict = {}
	for char in root:
		code = ''
		for child in tree.values():
			if child:
				if char in child[0]:
					code = '0' + code
				elif char in child[1]:
					code = '1' + code
			else:
				continue
		codeDict[char] = code
	return codeDict


def create_Tree(dic):
	'''
	Creates the tree and nodes.
	'''
	pqueue = list(dic.items())
	newNode = {}
	for char in dic.keys(): #initializes leaf nodes
		newNode[char] = []
	while len(pqueue) > 1:
		newKey = pqueue[-1][0] + pqueue[-2][0]
		newFreq = pqueue[-1][1] + pqueue[-2][1]
		reinsertedNode = (newKey,newFreq) #creates a node for reinsertion into pqueue
		newNode[newKey] = [pqueue[-1][0], pqueue[-2][0]] #adds a pair of child nodes to each new node

		pqueue = pqueue[:-2]  #removes child nodes from pqueue
		pqueue.append(reinsertedNode)
		pqueue = sort_FreqDict(pqueue)
	treeDict = newNode
	return treeDict

def map_Code(keystring):
	'''
	Puts all the above functions into one box. Returns the code map.
	'''
	a = count_Frequency(keystring)
	b = create_Tree(a)
	c = code_Gen(b)
	return c




def encode_Text(text, codedict):
	'''
	Encodes a given text using code map generated by code_Gen (or map_Code)
	'''
	encText = ''
	for char in text:
		try:
			encText += codedict[char]
		except KeyError:
			print('Only ASCII characters are accepted for now')
			return
	return encText


def decode_Text(text, codedict):
	'''
	Decodes a previously encoded text provided the both encryption and decryption used the right key.
	'''
	text = text.strip()
	if any(char not in '01' for char in text):
		print('Error: expected string of 0s and 1s.')
		return
	reversedDict = {v:k for k,v in codedict.items()}
	decText = ''
	fullCharCode = ''
	for digit in text:
		fullCharCode += digit
		try:
			decText += reversedDict[fullCharCode]
			fullCharCode = ''
		except KeyError:
			continue
	return decText


def enc_Button():
	toencode = inputText.get('1.0', END)
	toencode = toencode[:-1]
	try:
		enctext = encode_Text(toencode,theCode)
		outputText.delete('1.0',END)
		outputText.insert(END, enctext)
	except:
		messagebox.showerror("Error","Only ASCII characters are currently valid.")
		return
	return
	
def dec_Button():
	todecode = outputText.get('1.0', END)
	todecode = todecode[:-1]
	try:
		dectext = decode_Text(todecode,theCode)
		inputText.delete('1.0',END)
		inputText.insert(END, dectext)
	except:
		messagebox.showerror("Error","Only 0s and 1s allowed.")
		return
	return

def viewset_Key():
	global theKey, theCode
	answer = messagebox.askyesno('Change encryption key?', f'The current encryption key is:\n\n{theKey}\n\nDo you want to set a new key?', default='no', icon='question', parent=root)
	if answer == False:
		return
	else:
		file = askopenfile(mode = 'r', filetypes=[("Text","*.txt")], title="Select a text file...")
		if file:
			newKey = file.read()
			newKeySet = set(newKey)
			if any(char not in allASCII for char in newKeySet) or not newKey:
				messagebox.showerror("Error","Selected file contains non ASCII characters or is blank. Key not changed.")
				return
			if len(newKeySet) < 27:
				answer = messagebox.askyesno('Data set too small', "The selected file doesn't contain enough unique ASCII characters. Encoded messages will be longer than usual, but encryption/decryption will still work. Do you want to continue?", default='no', icon='question', parent=root)
				if answer == False:
					return
			
			answer = messagebox.askyesno('Back up current key?', 'Do you want to save the current key to a backup txt file?', default='no', icon='question', parent=root)
			if answer == True:
				filename = asksaveasfilename(defaultextension=".txt", filetypes=[("Text","*.txt")], title="Save file as")
				if filename:
					with open(filename, "w") as output_file:
						output_file.write(theKey)

			theKey = newKey
			theCode = map_Code(theKey)

			set_defaultKeyFile(theKey)
			file.close()
			messagebox.showinfo('Done!','Key successfully updated!')

def set_defaultKeyFile(keystring):
	defaultKeyFile = open('currentKey.txt', 'w')
	defaultKeyFile.write(keystring)
	defaultKeyFile.close()

def get_defaultKeyFile():
	defaultKeyFile = open('currentKey.txt', 'r')
	newKey = defaultKeyFile.read()
	defaultKeyFile.close()
	return newKey



		
		



if __name__ == '__main__':
	root = Tk()
	root.title("Message encyptor/decryptor - by Bernardo Tonasse")
	try:
		root.iconbitmap("EncDec.ico")
	except:
		pass

	# Initializing keystring and code mapping-------------
	try:
		theKey = get_defaultKeyFile()
	except:
		set_defaultKeyFile(theKey)
		root.withdraw()
		messagebox.showinfo('Warning',"Default key 'currentKey.txt' not found. Initializing placeholder key.")
		root.deiconify()
	theCode = map_Code(theKey) 
	# ----------------------------------------------------

	inputScroll = Scrollbar(root)
	outputScroll = Scrollbar(root)
	inputText = Text(root, selectbackground = 'gray', yscrollcommand = inputScroll.set)
	outputText = Text(root, bg = 'black', fg = 'white', insertbackground = 'white', selectbackground = 'gray', yscrollcommand = outputScroll.set)
	inputScroll.config(command=inputText.yview)
	outputScroll.config(command=outputText.yview)

	encBtn = Button(root, text='ENCODE-->', command=enc_Button)
	decBtn = Button(root, text='<--DECODE', command=dec_Button)
	keyBtn = Button(root, text='VIEW/SET KEY', command=viewset_Key)

	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)
	root.grid_columnconfigure(2, weight=1)
	inputText.grid   (row = 0, column = 0, padx = (4,0), pady = 4, sticky=N+E+W+S)
	inputScroll.grid (row = 0, column = 1, padx = (0,4), pady = 4, sticky=N+S)
	outputText.grid  (row = 0, column = 2, padx = (0,0), pady = 4, sticky=N+E+W+S)
	outputScroll.grid(row = 0, column = 3, padx = (0,4), pady = 4, sticky=N+S)
	encBtn.grid      (row = 1, column = 0, padx = (4,0), pady = (0,4), columnspan = 2, sticky = E+W)
	decBtn.grid      (row = 1, column = 2, padx = (0,4), pady = (0,4), columnspan = 2, sticky = E+W)
	keyBtn.grid      (row = 2, column = 0, padx = 4, columnspan = 4, sticky = E+W)

	root.mainloop()







