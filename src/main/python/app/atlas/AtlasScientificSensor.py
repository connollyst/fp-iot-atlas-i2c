import json

from .AtlasScientificSensorReading import AtlasScientificSensorReading
from ..comms.IO import IO


class AtlasScientificSensor:
    # Timeout needed to query readings and calibrations
    LONG_TIMEOUT = 1.5
    # Timeout for regular commands
    SHORT_TIMEOUT = .3

    NAME_COMMAND = 'name,?'
    INFO_COMMAND = 'I'
    READ_COMMAND = 'R'

    def __init__(self, address, io: IO):
        self._address = address
        self._io = io
        name = self._io.send_and_receive(address, self.NAME_COMMAND, self.SHORT_TIMEOUT)
        print('> {}: {}'.format(self.NAME_COMMAND, name))
        info = self._io.send_and_receive(address, self.INFO_COMMAND, self.SHORT_TIMEOUT)
        print('> {}     : {}'.format(self.INFO_COMMAND, info))
        try:
            self._name = name.split(",")[1]
        except IndexError:
            # TODO do better than this!
            self._name = 'Err'
        try:
            self._module = info.split(",")[1]
        except IndexError:
            # TODO do better than this!
            self._module = info
        try:
            self._version = info.split(",")[2]
        except IndexError:
            # TODO do better than this!
            self._version = 'Err'

    @property
    def address(self):
        return self._address

    @property
    def name(self):
        return self._name

    @property
    def module(self):
        return self._module

    @property
    def version(self):
        return self._version

    def take_reading(self) -> AtlasScientificSensorReading:
        # TODO store reading
        # TODO support multiple readings
        return AtlasScientificSensorReading(
            self._io.send_and_receive(self.address, self.READ_COMMAND, self.LONG_TIMEOUT))

    def to_json(self) -> str:
        # TODO I don't like this side affect
        reading = self.take_reading()
        message = {
            'name': self.name,
            'module': self.module,
            'version': self.version,
            'address': self.address,
            'addressType': 'I2C',
            'reading': {
                'value': reading.value,
                'timestamp': reading.timestamp
            }
        }
        # TODO necessary to replace still?
        return json.dumps(message, indent=4, default=str).replace(r'\u0000', '')

    def __str__(self) -> str:
        if self._name == '':
            return self._module + ' ' + str(self.address)
        else:
            return self._module + ' ' + str(self.address) + ' ' + self._name