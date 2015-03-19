from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet,ethernet
import pprint

class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(L2Switch,self).__init__(*args, **kwargs)
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        self.send_port_desc_stats_request(datapath)
        print("send_port_desc_stats_request")


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self,ev):
        pass

    def send_port_desc_stats_request(self, datapath):
        ofp_parser = datapath.ofproto_parser
        req = ofp_parser.OFPPortDescStatsRequest(datapath, 0)
        datapath.send_msg(req)
        print("OFPPortDescStatsRequest")

    def add_flow(self, datapath, in_port, instructions):
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        match = ofp_parser.OFPMatch(in_port)
        flow = ofp_parser.OFPFlowMod(datapath=datapath,
                                 match=match,
                                 cookie=0,
                                 command=ofproto.OFPFC_ADD,
                                 instructions=instructions)
        datapath.send_msg(flow)

    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_desc_stats_reply_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        ports = []
        for p in ev.msg.body:
            if p.port_no < 100:
                ports.append("%d" % (p.port_no))
        action = [datapath.ofproto_parser.OFPActionOutput(int(ports[1]))]
        instructions = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,action)]
        self.add_flow(datapath,int(ports[0]),instructions)
        action = [datapath.ofproto_parser.OFPActionOutput(int(ports[0]))]
        instructions = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,action)]
        self.add_flow(datapath,int(ports[1]),instructions)
