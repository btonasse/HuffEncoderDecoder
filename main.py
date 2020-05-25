import string as st
import os.path
from jnius import autoclass
from time import sleep

from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.factory import Factory

from android.permissions import request_permissions, Permission, check_permission
if not check_permission(Permission.WRITE_EXTERNAL_STORAGE) or not check_permission(Permission.READ_EXTERNAL_STORAGE):
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                     Permission.READ_EXTERNAL_STORAGE])
    sleep(5)


Config.set('kivy','pause_on_minimize', 1)
Config.set('kivy', 'exit_on_escape', 0)

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

defKey = theKey

theCode = {}

class CustPopup(Popup):
    lbl_text = StringProperty('')
    newkeyinput = StringProperty('')

class LoadDiag(BoxLayout):
    dism = ObjectProperty(None)
    load = ObjectProperty(None)
    
class SaveDiag(BoxLayout):
    dism = ObjectProperty(None)
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    
class RootBox(BoxLayout):
    newkey_input = StringProperty('')
    yesno_answer = StringProperty('')
    temppath = StringProperty('')
    tempfile = StringProperty('')

    def show_load(self):
        content = LoadDiag(dism = self.dismiss, load = self.load)
        self.saveloadpop = Popup(title='Load file...', content=content, auto_dismiss=False)
        self.saveloadpop.open()

    def dismiss(self):
        self.saveloadpop.dismiss()

    def load(self, path, file):
        if not file:
            return
        filename = file[0]
        with open(filename) as filetoopen:
            self.newkey_input = filetoopen.read()
        self.dismiss()

    def show_save(self):
        content = SaveDiag(dism = self.dismiss, save = self.save)
        self.saveloadpop = CustPopup(title='Save file...', content=content, auto_dismiss=False)
        self.saveloadpop.open()
    
    def generic_yesno(self, tit, txt):
        Factory.GenYesNo(title=tit, lbl_text=txt).open()
    
    def save(self, path, file):
        if not file:
            return
        validtext = st.ascii_letters + st.digits + '.-_ '
        if any(char not in validtext for char in file):
            Factory.GenericPop(title='Error',lbl_text='No special characters on the filename, please.').open()
            return
        oldkey_text = self.get_currentKeyFile()
        filename = os.path.join(path, file)
        
        self.temppath = path
        self.tempfile = file        
        if os.path.exists(filename) and not self.yesno_answer:
            self.generic_yesno(tit='Overwrite existing file?', txt='File already existis. Overwrite it?')
        elif self.yesno_answer == 'no':
                self.yesno_answer = ''
                return
        else:
            self.yesno_answer = ''
            if filename[-4:] != '.txt':
                filename += '.txt'
            with open(filename, 'w') as filetosave:
                filetosave.write(oldkey_text) 
            self.dismiss()
    
    def complete_Key(self, keystring):
        '''
        Returns a list of characters contained in the keystring so the program raises exceptions whenever you try to encode a message containing unmapped characters.
        If some ascii characters are missing, they are added at the end of the string.
        '''
        origChars = set(keystring)
        
        if any(char not in allASCII for char in origChars):
          Factory.GenericPop(title='Error',lbl_text='Key contains non ASCII characters. Please enter a valid key.').open()
          return

        charsToAdd = [char for char in allASCII if char not in origChars]
        stringToAdd = ''.join(charsToAdd)
        finalKey = keystring + stringToAdd
        return finalKey

    def count_Frequency(self, keystring):
        '''
        Returns a sorted dictionary containing all ASCII characters and their frequencies in the keystring.
        '''
        completeKey = self.complete_Key(keystring)
        freqDict = {}
        for char in set(completeKey):
            freqDict[char] = completeKey.count(char)
        freqDict = self.sort_FreqDict(freqDict)
        return freqDict

    def sort_FreqDict(self, dic):
        '''
        Sorts chars dictionary by frequency. Ties are broken by 'alphabetical' order to ensure sorting consistency.
        '''
        if type(dic) is list:
          toDict = dict(dic)
          sortedDict = sorted(toDict.items(), key=lambda x: x[1], reverse=True)
        else:
          sortedDict = dict(sorted(dic.items(), key=lambda x: (x[1],x[0]), reverse=True))
        return sortedDict
    
    def create_Tree(self, dic):
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
          pqueue = self.sort_FreqDict(pqueue)
        treeDict = newNode
        return treeDict

    def code_Gen(self, tree):
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

    def map_Code(self, keystring):
        '''
        Puts all the above functions into one box. Returns the code map.
        '''
        a = self.count_Frequency(keystring)
        b = self.create_Tree(a)
        c = self.code_Gen(b)
        return c

    def encode_Text(self, text, codedict):
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

    def decode_Text(self, text, codedict):
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

    def enc_Button(self):
        '''
        Callback for encode button.
        '''
        toencode = self.ids.inputBox.text

        try:
            enctext = self.encode_Text(toencode,theCode)
            self.ids.outputBox.ids.ti.text = enctext
        except:
            Factory.GenericPop(title='Error',lbl_text='Only printable ASCII characters are accepted.').open()
            return
        return

    def dec_Button(self):
        '''
        Callback for decode button.
        '''
        todecode = self.ids.outputBox.text
        
        try:
          dectext = self.decode_Text(todecode,theCode)
          self.ids.inputBox.ids.ti.text = dectext
        except:
          Factory.GenericPop(title='Error',lbl_text='Only 0s and 1s are accepted.').open()
          return
        return

    def set_currentKeyFile(self, keystring):
        '''
        Write the new key to the currentKey.txt file, so the program remembers it next time.
        '''        
        file_path = os.path.join(data_dir, 'currentKey.txt')
        currentKeyFile = open(file_path, 'w')
        currentKeyFile.write(keystring)
        currentKeyFile.close()
    
    def get_currentKeyFile(self):
        '''
        Helps rebuilding currentKey.txt. Kinda redundant, since if it fails the program will fallback to the theKey global variable to do the same.
        '''        
        file_path = os.path.join(data_dir, 'currentKey.txt')
        currentKeyFile = open(file_path, 'r')
        newKey = currentKeyFile.read()
        if not newKey or any(char not in allASCII for char in newKey):
            currentKeyFile.close()
            raise ValueError('Only printable ASCII chars allowed.')
        currentKeyFile.close()
        return newKey

    def get_defaultKeyFile(self):
        '''
        Reads defaultKey.txt and returns its contents.
        '''
        file_path = os.path.join(data_dir, 'defaultKey.txt')

        if not os.path.exists(file_path):
            newdefKeyFile = open(file_path, 'w')
            newdefKeyFile.write(defKey)
            newdefKeyFile.close()

        defaultKeyFile = open(file_path, 'r')
        newKey = defaultKeyFile.read()
        if not newKey or any(char not in allASCII for char in newKey):
            defaultKeyFile.close()
            raise ValueError("'defaultKey.txt' contains non printable ASCII chars.")
        defaultKeyFile.close()
        return newKey

    def init_program(self, reinitKey=None):  
        '''
        Executed when the program is first runs.
        Initializes the encryption key and calls all functions necessary to build the code dictionary.
        Is also run when the encryption key is changed to rebuild the dictionary and txt files.
        '''        
        global theKey, theCode

        if reinitKey:
            if any(char not in allASCII for char in reinitKey):
                Factory.GenericPop(title='Error',lbl_text='Only printable ASCII characters are accepted.').open()
                return
            else:
                self.set_currentKeyFile(reinitKey)
                theKey = self.get_currentKeyFile()
                theCode = self.map_Code(theKey)

        else: #This should only run the first time the program executes
            try:
                theKey = self.get_currentKeyFile()
            except PermissionError:
                print('No storage permissions. Exiting app.')
                mainapp.stop()
            except:
                try:
                    theKey = self.get_defaultKeyFile()
                    self.set_currentKeyFile(theKey)
                except:
                    self.set_currentKeyFile(theKey)
            theCode = self.map_Code(theKey) 


class ScrollableText(ScrollView):
    text = StringProperty('')
class ScrollableLabel(ScrollView):
    text = StringProperty('')

class EncDecApp(App):
    rootMain = ObjectProperty(RootBox())
    def build(self):
        
        rootMain = RootBox()
        rootMain.init_program()
        return rootMain

mainapp = EncDecApp()
if __name__ == "__main__":
    try:
        Environment = autoclass('android.os.Environment')
        path = Environment.getExternalStorageDirectory().getAbsolutePath()
        data_dir = os.path.join(path, 'EncDec')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
    except PermissionError:
        print('Failed to create EncDec folder (no permission). Exiting app.')
        mainapp.exit()    
    
    mainapp.run()

