import EncDec as enc
from copy import deepcopy


class Node():
    def __init__(self, char, code, left=None, right=None):
        self.char = char
        self.code = code
        self.parent = code[:-1]
        self.left = left
        self.right = right


class Tree():
    def __init__(self, code):
        self.code = code
        self.depth = len(max(self.code.values(), key=len))
        self.tree = self.build_Tree(self.code)
        self.treeLines = [[] for i in range(self.depth+1)]
        self.pop_treeLines()
        

    def pop_treeLines(self):
        self.treeLines[0] = 'ROOT'
        self.treeLines[1].extend(['0', '1'])
        sortedTree = dict(sorted(self.tree.items(), key=lambda x: (len(x[1].code), x[1].code)))
        for k, v in sortedTree.items():
            if v.left == None:
                self.treeLines[len(v.code)].append(k + ' : ' + v.code)
            else:
                self.treeLines[len(v.code)].append('XX')

    def build_Tree(self, code, tree=None, treelen=None):
     
        if not tree: #adds leaf nodes (runs only for the first iteration
            tree = dict()
            for k, v in code.items(): 
                tree[k] = Node(k, v)
            return self.build_Tree(code, tree, len(tree))

        else:
            new_tree = deepcopy(tree)
            for k, v in tree.items():
                if len(v.parent) > 1: #stops generating parent nodes before 0 and 1 (to avoid conflict with the '0' and '1' keys.
                    try:
                        new_tree[v.parent]
                    except KeyError:
                        new_tree[v.parent] = Node(None, v.parent)
                    if v.code[-1] == '0':
                        new_tree[v.parent].left = k
                    elif v.code[-1] == '1':
                        new_tree[v.parent].right = k
            if len(new_tree) == treelen:
                return new_tree
            else:
                return self.build_Tree(code, new_tree, len(new_tree))

    def visualize_Tree(self): #need to implement whitespace replacement and an actual way of plotting the tree
        maxlen = len('  '.join(self.treeLines[-1]))
        printable = ''
        for line in self.treeLines:
            stringit = '  '.join(line).center(maxlen)
            printable += (stringit + '\n')
        return printable

    def save_to_File(self):
        output = open('huffTree.txt', 'w')
        output.write(self.visualize_Tree())
        output.close()
        
if __name__ == '__main__':
    print('Tree generator for EncDec by Bernardo Tonasse')
    code = enc.map_Code(enc.theKey)
    mainTree = Tree(code)


'''
def build_Tree(code, tree=None, treelen=None):
 
    if not tree: #adds leaf nodes (runs only for the first iteration)
        tree = dict()
        for k, v in code.items(): 
            tree[k] = Node(k, v)
        return build_Tree(code, tree, len(tree))

    else:
        new_tree = deepcopy(tree)
        for k, v in tree.items():
            if len(v.parent) > 1:
                try:
                    new_tree[v.parent]
                except KeyError:
                    new_tree[v.parent] = Node(None, v.parent)
                if v.code[-1] == '0':
                    new_tree[v.parent].left = k
                elif v.code[-1] == '1':
                    new_tree[v.parent].right = k
        if len(new_tree) == treelen:
            return new_tree
        else:
            return build_Tree(code, new_tree, len(new_tree))
            
'''

    
'''
for w in range(1,depth+1):
    count = sum(map(lambda x: len(x) == w, code.values()))
    print(f'Number of items with len = {w}: {count}')
'''
