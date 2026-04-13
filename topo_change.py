from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
import time

log = core.getLogger()
topology_map = {}

class TopologyChangeDetector(object):
    def __init__(self, connection):
        self.connection = connection
        self.dpid = connection.dpid
        connection.addListeners(self)
        topology_map[self.dpid] = {
            'ports': [],
            'connected_at': time.strftime("%H:%M:%S")
        }
        log.info("Switch %s connected at %s" % (
            dpidToStr(self.dpid),
            topology_map[self.dpid]['connected_at']))
        self.display_topology()

    def _handle_PacketIn(self, event):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        action = of.ofp_action_output(port=of.OFPP_FLOOD)
        msg.actions.append(action)
        self.connection.send(msg)
        flow_msg = of.ofp_flow_mod()
        flow_msg.match = of.ofp_match.from_packet(
            event.parsed)
        flow_msg.idle_timeout = 10
        flow_msg.hard_timeout = 30
        flow_msg.priority = 100
        flow_msg.actions.append(
            of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(flow_msg)

    def _handle_PortStatus(self, event):
        port = event.port
        if event.added:
            reason = "ADDED"
            if port not in topology_map[self.dpid]['ports']:
                topology_map[self.dpid]['ports'].append(port)
        elif event.deleted:
            reason = "DELETED"
            if port in topology_map[self.dpid]['ports']:
                topology_map[self.dpid]['ports'].remove(port)
        elif event.modified:
            reason = "MODIFIED"
        else:
            reason = "UNKNOWN"
        log.info("*** TOPOLOGY CHANGE DETECTED ***")
        log.info("Switch : %s" % dpidToStr(self.dpid))
        log.info("Port   : %s | Event: %s" % (port, reason))
        log.info("Time   : %s" % time.strftime("%H:%M:%S"))
        self.display_topology()

    def display_topology(self):
        log.info("=== Current Topology Map ===")
        for dpid, info in topology_map.items():
            log.info("Switch %s | Ports: %s | Since: %s" % (
                dpidToStr(dpid),
                info['ports'],
                info['connected_at']))
        log.info("============================")

def launch():
    def start_detector(event):
        TopologyChangeDetector(event.connection)
    core.openflow.addListenerByName(
        "ConnectionUp", start_detector)
    log.info("Topology Change Detector is running...")
