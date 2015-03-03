__author__ = 'aaronhalbert'

from nimble import cmds

def fn(name, index):
    return name + str(index)

def createBar(name, index):
    ## actual standard gold bar dimensions (inches)
    y = 1.75
    x = 7.
    z = 3.63
    cmds.polyCube(h=y,w=x,d=z, n=fn(name,index))
    cmds.scale(.94, .9, fn(name,index) + '.f[1]', xz=True)
    cmds.move(y/4+.001,y=True, relative=True)
    cmds.scale(.5,.5,.5)
    cmds.polyBevel(fn(name,index), o=.07, sg=12)

def createSphere(name, index):
    cmds.polySphere(n=fn(name,index))
    cmds.move(1, y=True)

def createRing(name, index):
    cmds.polyCylinder(r=1.288, sx=48, n=fn('cyl', index))
    cmds.polyTorus(n=fn('torus', index), sx=48, sy=24)
    cmds.polyBoolOp(fn('torus',index), fn('cyl', index), op=2, n=fn(name,index))
    cmds.move(.407, y=True)

def main(name, index):
    if name == 'bar':
        createBar(name, index)
    elif name == 'sphere':
        createSphere(name, index)
    elif name == 'ring':
        createRing(name, index)