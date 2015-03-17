from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet,ethernet
import pprint

class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L2Switch,self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self,ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

#        pkt = packet.Packet(msg.data)
#        eth = pkt.get_protocols(ethernet.ethernet)[0]
#        dst = eth.dst
#        src = eth.src

#        dpid = dp.id
#       self.mac_to_port.setdefault(dpid, {})

        in_port = msg.match['in_port']
#       self.mac_to_port[dpid][src] = in_port

#       if dst in self.mac_to_port[dpid]:
#        out_port = self.mac_to_port[dpid][dst]
#       else:
#           out_port = ofproto.OFPP_FLOOD
        out_port = 1
        if in_port==out_port:
            out_port = 2
        else:
            out_port = 1
        actions = [ofp_parser.OFPActionOutput(out_port)]

        data = None
        if msg.buffer_id == ofp.OFP_NO_BUFFER:
            data = msg.data

        out = ofp_parser.OFPPacketOut(datapath=dp,
                                      buffer_id=msg.buffer_id,
                                      in_port=in_port,
                                      actions=actions,
                                      data=data)
        dp.send_msg(out)
