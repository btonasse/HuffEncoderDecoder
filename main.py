import string as st

from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from android.permissions import request_permissions, Permission
request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                     Permission.READ_EXTERNAL_STORAGE])

Config.set('kivy','window_icon','EncDec.ico')

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

theCode = {}

Builder.load_string('''
<ScrollableText>:
    id: scrl
    scroll_type: ['bars', 'content']
    bar_width: 4
    bar_color: [.2, .2, .2, .9]
    bar_inactive_color: [.7, .7, .7, .9]
    
    TextInput:
        id: ti
        size_hint_y: None
        height: max(self.minimum_height, scrl.height)

<ScrollableLabel>:
    id: sc
    
    Label:
        id: lb
        text: sc.text
        font_size: 12
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]

''')

class ScrollableText(ScrollView):
    pass
class ScrollableLabel(ScrollView):
    text = StringProperty('')

class EncDecApp(App):
    popup1 = ObjectProperty(None)
    popup2 = ObjectProperty(None)
    def build(self):
        self.title = 'Huffman encryptor/decryptor - by Bernardo Tonasse - v1.0'
        self.root = BoxLayout(orientation='vertical')
        
        self.topLayout = BoxLayout(size_hint_y=10)
        self.inputScroll = ScrollableText()
        self.outputScroll = ScrollableText()
        

        self.midLayout = BoxLayout()
        self.encBtn = Button(text='ENCODE--->')
        self.decBtn = Button(text='<---DECODE')

        self.encBtn.bind(on_press = lambda x: self.enc_Button())
        self.decBtn.bind(on_press = lambda x: self.dec_Button())
        
        self.botLayout = BoxLayout()
        self.keyBtn = Button(text='VIEW/SET KEY')
        self.keyBtn.bind(on_press = lambda x: self.viewset_Key())
        
        self.botLayout.add_widget(self.keyBtn)
        self.midLayout.add_widget(self.encBtn)
        self.midLayout.add_widget(self.decBtn)
        self.topLayout.add_widget(self.inputScroll)
        self.topLayout.add_widget(self.outputScroll)
        
        self.root.add_widget(self.topLayout)
        self.root.add_widget(self.midLayout)
        self.root.add_widget(self.botLayout)

        self.init_program()

        return self.root

    def generic_YesNo(self, button, texttoshow='None', titletoshow='Test'):
        
        poproot = GridLayout(cols=1, padding=10)

        popLabel = ScrollableLabel(size_hint_y = 10, text = texttoshow)
        popYes = Button(text = 'Yes')
        popNo = Button(text = 'No')

        poproot.add_widget(popLabel)
        poproot.add_widget(popYes)
        poproot.add_widget(popNo)

        self.popup1 = Popup(title = titletoshow, content = poproot, title_align='center', auto_dismiss=True)
        self.popup1.open()

        popYes.bind(on_press = self.yes_newKey)
        popNo.bind(on_press = self.popup1.dismiss)

    def yes_newKey(self, instance):
        self.popup1.dismiss()
        poproot = GridLayout(cols=1, padding=10)

        popText = ScrollableText(size_hint_y = 10)
        popOK = Button(text = 'OK')
        popCancel = Button(text = 'CANCEL')
        
        poproot.add_widget(popText)
        poproot.add_widget(popOK)
        poproot.add_widget(popCancel)

        self.popup2 = Popup(title = 'Enter new key (only ASCII printable characters allowed)', content = poproot, title_align='center', auto_dismiss=True)
        self.popup2.open()

        popOK.bind(on_press = lambda x: self.init_program(popText.ids.ti.text.strip()))
        popCancel.bind(on_press = self.popup2.dismiss)
        

    def generic_Exception(self, button, texttoshow='None', titletoshow='Error!'):
        poproot = GridLayout(cols=1, padding=10)

        popLabel = Label(size_hint_y = 10, text = texttoshow)
        popOK = Button(text = 'OK')
        
        poproot.add_widget(popLabel)
        poproot.add_widget(popOK)
        
        popup = Popup(title = titletoshow, content = poproot, title_align='center')
        popup.open()

        popOK.bind(on_press = popup.dismiss)

    def complete_Key(self, keystring):
        '''
        Returns a list of characters contained in the keystring so the program raises exceptions whenever you try to encode a message containing unmapped characters.
        If some ascii characters are missing, they are added at the end of the string.
        '''
        origChars = set(keystring)
        
        if any(char not in allASCII for char in origChars):
          self.generic_Exception('',texttoshow='Key contains non ASCII characters. Please enter a valid key.',titletoshow='Error')
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
        toencode = self.inputScroll.ids.ti.text
        try:
            enctext = self.encode_Text(toencode,theCode)
            self.outputScroll.ids.ti.text = enctext
        except:
            self.generic_Exception('',texttoshow='Only printable ASCII characters are accepted.',titletoshow='Error')
            return
        return

    def dec_Button(self):
        '''
        Callback for decode button.
        '''
        todecode = self.outputScroll.ids.ti.text
        
        try:
          dectext = self.decode_Text(todecode,theCode)
          self.inputScroll.ids.ti.text = dectext
        except:
          self.generic_Exception('',texttoshow='Only 0s and 1s are accepted.',titletoshow='Error')
          return
        return

    def viewset_Key(self):
      global theKey, theCode
      self.generic_YesNo('', texttoshow=theKey, titletoshow='This is the current encryption key. Do you want to change it?')
    
    def set_defaultKeyFile(self, keystring):
        defaultKeyFile = open('currentKey.txt', 'w')
        defaultKeyFile.write(keystring)
        defaultKeyFile.close()
    
    def get_defaultKeyFile(self):
        defaultKeyFile = open('currentKey.txt', 'r')
        newKey = defaultKeyFile.read()
        if any(char not in allASCII for char in newKey):
            defaultKeyFile.close()
            raise ValueError('Only printable ASCII chars allowed.')
        defaultKeyFile.close()
        return newKey

    def init_program(self, reinitKey=None):  
        global theKey, theCode
        
        if reinitKey:
            try:
                self.set_defaultKeyFile(reinitKey)
                theKey = self.get_defaultKeyFile()
                theCode = self.map_Code(theKey)
                self.popup2.dismiss()
            except:
                self.generic_Exception('',texttoshow='Only printable ASCII characters are accepted.',titletoshow='Error')
                return
        else:
            try:
                theKey = self.get_defaultKeyFile()
            except:
                self.set_defaultKeyFile(theKey)
                #self.generic_Exception('',texttoshow="Default key 'currentKey.txt' not found. Initializing placeholder key.",titletoshow='Warning')
            theCode = self.map_Code(theKey) 

if __name__ == "__main__":
    EncDecApp().run()

