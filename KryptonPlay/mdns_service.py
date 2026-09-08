"""Local mDNS advertisement for the approved KryptonPlay address."""
from __future__ import annotations

import ipaddress
import logging
import socket
from typing import Optional

from zeroconf import ServiceInfo, Zeroconf

logger = logging.getLogger("kryptonplay.mdns")

HOSTNAME = "kryptonplay.local."
SERVICE_TYPE = "_http._tcp.local."
SERVICE_NAME = "KryptonPlay._http._tcp.local."


def _local_address(network_access: str) -> str:
    if network_access != "lan":
        return "127.0.0.1"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return str(sock.getsockname()[0])
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


class LocalDiscovery:
    def __init__(self) -> None:
        self._zeroconf: Optional[Zeroconf] = None
        self._service: Optional[ServiceInfo] = None

    def start(self, port: int, network_access: str = "local") -> None:
        address = _local_address(network_access)
        try:
            info = ServiceInfo(
                SERVICE_TYPE,
                SERVICE_NAME,
                addresses=[ipaddress.ip_address(address).packed],
                port=int(port),
                server=HOSTNAME,
                properties={b"path": b"/", b"product": b"KryptonPlay"},
            )
            self._zeroconf = Zeroconf()
            self._zeroconf.register_service(info, allow_name_change=False)
            self._service = info
            logger.info("mDNS ativo: http://%s:%s (%s)", HOSTNAME.rstrip("."), port, address)
        except Exception:
            logger.exception("Não foi possível iniciar a descoberta mDNS.")
            self.close()

    def close(self) -> None:
        if self._zeroconf is not None:
            try:
                if self._service is not None:
                    self._zeroconf.unregister_service(self._service)
            except Exception:
                logger.exception("Falha ao remover o anúncio mDNS.")
            try:
                self._zeroconf.close()
            except Exception:
                logger.exception("Falha ao encerrar mDNS.")
        self._service = None
        self._zeroconf = None
