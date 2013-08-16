import os
import re
import copy

class GroupedResults(object):
    def __init__(self, groups):
        self._grouped_paths = []
        self._grouped_variables = []
        self._flat_paths = []
        self._flat_variables = []
        self._groups = []

        for k, group in groups.iteritems():
            self._grouped_paths.append([])
            self._grouped_variables.append([])
            self._groups.append([])
            dct = {}
            parts = []
            for item in group:
                dct = {}
                parts = []
                for _, name, val, _ in item:
                    if not name is None:
                        dct[name] = val
                    parts.append(val)                    
                path = os.path.join(*parts)
                self._groups[-1].append(  (path, dct) )
                self._grouped_variables[-1].append(  dct )
                self._grouped_paths[-1].append( path )
                self._flat_variables.append(  dct )
                self._flat_paths.append( path )

    def groups(self):
        return copy.copy(self._groups)

    def grouped_paths(self):
        return copy.copy(self._grouped_paths)

    def grouped_variables(self):
        return copy.copy(self._grouped_variables)

    def flat_paths(self):
        return copy.copy(self._flat_paths)

    def flat_variables(self):
        return copy.copy(self._flat_variables)


class Node(object):

    def __init__(self, match):
        self.variable_name, remainder = match.split("<", 1) if "<" in match else ( None,match)
        directive = None
        pattern = remainder
        remainder = remainder.strip()
        if remainder.startswith("::"):
            remainder = remainder[2:]
            directive, pattern = remainder.split(":",1) if ":" in remainder else (remainder, None)
        self.next =None
        self._directive = directive
        self._pattern = pattern
        self._match = match
        self._next = None
        self._qualify = None

        if directive == "any" or directive == "all" or directive == "file" or directive == "dir":
            qf = os.path.exists
            ## TODO: fix file and dir
            self._qualify = lambda x,y: qf(y)
            if self._pattern:
                repat = re.compile(self._pattern)
                self._qualify = lambda x, y: (not repat.search(x) is None) and qf(y)
        elif directive is None:
            self._directive = "any"
            self._qualify = lambda x, y: (x == pattern)

        priorities = {'all': 1,'any': 0, 'file': 0,'dir': 0}
        self._priority  = priorities[ self._directive ]

    def match_(self, root = ".", stack = None):
        if not os.path.isdir(root): return []
        if stack == None: stack = []

        stack.append( (0, 0,  None, None) )
        return_values = []
        for d in os.listdir(root):
            cur_path = os.path.join(root, d) 
            stack[-1] = (self._priority, len(stack), self.variable_name, d, self._directive)
            if self._qualify(d,cur_path):
                if self.next:
                    return_values += self.next.match_(cur_path, stack)
                else:
                    ret = sorted(copy.copy(stack))
                    return_values.append(ret)

        stack = stack[:-1]
        return return_values

    def search(self, root = "."):
        lst = self.match_(root)
        groups = {}
        for row in lst:
            i = 0
            parts = []
            iden = []
            for i in range(len(row)):
                if row[i][0] == 0:
                    iden.append(row[i][3])
                parts.append(row[i][1:])

            groupid = "/".join(iden)
            if not groupid in groups: groups[groupid] = []
            groups[groupid].append( sorted( parts ) )
        
        return GroupedResults(groups)



def compile(path):
    parts = path.split("/")
    nodes = [Node(x) for x in parts]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    
    return nodes[0]


if __name__ == "__main__":
    expr = compile(r"type<::any/lst<::any/hello world/::all:\d+")
    match = expr.search("./")
    print match.grouped_paths()
    expr = compile(r"type<::any/lst<::all/hello world/::anyp:\d+")
    match = expr.search("./")
    print match.grouped_paths()
#    for a in  expr.search("./"):
#        print a

