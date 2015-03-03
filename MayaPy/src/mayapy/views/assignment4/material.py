__author__ = 'aaronhalbert'

from nimble import cmds

def assignGoldShader(name):
    selected = cmds.ls(sl=True)[0].encode('ascii','ignore')
    print(selected)
    cmds.sets( name='goldMaterialGroup', renderable=True, empty=True )
    cmds.shadingNode( 'anisotropic', name='goldShader', asShader=True )
    cmds.setAttr( 'goldShader.color', 1, .775814, 0, type='double3' )
    cmds.setAttr( 'goldShader.specularColor', 1, 1, 1, type='double3' )
    cmds.setAttr( 'goldShader.diffuse', .475 )
    cmds.setAttr( 'goldShader.translucence', .263)
    cmds.setAttr( 'goldShader.translucenceFocus', .869)
    cmds.setAttr( 'goldShader.spreadX', 5 )
    cmds.setAttr( 'goldShader.spreadY', 24 )
    cmds.setAttr( 'goldShader.roughness', .75 )
    cmds.setAttr( 'goldShader.fresnelRefractiveIndex', 9.227 )
    cmds.surfaceShaderList( 'goldShader', add='goldMaterialGroup' )
    cmds.sets( selected, e=True, forceElement='goldMaterialGroup' )
    return name

def assignPlasticShader(name):
    selected = cmds.ls(sl=True)[0].encode('ascii','ignore')
    print(selected)
    cmds.sets( name='plasticMaterialGroup', renderable=True, empty=True )
    cmds.shadingNode( 'blinn', name='plasticShader', asShader=True )
    cmds.setAttr( 'plasticShader.color', .667628, 0., 1., type='double3')
    cmds.setAttr( 'plasticShader.diffuse', .5 )
    cmds.setAttr( 'plasticShader.eccentricity',.5 )
    cmds.surfaceShaderList( 'plasticShader', add='plasticMaterialGroup' )
    cmds.sets( selected, e=True, forceElement='plasticMaterialGroup' )
    return name

def main(name, type):
    if type == 'gold':
        return assignGoldShader(name)
    elif type == 'plastic':
        return assignPlasticShader(name)
