from abc import ABC, abstractmethod


class BaseBlocklist(ABC):
    @abstractmethod
    def add(self, ip):
        """Set IP to blocklist"""

    def check(self, ip) -> bool:
        """Check if IP is in blocklist"""

    def remove(self, ip):
        """Remove from blocklist"""


class SimpleBlocklist(BaseBlocklist):
    def __init__(self):
        self.storage = set()

    def add(self, ip):
        self.storage.add(ip)

    def check(self, ip) -> bool:
        return ip in self.storage

    def remove(self, ip):
        try:
            self.storage.remove(ip)
        except KeyError:
            pass
