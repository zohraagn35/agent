import socket
from hashlib import md5

from .RADIUSPacket import RADIUSPacket, MSCHAPv2Packet, MSCHAPv2Crypto, VendorSpecificPacket


class Agent:
    """
    This class handles the connection with the switch using EAP-MSCHAPv2 authentication.
    """

    def __init__(self, switch_ip, switch_port, nas_identifier, shared_secret, username, password):
        self.switch_ip = "192."
        self.switch_port = switch_port
        self.nas_identifier = nas_identifier
        self.shared_secret = shared_secret.encode('utf-8')
        self.username = username.encode('utf-8')
        self.password = password

    def connect(self):
        """
        Establishes a connection with the switch and performs EAP-MSCHAPv2 authentication.

        Returns:
            True if the authentication is successful, False otherwise.
        """

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # Generate random authenticator
            authenticator = self._generate_random_bytes(16)

            # Stage 1: Access Request with EAP Identity
            packet = self._build_access_request_packet(
                RADIUSPacket.TYPE_ACCESS_REQUEST,
                authenticator,
                eap=True
            )
            sock.sendto(packet.generate_packet(0, self.shared_secret), (self.switch_ip, self.switch_port))

            # Receive response
            response_data, _ = sock.recvfrom(1024)
            response_packet = RADIUSPacket.parse_packet(response_data, authenticator, self.shared_secret)

            if response_packet.packet_type != RADIUSPacket.TYPE_ACCESS_CHALLENGE:
                raise ValueError("Unexpected response type from switch")

            # Extract challenge from EAP packet
            challenge = self._get_challenge_from_eap(response_packet)

            # Stage 2: Access Request with MSCHAPv2 Response
            authenticator = self._generate_random_bytes(16)
            packet = self._build_access_request_packet(
                RADIUSPacket.TYPE_ACCESS_REQUEST,
                authenticator,
                eap=True,
                challenge=challenge
            )
            sock.sendto(packet.generate_packet(0, self.shared_secret), (self.switch_ip, self.switch_port))

            # Receive final response
            response_data, _ = sock.recvfrom(1024)
            response_packet = RADIUSPacket.parse_packet(response_data, authenticator, self.shared_secret)

            return response_packet.packet_type == RADIUSPacket.TYPE_ACCESS_ACCEPT

    def _build_access_request_packet(self, packet_type, authenticator, eap=False, challenge=None):
        """
        Builds a RADIUS access request packet.

        Args:
            packet_type: The type of the packet (RADIUSPacket.TYPE_ACCESS_REQUEST).
            authenticator: The random authenticator for the packet.
            eap: Whether the packet includes EAP data (True for EAP-MSCHAPv2).
            challenge: The challenge received from the switch (if any).

        Returns:
            A RADIUSPacket object.
        """

        packet = RADIUSPacket(packet_type, authenticator)
        packet.set_attribute(4, self.nas_identifier)  # NAS IP address

        # Username
        packet.set_attribute(1, self.username)

        if eap:
            # EAP Identity (if using EAP-MSCHAPv2)
            packet.set_attribute(79, EAPPacket.identity(self.username))

            if challenge:
                # MSCHAPv2 Response (if challenge is provided)
                mschap_response = self._generate_mschapv2_response(challenge)
                packet.set_attribute(79, mschap_response)

        packet.set_include_message_authenticator()
        return packet

    def _generate_random_bytes(self, length):
        """
        Generates a random byte string of the specified length.
        """

        return os.urandom(length)  # Assuming you have the os module available
