import rospy
from std_msgs.msg import String

def setup_talker():
    global pub
    pub = rospy.Publisher('kinefly/command', String, queue_size=10)
    rospy.init_node('cmdSender', anonymous=True)
    rate = rospy.Rate(10) # 10hz

def start_talking():
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish('record')
        rospy.sleep(5)

def command_callback(msg):
    command=msg.data
    rospy.loginfo(command)
    return


if __name__ == '__main__':
    try:
        setup_talker()
        subCommand     = rospy.Subscriber('kinefly/command',   String, command_callback, queue_size=1000)
        start_talking()
    except rospy.ROSInterruptException:
        pass
