#!/usr/bin/python

#### GENERATE RANDOM CLIFFORD CIRCUITS
#### Author : Ross Duncan

from random import random
from more_itertools import sliced
from itertools import product
from copy import deepcopy
import sys
import json

#### default params -- the first four are overwritten
###  from the first four command line args if present
###  the others have to be changed here

params = {
    'width'  : 3,      # how many qubits?
    'depth'  : 5,      # max number of sequential gates
    'number' : 1,      # how many circuits to generate
    'prefix' : "",     # prepended to the filenames of generated circuits
    'ASCII'  : False,  # Save acsii version of file?
    'JSON'   : True,   # Save json version (for Quantomatic)?
    'verbose': True,   # print 'useful' information to stdout?
    'name'   : "Rando" # stem for filename
}

### these values are the probabilities for 
### choosing the next gate.
pHH = 0.0  # not using hadamard today
pZ1 = 0.11
pZ2 = 0.11
pZ3 = 0.11
pX1 = 0.11
pX2 = 0.11
pX3 = 0.11
pCNOT = 0.11
pTONC = 0.11
## make sure this adds up to less than 1.0!
## pId is whatever is left


# The intended meaning is : 
#   -- = identity or wire
#   HH = Hadamard
#   Z1 = S
#   Z2 = Z1 * Z1 = Z
#   Z3 = Z1 * Z1 * Z1 
#   X1 = HSH
#   X2 = X
#   X3 = can you guess?
#   CNOT = CNOT with the control on the top wire
#   TONC = CNOT with the control on the bottom wire.
# In the ascii drawings we have 
#   --CN--                   --TO--
#   --OT-- for the CNOT and  --NC-- for the TONC
# Easy to remember -- the one with the 'C' is the control!


#### You probably don't need to change anything below this line
#-------------------------------------------------------
# needs to be ordered by size (last coord)
gates = [
    (pHH, 'HH', 1),
    (pZ1, 'Z1', 1),
    (pZ2, 'Z2', 1),
    (pZ3, 'Z3', 1),
    (pX1, 'X1', 1),
    (pX2, 'X2', 1),
    (pX3, 'X3', 1),
    (pCNOT, 'CNOT', 2),
    (pTONC, 'TONC', 2)]


def nextGate (max_size=2) : 
    coin = random()
    acc = 0.0
    for g in [ h for h in gates if h[0] > 0.0]: 
        acc += g[0]
        if g[2] <= max_size :
            if acc > coin :
                return g
    return (1.0, '--', 1)


def genCirc (width, depth) :
    circ = [['' for x in range(depth)] for y in range(width)] 
    for d in xrange(depth) :
        w = 0
        while w < width :
            gate = nextGate(width-w)
            for s in sliced(gate[1],2) :
                circ[w][d] = s
                w += 1
    return circ

def prettyCirc(circ) :
    return "\n".join(map( (lambda wire : '-'.join(wire)), circ))

####--- JSON related stuff for quantomatic -----------------------

scale = 1.0   # for coords

json_gate = {
    'in' : {'annotation':{'boundary':True}},
    'ex' : {'annotation':{'boundary':True}},  # ex = exit = output
    '--' : {'annotation':{'boundary':False}},
    'CN' : {'data':{'type':'Z','value':''},'annotation':{}},
    'NC' : {'data':{'type':'Z','value':''},'annotation':{}},
    'OT' : {'data':{'type':'X','value':''},'annotation':{}},
    'TO' : {'data':{'type':'X','value':''},'annotation':{}},
    'HH' : {'data':{'type':'hadamard','value':''},'annotation':{}},
    'X1' : {'data':{'type':'X','value':'\\pi/2'},'annotation':{}},
    'X2' : {'data':{'type':'X','value':'\\pi'},'annotation':{}},
    'X3' : {'data':{'type':'X','value':'-\\pi/2'},'annotation':{}},
    'Z1' : {'data':{'type':'Z','value':'\\pi/2'},'annotation':{}},
    'Z2' : {'data':{'type':'Z','value':'\\pi'},'annotation':{}},
    'Z3' : {'data':{'type':'Z','value':'-\\pi/2'},'annotation':{}}
}

def vname(w,h) :
    return "v{0}_{1}".format(w,h)

def json_edge(w1,h1,w2,h2) : 
    return { 'src' : vname(w1,h1), 'tgt' : vname(w2,h2) }

def json_vertex(kind, x, y) :
    vert = deepcopy(json_gate[kind])
    vert['annotation']['coord'] = [x*scale,y*scale]
    return vert

def jsonifyCirc(circ) : 
    width = len(circ)
    depth = len(circ[0])
    nodes = {}
    edges = {}
    ename = lambda : "e{0}".format(len(edges))

    ins = { "in{0}".format(w) : json_vertex('in',-1,w) for w in xrange(width) }
    outs = { "out{0}".format(w) : json_vertex('ex',depth,w) for w in xrange(width) } 
    wires = dict(ins,**outs)

    for w in xrange(width) :
        edges[ename()] = {'src': "in{0}".format(w), 'tgt': vname(w,0)}
        for d in xrange(depth-1) : 
            edges[ename()] = json_edge(w,d,w,d+1)
        edges[ename()] = {'tgt': "out{0}".format(w), 'src': vname(w,depth-1)}

    for (w,d) in product(xrange(width),xrange(depth)) :
        g = circ[w][d]
        vertex = json_vertex(g,d,w)
        if g == '--' :
            wires[vname(w,d)] = vertex
        else :
            nodes[vname(w,d)] = vertex
        if g == 'CN' or g == 'TO' :
            edges[ename()] = json_edge(w,d,w+1,d)

    return json.dumps({'wire_vertices' : wires, 
                       'node_vertices' : nodes,
                       'undir_edges' : edges})


def parseArgs() :
    if len(sys.argv) > 1 : params['width'] = int(sys.argv[1])
    if len(sys.argv) > 2 : params['depth'] = int(sys.argv[2])
    if len(sys.argv) > 3 : params['number'] = int(sys.argv[3])
    if len(sys.argv) > 4 : params['prefix'] = sys.argv[4]
    

def main() : 
    parseArgs()
    if params['verbose'] :
        print 'HELLO!'
        print 'Random Clifford circuits are being created...'
    for i in xrange(params['number']) :
        filename_no_suffix = params['prefix'] + params['name'] + str(i+1) 
        circ = genCirc(params['width'],params['depth'])
        if params['verbose'] :
            print ""
            print "Generated : "
            print prettyCirc(circ)
        if params['JSON'] : 
            filename = filename_no_suffix + ".qgraph"
            if params['verbose'] : print "Writing file " + filename 
            jsonfile = open(filename,'w') 
            jsonfile.write(jsonifyCirc(circ))
            jsonfile.close()
        if params['ASCII'] : 
            filename = filename_no_suffix + ".txt"
            if params['verbose'] : print "Writing file " + filename 
            textfile = open(filename,'w')             
            textfile.write(prettyCirc(circ))
            textfile.close()
    
main()
