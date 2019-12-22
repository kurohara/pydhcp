""" Base DHCP backend """

import sys
import logging

logger = logging.getLogger(__name__)

BACKENDS = {}


class DHCPBackendMeta(type):
    """ Register Backend classes in the library """

    def __new__(cls, clsname, bases, attrs):
        newclass = super().__new__(cls, clsname, bases, attrs)
        BACKENDS[clsname] = newclass
        return newclass


class DHCPBackend(metaclass=DHCPBackendMeta):
    """ Base DHCP backend """

    DISABLED = False

    @property
    def NAME(self):  # pylint: disable=invalid-name
        """ Return a default name property """
        return self.__class__.__name__

    def offer(self, packet):
        """ Generate an offer in response to a DISCOVER """
        raise NotImplementedError()

    def acknowledge(self, packet, offer):
        """ Generate an ACKNOWLEGE response to a REQUEST """
        raise NotImplementedError()

    def release(self, packet):
        """ Process a release """
        raise NotImplementedError()

    def pxe_boot_request(self, packet, lease):
        """ Add pxe boot options to a lease """

    def uefi_boot_request(self, packet, lease):
        """ Add UEFI boot options to a lease """


def get_backend(name):
    """ Retrive the enabled backend `name` """

    if name in BACKENDS:
        if BACKENDS[name].DISABLED:
            logger.error("Backend %s is DISABLED: %s", name,
                         BACKENDS[name].DISABLED)
            sys.exit(1)
        else:
            return BACKENDS[name]

    logger.error("Backend %s is unknown", name)
    sys.exit(1)
