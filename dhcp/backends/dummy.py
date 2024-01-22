import os
import logging
import ipaddress
from datetime import datetime, timedelta, timezone

from dhcp.backends.base import DHCPBackend
from dhcp.lease import Lease
from dhcp.packet import PacketOption
from dhcp.settings import SETTINGS

class DummyBackend(DHCPBackend):
    """ Base DHCP backend """

    NAME = "dummy"

    _API_VERSION = None
    _IPADDRESS_DHCP_STATUS = "dhcp"
    
    DISABLED = False

    def __init__(self, url=None, token=None, allow_unknown_devices=False, lease_time=None):
        # self.url = url or SETTINGS.netbox_url or os.getenv("NETBOX_URL", None)
        # self.token = token or SETTINGS.netbox_token or os.getenv("NETBOX_TOKEN", None)
        # self.lease_time = lease_time or SETTINGS.lease_time or \
        #     int(os.getenv("PYDHCP_LEASE_TIME", "3600"))
        # self.allow_unknown_devices = allow_unknown_devices or \
        #     SETTINGS.netbox_allow_unknown_devices or \
        #     os.getenv("NETBOX_ALLOW_UNKNOWN_DEVICES", "false").lower() == "true"

        # if not self.url and self.token:
        #     raise RuntimeError("url and token required for netbox backend")

        self._client = None
        
    def offer(self, packet):
        """ Generate an offer in response to a DISCOVER """
        raise NotImplementedError()

    def acknowledge(self, packet, offer):
        """ Generate an ACKNOWLEGE response to a REQUEST """
        raise NotImplementedError()

    # Implementations MAY CHOOSE to implement specific behavior for some of the specific
    # client states that generate a DHCP request, non implemented states fall back to
    # the generic acknowledge.  If all are implemented there is no need to implement
    # acknowledge
    def acknowledge_selecting(self, packet, offer):
        """ Generate an ACKNOWLEGE response to a REQUEST from a client in SELECTING state """
        return self.acknowledge(packet, offer)

    def acknowledge_renewing(self, packet, offer):
        """ Generate an ACKNOWLEGE response to a REQUEST from a client in RENEWING state """
        return self.acknowledge(packet, offer)

    def acknowledge_rebinding(self, packet, offer):
        """ Generate an ACKNOWLEGE response to a REQUEST from a client in REBINDING state """
        return self.acknowledge(packet, offer)

    def acknowledge_init_reboot(self, packet, offer):
        """ Generate an ACKNOWLEGE response to a REQUEST from a client in INITREBOOT state """
        return self.acknowledge(packet, offer)

    def release(self, packet):
        """ Process a release """
        raise NotImplementedError()

    def boot_request(self, packet, lease):
        """ Add boot options to the lease """

