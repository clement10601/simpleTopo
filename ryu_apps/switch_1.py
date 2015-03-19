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

    def add_flow(self, datapath, in_port,eth_dst, instructions):

        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        match = ofp_parser.OFPMatch(in_port=in_port)
        cookie = cookie_mask = 0
        table_id = 0
        idle_timeout = hard_timeout = 0
        priority = 32768
        buffer_id = ofproto.OFP_NO_BUFFER

        flow = ofp_parser.OFPFlowMod(datapath,
                                 cookie,cookie_mask,
                                 table_id,ofproto.OFPFC_ADD,
                                 idle_timeout,hard_timeout,
                                 priority,buffer_id,
                                 ofproto.OFPP_ANY,ofproto.OFPG_ANY,
                                 ofproto.OFPFF_SEND_FLOW_REM,
                                 match,
                                 instructions=instructions)
        print(flow)
        ini = datapath.send_msg(flow)
        print(ini)

    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_desc_stats_reply_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        ports = []
        macs =[]
        for p in ev.msg.body:
            if p.port_no < 100:
                ports.append("%d" % (p.port_no))
                macs.append("%s" % (p.hw_addr))
        print(ports)
        action = [datapath.ofproto_parser.OFPActionOutput(int(ports[1],0))]
        instructions = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,action)]
        print(action)
        print(instructions)
        self.add_flow(datapath,int(ports[0]),macs[0],instructions)

        action = [datapath.ofproto_parser.OFPActionOutput(int(ports[0],0))]
        instructions = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,action)]
        print(action)
        print(instructions)
        self.add_flow(datapath,int(ports[1]),macs[1],instructions)
