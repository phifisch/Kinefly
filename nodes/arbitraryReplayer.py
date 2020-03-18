#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32, Header, String
from Kinefly.msg import MsgFlystate, MsgState
#from numpy import array
import pdb

flystate_priorities = ['left','right','abdomen','head','aux']

class Replayer:
    def __init__(self,*args,**kwargs):
        self.nodename = 'kinefly'
        #self.nodename = rospy.get_name().rstrip('/')
        self.filename = self.getFilename()
        self.valueGenerator = self.valueGenerator_fromfile()
        self.iCount = 0

        rospy.init_node('replayer', anonymous=True)
        self.namespace = rospy.get_namespace()

        #self.flystate = MsgFlystate()
        #self.flystate.header = Header(seq=0, stamp=rospy.Time.now(), frame_id='Fly')
        #self.flystate.header = Header(seq=self.iCount, frame_id='Fly')
        #self.flyBodyparts = [ eval('flystate.'+bodypart) for bodypart in flystate_priorities ]
        #self.neutralValue = 0.
        #self.neutralMsgState = MsgState()
        self.pubFlystate = rospy.Publisher(self.namespace.rstrip('/')+'/flystate', MsgFlystate, queue_size=100)


    def getFilename(self):
        return "/home/schnell_la/catkin/src/Kinefly/nodes/replayValues.txt"

    def valueGenerator_fromfile(self):
        with open(self.filename,'r') as f:
            content = f.read()
        content = content.split()
        content = [c for c in content if c] #remove empty strings from list
        """
        #WTF this was way to complicated, no closures needed, generator keeps variables anyways
        outeri=0
        def generateValues_fromfile():
            i=outeri
            while True:
                yield [float(val) for val in content[i].split(',') ]
                i+=1
                #endlessly looping from beginning
                if i==len(content):
                    i=0
        gen = generateValues_fromfile
        return gen()
        """
        #instead create generator in main "function"
        i=0
        while True:
            yield [float(val) for val in content[i].split(',') ]
            i+=1
            #endlessly looping from beginning
            if i==len(content):
                i=0
        #end of generator fucntion

    def publish(self):
        vals = next(self.valueGenerator)
        flystate = MsgFlystate()
        #pdb.set_trace()
        #set the attributes of flystate according to priorities and with correct datatype
        for i in range(5):
            setattr(flystate, flystate_priorities[i], MsgState() )
            if i>=len(vals):
                continue
            else:
                setattr(getattr(flystate, flystate_priorities[i]), 'angles', [vals[i],vals[i]])
                setattr(getattr(flystate, flystate_priorities[i]), 'radii', [1.])

        flystate.header = Header(seq=float(self.iCount), stamp=rospy.Time.now(), frame_id='Fly')

        #vals.extend(([MsgState()]*(5-len(vals))))
        """flystate.left.angles = [vals[0],vals[0]]
        flystate.left.radii = [0.1]
        flystate.right.angles = [vals[1],vals[1]]
        flystate.right.radii = [0.5]
        flystate.abdomen = [vals[2]]
        flystate.head = vals[3]
        flystate.aux = vals[4]
        """
        self.iCount+=1
        self.pubFlystate.publish(flystate)
        self.valProvider.publish('      '.join([str(v) for v in vals]))

    def run(self):
        self.valProvider = rospy.Publisher("/replayer/values", String, queue_size=100)
        r=rospy.Rate(50)
        while not rospy.is_shutdown():
            self.publish()
            r.sleep()


if __name__=="__main__":
    rp=Replayer()
    rp.run()
