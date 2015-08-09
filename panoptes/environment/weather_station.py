import datetime
import zmq

from . import monitor
from ..utils.logger import has_logger

@has_logger
class WeatherStation(monitor.EnvironmentalMonitor):

    """
    This object is used to determine the weather safe/unsafe condition. It inherits
    from the monitor.EnvironmentalMonitor base class. It listens on the 'weather'
    channel of the messaging system.

    Config:
        weather_station.port (int): Port to publish to. Defaults to 6500
        weather_station.channel (str): the channel topic to publish on. Defaults to 'weather'

    Args:
        messaging (panoptes.messaging.Messaging): A messaging Object for creating new
            sockets.
    """

    def __init__(self, config=None, name="Weather Station", messaging=None, connect_on_startup=False):
        super().__init__(config=config, messaging=messaging, name='WeatherStation')

        # Get the messaging information
        self.port = self.config.get('messaging').get('port', 6500)
        self.channel = self.config.get('messaging').get('channel', 'weather')

        # Create our Publishing socket
        self.socket = self.messaging.create_subscriber(port=self.port, channel=self.channel)

        if connect_on_startup:
            self.start_monitoring()

    def monitor(self):
        """
        Reads serial information off the attached weather station
        """
        msg = self.socket.recv_json()
