__author__ = 'aaronhalbert'

from nimble import cmds
import random
import time

# Create a sphere, with 10 subdivisions in the X direction,
# and 15 subdivisions in the Y direction,
# the radius of the sphere is 20.

def createBubble(tx, tz, name):
    """
    :param tx: translate x value
    :param tz: translate z value
    :param name: string name of bubble
    :return: nothing
    """
    cmds.polySphere(sx=15, sy=15, r=.1, n=name)
    cmds.move(tx,0,tz, name, absolute=True)

def main(bubbleQuantity, allAtts):
    for i in range(bubbleQuantity): # create 50 bubbles
        name = 'bubble' + str(i) # name them sequentially

        """
        first -- a random integer between 1 and 50
        which represents the keyframe in which a
        bubble is generated
        """
        first = random.randint(1,300)

        last = first + 66 # all bubbles take 66 keyframes to rise
        x = 10 - random.random()*20 # this makes x values in the range [-10.0,10.0]
        z = 10 - random.random()*20 # this makes z values in the range [-10.0,10.0]
        createBubble(x,z,name)
        cmds.currentTime(first)

        cmds.setKeyframe( name, v=1, at='visibility' )
        cmds.setKeyframe(name)
        cmds.currentTime(last)

        ############ keyframe all attributes ############
        if allAtts:
            cmds.scale(10,10,10, name)
            cmds.move(0, 20, 0, name, relative=True)
            cmds.setKeyframe()
        #################################################

        ####### keyframe only necessary attributes ######
        else:
            cmds.setKeyframe( name, v=10, at='scaleX' )
            cmds.setKeyframe( name, v=10, at='scaleY' )
            cmds.setKeyframe( name, v=10, at='scaleZ' )
            cmds.setKeyframe( name, v=10, at='translateY' )
        #################################################

        cmds.currentTime(last + 1)
        cmds.setKeyframe( name, v=0, at='visibility' )
    cmds.currentTime(1)
    # cmds.select(all=True)
    # cmds.delete()

if __name__ == "__main__":
    # start = time.time()
    # for i in range(5):
    #     main(250, True)
    #     print(str(i + 1) + " iterations of \"all attributes\" test completed")
    # print("All attributes keyframed, completed on average in " + str((time.time() - start)/5) + " seconds.")
    # start = time.time()
    # for i in range(5):
    #     main(250, False)
    #     print(str(i + 1) + " iterations of \"selected attributes\" test completed")
    # print("Selected attributes keyframed, completed on average in " + str((time.time() - start)/5) + " seconds.")
    main(300, True)