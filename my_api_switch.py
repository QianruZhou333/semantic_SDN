################################
# @author: Qianru Zhou
# @email: chowqianru@gmail.com
# All rights reserved
#################################

from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.lib import dpid as dpid_lib
import ryu.app.ofctl.api as api

class SwitchAPI(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self):
        super(SwitchAPI, self).__init__()

    def add_flow(self, datapath, priority, in_port, eth_dst, actions, buffer_id):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        if in_port & eth_dst:
            match = parser.OFPMatch(in_port=in_port, eth_dst=eth_dst)

        # OFPFlowMod will add flow by default. command = ofproto.OFPFC_ADD.
        mod = parser.OFPFlowMod(datapath=datapath, command=ofproto.OFPFC_ADD,
                                buffer_id=buffer_id,
                                priority=priority, match=match,
                                instructions=inst)
        return mod

    def delete_flow(self, datapath, priority, in_port, eth_dst, actions, buffer_id):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        if in_port & eth_dst:
            match = parser.OFPMatch(in_port=in_port, eth_dst=eth_dst)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=datapath, command = ofproto.OFPFC_DELETE,
                          buffer_id=buffer_id, priority = priority,
                          match = match, instrunctions = inst)
        return mod

    def dump_all_switches(self):
        self.get_switch_by_id()

    def get_switch_by_id(self, **kwargs):
        if 'dpid' in kwargs:
            dpid = dpid_lib.str_to_dpid(kwargs['dpid'])
        switches = api.get_datapath(self, dpid)
        body = json.dumps([switch.to_dict() for switch in switches])
        return Response(content_type='application/json', body=body)
