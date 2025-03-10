import snap7
from snap7.util import get_string, get_real, set_real
from snap7.type import Areas
from typing import Union, Literal


class Client:
    def __init__(self):
        """Creates a Siemens Snap7 Server"""
        self.client = snap7.client.Client()
        return

    def connect(self, ip_address: str = '127.0.0.1', port_num: int = 24565):
        """
        Connects to Siemens Snap7 server at ip_address and port_num.

        :param ip_address: IP address of server.
        :param port_num: Port number.
        :return: 1 if connection is successful; otherwise 0.
        """
        try:
            self.client.connect(ip_address, 0, 1, port_num)  # Use the port number specified in the server
        except Exception as e:
            print(f"Failed to connect to the client: {e}")
            return 0

        print(f"Connected to the client at IP:{ip_address} | port:{port_num}")
        return 1

    def inject(self, inject_value: float, db_number: int = 1, db_start: int = 0):
        """
        Injects inject_value to the server starting at position db_start \
        in the Siemens Snap7 Server database block db_number.

        :param inject_value: Value to inject.
        :param db_number: Database block number.
        :param db_start: Database write start position.
        :return: 1 if successful; otherwise 0.
        """
        # Write data to the server
        data_to_write = bytearray(4)
        set_real(data_to_write, 0, inject_value)

        try:
            self.client.write_area(area=Areas.PE,
                                   db_number=db_number,
                                   start=db_start,
                                   data=data_to_write)
        except Exception as e:
            print(f"Failed to inject to client: {e}")
            return 0

        return 1

    def sniff(self, data_type: Union[Literal['str'], Literal['real']] = 'real',
              snap7_area: Union[Literal[Areas.PA], Literal[Areas.DB]] = Areas.PA,
              db_number=1, start_pos=0, num_chars=4):
        """
        Reads data from Siemens Snap7 server.

        :param snap7_area: Database type.
        :param data_type: Data type to read.
        :param db_number: Database number.
        :param start_pos: Database read start position.
        :param num_chars: Number of characters (bytes) to read.
        :return: Read value if successful; otherwise 0.
        """
        # Read data from the server
        try:
            data_read = self.client.read_area(area=snap7_area,
                                              db_number=db_number,
                                              start=start_pos,
                                              size=num_chars)

            if data_type == 'real':
                value = get_real(data_read, 0)
            else:
                value = get_string(data_read, 0)

            print(f"Read data from server: {value}")
        except Exception as e:
            print(f"Failed to read from client: {e}")
            return 0

        return value

    def disconnect(self):
        """Disconnect the client."""
        self.client.disconnect()
        return


if __name__ == "__main__":
    client = Client()
    client.connect('18.118.186.100')
