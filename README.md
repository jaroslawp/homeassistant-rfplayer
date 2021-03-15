Quick & dirty (and unfinished ...) copy & paste hack to 
get RFPlayer RFP1000 working on Home Assistant.

Most of the code is borrowed from HA rflink implementation 
(https://github.com/home-assistant/core/) and 
Domoticz RFplayer plugin (https://github.com/sasu-drooz/Domoticz-Rfplayer) 

Only Delta Dore X2D sensors data handling is implemented.


1. place custom_components/rfplayer in /root/config/custom_components/
2. Edit /root/config/configuration.yaml adding lines from configuration.yaml
3. Restart Home Assistant
4. Check log at /root/config/home-assistant.log



Example debug log output:

```    
2021-03-15 17:08:09 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] f:detecto
integration rfplayer which has not been tested by Home Assistant. This component might 
cause stability problems, be sure to disable it if you experience issues with Home Assi
stant

...

2021-03-15 16:52:57 INFO (MainThread) [homeassistant.setup] Setting up rfplayer
2021-03-15 16:52:57 INFO (MainThread) [homeassistant.setup] Setup of domain rfplayer took 0.0 seconds

...

2021-03-15 16:52:57 INFO (MainThread) [custom_components.rfplayer] Initiating Rfplayer connection
2021-03-15 16:52:57 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] CommandSerialization
2021-03-15 16:52:57 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] PacketHandling
2021-03-15 16:52:57 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] EventHandling
2021-03-15 16:52:57 INFO (MainThread) [custom_components.rfplayer] Connected to Rfplayer
2021-03-15 16:52:57 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] connected
2021-03-15 16:52:57 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] writing data: 'ZIA++HELLO\r\n'
2021-03-15 16:52:57 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] writing data: 'ZIA++RECEIVER + *\r\n'
2021-03-15 16:52:57 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] writing data: 'ZIA++FORMAT JSON\r\n'
2021-03-15 16:52:57 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] initialized

...

2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] received data: ZIA--Welcome to Ziblue Dongle RFPLAYER (RFP100
0, Firmware=V1.39 F=433Mhz & 868Mhz EU)!
.ZIA--RECEIVED PROTOCOLS: X10 RTS VISONIC BLYSS CHACON OREGONV1 OREGONV2 OREGONV3/OWL DOMIA X2D KD101 PARROT TIC FS20 EDISIO
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] got packet: ZIA--Welcome to Ziblue Dongle RFPLAYER (RFP1000, 
Firmware=V1.39 F=433Mhz & 868Mhz EU)!

2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] decoded packet: {'node': 'gateway', 'message': 'Welcome to Zi
blue Dongle RFPLAYER (RFP1000, Firmware=V1.39 F=433Mhz & 868Mhz EU)!\n'}
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] handle_packet
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] _handle_packet
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] ABBREV: {'status': 'sta', 'sensor': 'sen', 'detector': 'dtc', '
command': 'cmd', 'battery': 'bat'}
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] items: dict_items([('node', 'gateway'), ('message', 'Welcome to
 Ziblue Dongle RFPLAYER (RFP1000, Firmware=V1.39 F=433Mhz & 868Mhz EU)!\n')])
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] f:node,v:gateway
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] f:message,v:Welcome to Ziblue Dongle RFPLAYER (RFP1000, Firmwar
e=V1.39 F=433Mhz & 868Mhz EU)!

2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] got packet: ZIA--RECEIVED PROTOCOLS: X10 RTS VISONIC BLYSS CH
ACON OREGONV1 OREGONV2 OREGONV3/OWL DOMIA X2D KD101 PARROT TIC FS20 EDISIO

2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] decoded packet: {'node': 'gateway', 'message': 'RECEIVED PROT
OCOLS: X10 RTS VISONIC BLYSS CHACON OREGONV1 OREGONV2 OREGONV3/OWL DOMIA X2D KD101 PARROT TIC FS20 EDISIO\n'}
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] handle_packet
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] _handle_packet
2021-03-15 16:52:58 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] ABBREV: {'status': 'sta', 'sensor': 'sen', 'detector': 'dtc', '
command': 'cmd', 'battery': 'bat'}

...

2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] received data: ZIA33{ "frame" :{"header": {"frameType": "0", 
"cluster": "0", "dataFlag": "1", "rfLevel": "-88", "floorNoise": "-100", "rfQuality": "3", "protocol": "8", "protocolMeaning": "X2D", "infoTy
pe": "11", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "2916083969", "qualifier": "2", "quali
fierMeaning": { "flags": ["Alarm"]}, "d0": "55804", "d1": "0", "d2": "0", "d3": "0"}}}
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] got packet: ZIA33{ "frame" :{"header": {"frameType": "0", "cl
uster": "0", "dataFlag": "1", "rfLevel": "-88", "floorNoise": "-100", "rfQuality": "3", "protocol": "8", "protocolMeaning": "X2D", "infoType"
: "11", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "2916083969", "qualifier": "2", "qualifie
rMeaning": { "flags": ["Alarm"]}, "d0": "55804", "d1": "0", "d2": "0", "d3": "0"}}}

2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] decoded packet: {'node': 'gateway', 'protocol': 'x2d', 'id': 
'2916083969', 'detector': 'open'}
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] handle_packet
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] _handle_packet
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] ABBREV: {'status': 'sta', 'sensor': 'sen', 'detector': 'dtc', '
command': 'cmd', 'battery': 'bat'}
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] items: dict_items([('node', 'gateway'), ('protocol', 'x2d'), ('
id', '2916083969'), ('detector', 'open')])
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] f:node,v:gateway
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] f:protocol,v:x2d
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] f:id,v:2916083969
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] f:detector,v:open
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] event: detector -> open
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpparser] packet_events, sensor:detector,value:open
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] ignore_event
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer.rfpprotocol] got event: {'id': 'x2d_2916083969_dtc', 'sensor': 'detector',
 'value': 'open', 'unit': None}
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer] event of type sensor: {'id': 'x2d_2916083969_dtc', 'sensor': 'detector', 
'value': 'open', 'unit': None}
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer] entity_ids: ['sensor.x2d_2916083969_dtc'], type: sensor,event_id: x2d_291
6083969_dtc
2021-03-15 16:58:04 DEBUG (MainThread) [custom_components.rfplayer] passing event to sensor.x2d_2916083969_dtc

...
```
