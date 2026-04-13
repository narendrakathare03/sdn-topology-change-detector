from  pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log=core.getLogger()

class MyController(object):
     def __init__(self, connection):
        self.connection=connection
        connection.addListeners(self)
        log.info("Controller connected to switch: %s" % dpidToStr(connection.dpid))
    
    def _handle_PacketIn(self, event):
       packet=event.parsed
       log.info("PacketIN from Switch %s port %s" % (dpidToStr(event.dpid), event.port))

       msg=of.ofp_packet_out()
       msg.data=event.ofp
       action=of.ofp_action_output(port=of.OFPP_FLOOD)
       msg.actions.append(action)
       self.connection.send(msg)


       flow_msg=of.ofp_flow_mod()
       flow_msg.match=of.ofp_match.from_packet(packet)
       flow_msg.idle_timeout=10
       flow_msg.hard_timeout=30
       flow_msg.priority=100
       flow_msg.actions.append(of.ofp_action_output(port=of.OFFP_FLOOD))
       self.connection.send(flow_msg)
       log.info("Flow rule installed")

def launch():
    def start_controller(event):
        MyController(event.connection)
    core.openflow.addListenerByName("Connectionup", start_controller)
    log.info("My SDN Contoller is running...")
