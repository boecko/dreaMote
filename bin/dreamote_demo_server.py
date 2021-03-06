#!/bin/python
# -*- coding: UTF-8 -*-
####
# Simple Demo Server for dreaMote, powered by twisted web
# Currently supports most e2 functionality also present in dreaMote, and parts
# of the e1 and neutrino functionality are supported.
# Eventually this should properly emulate all used functionality of the
# HTTP based backends.
# Given that VDR does not require extra hardware for testing and is not based
# on HTTP as the other systems, it will not be included here.
####


from twisted.web import server, resource
from twisted.internet import reactor
import time

# changes api to retrieve services
# 0: recent enigma
# 1: older enigma (/xml/getservices), current document style
# 2: older enigma (/xml/getservices), old document style
# 3: old enigma (/xml/getServices), old document style
EMULATE_OLD_E1 = 0

# emulate neutrino hd
EMULATE_NEUTRINOHD = False

### DOCUMENTS
GETCURRENT = (
# (standby)
"""<e2currentserviceinformation>
	<e2service>
		<e2servicereference></e2servicereference>
		<e2servicename></e2servicename>
		<e2providername></e2providername>
		<e2videowidth></e2videowidth>
		<e2videoheight></e2videoheight>
		<e2servicevideosize>x</e2servicevideosize>
		<e2iswidescreen></e2iswidescreen>
		<e2apid></e2apid>
		<e2vpid></e2vpid>
		<e2pcrpid></e2pcrpid>
		<e2pmtpid></e2pmtpid>
		<e2txtpid></e2txtpid>
		<e2tsid></e2tsid>
		<e2onid></e2onid>
		<e2sid></e2sid>
	</e2service>
	<e2eventlist>
		<e2event>
			<e2eventservicereference></e2eventservicereference>
			<e2eventservicename></e2eventservicename>
			<e2eventprovidername></e2eventprovidername>
			<e2eventid></e2eventid>
			<e2eventname></e2eventname>
			<e2eventtitle></e2eventtitle>
			<e2eventdescription></e2eventdescription>
			<e2eventstart></e2eventstart>
			<e2eventduration></e2eventduration>
			<e2eventremaining></e2eventremaining>
			<e2eventcurrenttime>%(now).2f</e2eventcurrenttime>
			<e2eventdescriptionextended></e2eventdescriptionextended>
		</e2event>
		<e2event>
			<e2eventservicereference></e2eventservicereference>
			<e2eventservicename></e2eventservicename>
			<e2eventprovidername></e2eventprovidername>
			<e2eventid></e2eventid>
			<e2eventname></e2eventname>
			<e2eventtitle></e2eventtitle>
			<e2eventdescription></e2eventdescription>
			<e2eventstart></e2eventstart>
			<e2eventduration></e2eventduration>
			<e2eventremaining></e2eventremaining>
			<e2eventcurrenttime>%(now).2f</e2eventcurrenttime>
			<e2eventdescriptionextended></e2eventdescriptionextended>
		</e2event>
	</e2eventlist>
</e2currentserviceinformation>
""",
# (livetv)
"""<?xml version="1.0" encoding="UTF-8"?>
<e2currentserviceinformation>
	<e2service>
		<e2servicereference>1:0:1:445D:453:1:C00000:0:0:0:</e2servicereference>
		<e2servicename>DemoService</e2servicename>
		<e2providername>DemoProvider</e2providername>
		<e2videowidth>720</e2videowidth>
		<e2videoheight>576</e2videoheight>
		<e2servicevideosize>720x576</e2servicevideosize>
		<e2iswidescreen></e2iswidescreen>
		<e2apid>512</e2apid>
		<e2vpid>511</e2vpid>
		<e2pcrpid>511</e2pcrpid>
		<e2pmtpid>97</e2pmtpid>
		<e2txtpid>33</e2txtpid>
		<e2tsid>1107</e2tsid>
		<e2onid>1</e2onid>
		<e2sid>17501</e2sid>
	</e2service>
	<e2eventlist>
		<e2event>
			<e2eventservicereference>1:0:1:445D:453:1:C00000:0:0:0:</e2eventservicereference>
			<e2eventservicename>DemoService</e2eventservicename>
			<e2eventprovidername>DemoProvider</e2eventprovidername>
			<e2eventid>45183</e2eventid>
			<e2eventname>Demo Eventname</e2eventname>
			<e2eventtitle>Demo Eventname</e2eventtitle>
			<e2eventdescription>Event Short description</e2eventdescription>
			<e2eventstart>%(start_now).2f</e2eventstart>
			<e2eventduration>1560</e2eventduration>
			<e2eventremaining>1381</e2eventremaining>
			<e2eventcurrenttime>%(now).2f</e2eventcurrenttime>
			<e2eventdescriptionextended>Event description</e2eventdescriptionextended>
		</e2event>
		<e2event>
			<e2eventservicereference>1:0:1:445D:453:1:C00000:0:0:0:</e2eventservicereference>
			<e2eventservicename>DemoService</e2eventservicename>
			<e2eventprovidername>DemoProvider</e2eventprovidername>
			<e2eventid>45184</e2eventid>
			<e2eventname>Demo Eventname 2</e2eventname>
			<e2eventtitle>Demo Eventname 2</e2eventtitle>
			<e2eventdescription>Event Short description 2</e2eventdescription>
			<e2eventstart>%(start_next).2f</e2eventstart>
			<e2eventduration>1800</e2eventduration>
			<e2eventremaining>1800</e2eventremaining>
			<e2eventcurrenttime>%(now).2f</e2eventcurrenttime>
			<e2eventdescriptionextended>Event description 2</e2eventdescriptionextended>
		</e2event>
	</e2eventlist>
</e2currentserviceinformation>"""
# (recording)
,"""<e2currentserviceinformation>
	<e2service>
		<e2servicereference>N/A</e2servicereference>
		<e2servicename>Some recording</e2servicename>
		<e2providername>N/A</e2providername>
		<e2videowidth>624</e2videowidth>
		<e2videoheight>352</e2videoheight>
		<e2servicevideosize>624x352</e2servicevideosize>
		<e2iswidescreen></e2iswidescreen>
		<e2apid>N/A</e2apid>
		<e2vpid>N/A</e2vpid>
		<e2pcrpid>N/A</e2pcrpid>
		<e2pmtpid>N/A</e2pmtpid>
		<e2txtpid>N/A</e2txtpid>
		<e2tsid>N/A</e2tsid>
		<e2onid>N/A</e2onid>
		<e2sid>N/A</e2sid>
	</e2service>
	<e2eventlist>
		<e2event>
			<e2eventservicereference>N/A</e2eventservicereference>
			<e2eventservicename>Some recording</e2eventservicename>
			<e2eventprovidername>N/A</e2eventprovidername>
			<e2eventid></e2eventid>
			<e2eventname>Some name</e2eventname>
			<e2eventtitle>Some title</e2eventtitle>
			<e2eventdescription>Some description</e2eventdescription>
			<e2eventstart>%(start_now).2f</e2eventstart>
			<e2eventduration>5098</e2eventduration>
			<e2eventremaining>5098</e2eventremaining>
			<e2eventcurrenttime>%(now).2f</e2eventcurrenttime>
			<e2eventdescriptionextended></e2eventdescriptionextended>
		</e2event>
		<e2event>
			<e2eventservicereference>N/A</e2eventservicereference>
			<e2eventservicename>Some recording</e2eventservicename>
			<e2eventprovidername>N/A</e2eventprovidername>
			<e2eventid></e2eventid>
			<e2eventname></e2eventname>
			<e2eventtitle></e2eventtitle>
			<e2eventdescription></e2eventdescription>
			<e2eventstart></e2eventstart>
			<e2eventduration></e2eventduration>
			<e2eventremaining></e2eventremaining>
			<e2eventcurrenttime>%(now).2f</e2eventcurrenttime>
			<e2eventdescriptionextended></e2eventdescriptionextended>
		</e2event>
	</e2eventlist>
</e2currentserviceinformation>""")

SIMPLEXMLRESULT = """<?xml version="1.0" encoding="UTF-8"?>
<e2simplexmlresult>
<e2state>%s</e2state>
<e2statetext>%s</e2statetext>
</e2simplexmlresult>"""

ABOUT = """<?xml version="1.0" encoding="UTF-8"?>
<e2abouts>
	<e2about>
		<e2enigmaversion>2011-01-28-experimental</e2enigmaversion>
		<e2imageversion>Experimental 2010-12-17</e2imageversion>
		<e2webifversion>1.6.6</e2webifversion>
		<e2fpversion>None</e2fpversion>
		<e2model>dm800</e2model>
		<e2lanmac>00:09:34:27:9e:9f</e2lanmac>
		<e2landhcp>True</e2landhcp>
		<e2lanip>192.168.45.26</e2lanip>
		<e2lanmask>255.255.255.0</e2lanmask>
		<e2langw>192.168.45.1</e2langw>
		<e2hddinfo>
			<model>ATA(FUJITSU MHZ2320B)</model>
			<capacity>320.072 GB</capacity>
			<free>91.079 GB</free>
		</e2hddinfo>
		<e2tunerinfo>
			<e2nim>
				<name>Tuner A</name>
				<type> Alps BSBE2 (DVB-S2)</type>
			</e2nim>
		</e2tunerinfo>
		<e2servicename>ProSieben</e2servicename>
		<e2servicenamespace></e2servicenamespace>
		<e2serviceaspect></e2serviceaspect>
		<e2serviceprovider>ProSiebenSat.1</e2serviceprovider>
		<e2videowidth>720</e2videowidth>
		<e2videoheight>576</e2videoheight>
		<e2servicevideosize>720x576</e2servicevideosize>
		<e2apid>512</e2apid>
		<e2vpid>511</e2vpid>
		<e2pcrpid>511</e2pcrpid>
		<e2pmtpid>97</e2pmtpid>
		<e2txtpid>33</e2txtpid>
		<e2tsid>1107</e2tsid>
		<e2onid>1</e2onid>
		<e2sid>17501</e2sid>
	</e2about>
</e2abouts>"""

SERVICES_E2 = """<?xml version="1.0" encoding="UTF-8"?>
<e2servicelist>
	%(services)s
</e2servicelist>"""

SERVICE_E2 = """
	<e2service>
		<e2servicereference>%(sref)s</e2servicereference>
		<e2servicename>%(sname)s</e2servicename>
	</e2service>
"""

EPGSERVICE = """<?xml version="1.0" encoding="UTF-8"?>
<e2eventlist>
%s
</e2eventlist>"""

EVENTTEMPLATE = """<e2event>
		<e2eventid>45183</e2eventid>
		<e2eventstart>%.2f</e2eventstart>
		<e2eventduration>1560</e2eventduration>
		<e2eventcurrenttime>%.2f</e2eventcurrenttime>
		<e2eventtitle>Demo Event</e2eventtitle>
		<e2eventdescription>Event Short description</e2eventdescription>
		<e2eventdescriptionextended>Event description</e2eventdescriptionextended>
		<e2eventservicereference>%s</e2eventservicereference>
		<e2eventservicename>Demo Service</e2eventservicename>
	</e2event>
"""

TIMERLIST_E2 = """<?xml version="1.0" encoding="UTF-8"?>
<e2timerlist>
%s
</e2timerlist>"""

TIMERTEMPLATE_E2 = """<e2timer>
   <e2servicereference>%s</e2servicereference>
   <e2servicename>Demo Service</e2servicename>
   <e2eit>%d</e2eit>
   <e2name>%s</e2name>
   <e2description>%s</e2description>
   <e2descriptionextended></e2descriptionextended>
   <e2disabled>0</e2disabled>
   <e2timebegin>%d</e2timebegin>
   <e2timeend>%d</e2timeend>
   <e2duration>%d</e2duration>
   <e2startprepare>%d</e2startprepare>
   <e2justplay>%d</e2justplay>
   <e2afterevent>%d</e2afterevent>
   <e2logentries></e2logentries>
   <e2filename></e2filename>
   <e2backoff>0</e2backoff>
   <e2nextactivation></e2nextactivation>
   <e2firsttryprepare>True</e2firsttryprepare>
   <e2state>%d</e2state>
   <e2repeated>%d</e2repeated>
   <e2dontsave>0</e2dontsave>
   <e2cancled>False</e2cancled>
   <e2color>000000</e2color>
   <e2toggledisabled>1</e2toggledisabled>
   <e2toggledisabledimg>off</e2toggledisabledimg>
  </e2timer>"""

MOVIELIST_E2 = """<?xml version="1.0" encoding="UTF-8"?>
<e2movielist>
%s
</e2movielist>"""

MOVIETEMPLATE_E2 = """<e2movie>
		<e2servicereference>1:0:0:0:0:0:0:0:0:0:%s</e2servicereference>
		<e2title>%s</e2title>
		<e2description>%s</e2description>
		<e2descriptionextended>%s</e2descriptionextended>
		<e2servicename>%s</e2servicename>
		<e2time>1298106939</e2time>
		<e2length>0:11</e2length>
		<e2tags></e2tags>
		<e2filename>%s</e2filename>
		<e2filesize>7040976</e2filesize>
	</e2movie>"""

POWERSTATE = """<?xml version="1.0" encoding="UTF-8"?>
<e2powerstate>
	<e2instandby>%s</e2instandby>
</e2powerstate>"""

VOLUME = """<?xml version="1.0" encoding="UTF-8"?>
<e2volume>
	<e2result>True</e2result>
	<e2resulttext>%s</e2resulttext>
	<e2current>40</e2current>
	<e2ismuted>%s</e2ismuted>
</e2volume>"""

SIGNAL_E2 = """<?xml version="1.0" encoding="UTF-8"?>
<e2frontendstatus>
	<e2snrdb>
		12.80 dB
	</e2snrdb>
	<e2snr>
		79 %
	</e2snr>
	<e2ber>
		0
	</e2ber>
	<e2acg>
		76 %
	</e2acg>
</e2frontendstatus>"""

REMOTECONTROL = """<?xml version="1.0" encoding="UTF-8"?>
<e2remotecontrol>
	<e2result>%s</e2result>
	<e2resulttext>%s</e2resulttext>
</e2remotecontrol>"""

LOCATIONLIST = """<?xml version="1.0" encoding="UTF-8"?>
<e2locations>
<e2location>/hdd/movie/</e2location>
</e2locations>"""

FILELIST = """<?xml version="1.0" encoding="UTF-8"?>
<e2filelist>
	%s
</e2filelist>"""

FILE = """<e2file>
 <e2servicereference>%s</e2servicereference>
 <e2isdirectory>%s</e2isdirectory>
 <e2root>%s</e2root>
</e2file>"""

GETCURRENT_E1 = (
"""<?xml version="1.0" encoding="UTF-8" ?>
<currentservicedata>
    <service>
        <name></name>
        <reference></reference>
    </service>
    <audio_channels>
    </audio_channels>
    <audio_track>
    </audio_track>
    <video_channels>
    </video_channels>
    <current_event>
        <date></date>
        <time></time>
        <start></start>
        <duration></duration>
        <description></description>
        <details></details>
    </current_event>
    <next_event>
        <date></date>
        <time></time>
        <start></start>
        <duration></duration>
        <description></description>
        <details></details>
    </next_event>
</currentservicedata>""",
"""<?xml version="1.0" encoding="UTF-8" ?>
<currentservicedata>
    <service>
        <name>Some Service</name>
        <reference>:::::DUMMY:::::</reference>
    </service>
    <audio_channels>
		-1
    </audio_channels>
    <audio_track>
		-1
    </audio_track>
    <video_channels>
		-1
    </video_channels>
    <current_event>
        <date>-1</date>
        <time>-1</time>
        <start>%(start_now).2f</start>
        <duration>99</duration>
        <description>Some title</description>
        <details>Some description</details>
    </current_event>
    <next_event>
        <date>-1</date>
        <time>-1</time>
        <start>%(start_next).2f</start>
        <duration>101</duration>
        <description>Some other title</description>
        <details>Some other description</details>
    </next_event>
</currentservicedata>""",
"""<?xml version="1.0" encoding="UTF-8" ?>
<currentservicedata>
    <service>
        <name></name>
        <reference>:::DUMMY RECORDING:::</reference>
    </service>
    <audio_channels>
		-1
    </audio_channels>
    <audio_track>
		-1
    </audio_track>
    <video_channels>
		-1
    </video_channels>
    <current_event>
        <date>-1</date>
        <time>-1</time>
        <start>%(start_now).2f</start>
        <duration>99</duration>
        <description>Some recording</description>
        <details></details>
    </current_event>
    <next_event>
        <date></date>
        <time></time>
        <start></start>
        <duration></duration>
        <description></description>
        <details></details>
    </next_event>
</currentservicedata>""")

BOXSTATUS = """<?xml version="1.0" encoding="UTF-8"?>
<boxstatus><current_time>1298106939</current_time><standby>0</standby><recording>0</recording><mode>0</mode><ip>127.0.0.1</ip></boxstatus>"""

SERVICES_E1 = """<?xml version="1.0" encoding="UTF-8"?>
<bouquets>
 <bouquet><reference>%s</reference><name>%s</name>
  <service><reference>%s</reference><name>%s</name><provider>Demo Provider</provider><orbital_position>192</orbital_position></service>
 </bouquet>
</bouquets>"""

SERVICES_E1_OLD = """<?xml version="1.0" encoding="ISO-8859-1"?>
<bouquet>
 <service reference="1:0:1:6dca:44d:1:c00000:0:0:0:" orbitalposition="192">Demo Service</service>
</bouquet>"""

EPGSERVICE_E1 = """<?xml version="1.0" encoding="UTF-8"?>
 <?xml-stylesheet type="text/xsl" href="/xml/serviceepg.xsl"?>
 <service_epg>
 <service>
 <reference>1:0:1:6dca:44d:1:c00000:0:0:0:</reference>
 <name>Demo Service</name>
 </service>
 <event id="0">
 <date>18.09.2008</date>
 <time>16:02</time>
 <duration>3385</duration>
 <description>Demo Event</description>
 <genre>n/a</genre>
 <genrecategory>00</genrecategory>
 <start>1221746555</start>
 <details>Event Details</details>
 </event>
 </service_epg>"""

TIMERLIST_E1 = """<?xml version="1.0" encoding="UTF-8"?>
 <timers>
%s
 </timers>"""

TIMERTEMPLATE_E1 = """<timer>
   <type>%s</type>
   <days>%s</days>
   <action>%s</action>
   <postaction>%s</postaction>
   <status>%s</status>
   <typedata>%d</typedata>
   <service>
    <reference>%s</reference>
    <name>Demo Service</name>
   </service>
   <event>
    <date>%s</date>
    <time>%s</time>
    <start>%d</start>
    <duration>%d</duration>
    <description>%s</description>
   </event>
  </timer>"""

QUERYDELETETIMER_E1 = """<html>
    <head>
        <title>Question</title>
        <link rel="stylesheet" type="text/css" href="webif.css">
        <script>
            function yes()
            {
                document.location = "%s";
            }
            function no()
            {
                document.close();
            }
        </script>
    </head>
    <body>
        <b>ATTENTION</b>: This timer event is currently active.
        <br>
        Do you really want to delete this timer event?
        <br><br>
        <input name="yes" type="button" style="width: 100px; height: 22px; background-color: #1FCB12" value="YES" onClick=javascript:yes()>
        <input name="no" type="button" style="width: 100px; height: 22px; background-color: #CB0303" value="NO" onClick=javascript:no()>
    </body>
</html>"""

CLOSEWINDOW_E1 = """<html>
    <head>
        <title>Complete</title>
        <link rel="stylesheet" type="text/css" href="webif.css">
        <script>
            function init()
            {
                setTimeout("window.close()", 5000);
            }
        </script>
    </head>
    <body onLoad="init()" onUnload="parent.window.opener.location.reload(true)">
        %s
    </body>
</html>"""

MOVIELIST_E1 = """<?xml version="1.0" encoding="UTF-8"?>
<movies>
   %s
</movies>"""

MOVIETEMPLATE_E1 = """<service><reference>1:0:1:6dcf:44d:1:c00000:93d2d1:0:0:%s</reference><name>%s</name><orbital_position>192</orbital_position></service>"""

SIGNAL_E1 = """<?xml version="1.0" encoding="UTF-8" ?>
 <?xml-stylesheet type="text/xsl" href="/xml/streaminfo.xsl"?>
 <streaminfo>
 <frontend>#FRONTEND#</frontend>
 <service>
 <name>n/a</name>
 <reference></reference>
 </service>
 <provider>n/a</provider>
 <vpid>ffffffffh (-1d)</vpid>
 <apid>ffffffffh (-1d)</apid>

 <pcrpid>ffffffffh (-1d)</pcrpid>
 <tpid>ffffffffh (-1d)</tpid>
 <tsid>0000h</tsid>
 <onid>0000h</onid>
 <sid>0000h</sid>
 <pmt>ffffffffh</pmt>
 <video_format>n/a</video_format>
 <namespace>0000h</namespace>
 <supported_crypt_systems>4a70h Dream Multimedia TV (DreamCrypt)</supported_crypt_systems>

 <used_crypt_systems>None</used_crypt_systems>
 <satellite>n/a</satellite>
 <frequency>n/a</frequency>
 <symbol_rate>n/a</symbol_rate>
 <polarisation>n/a</polarisation>
 <inversion>n/a</inversion>
 <fec>n/a</fec>
 <snr>79%</snr>
 <agc>76%</agc>

 <ber>0</ber>
 <lock>n/a</lock>
 <sync>n/a</sync>
 <modulation>#MODULATION#</modulation>
 <bandwidth>#BANDWIDTH#</bandwidth>
 <constellation>#CONSTELLATION#</constellation>
 <guardinterval>#GUARDINTERVAL#</guardinterval>
 <transmission>#TRANSMISSION#</transmission>
 <coderatelp>#CODERATELP#</coderatelp>

 <coderatehp>#CODERATEHP#</coderatehp>
 <hierarchyinfo>#HIERARCHYINFO#</hierarchyinfo>
 </streaminfo>"""

SERVICES_NEUTRINO = """<?xml version="1.0" encoding="UTF-8"?>
<zapit>
 <Bouquet type="0" bouquet_id="0000" name="Demo Bouquet" hidden="0" locked="0">
  <channel serviceID="d175" name="Demo Service" tsid="2718" onid="f001"/>
 </Bouquet>
</zapit>"""

SERVICES_NEUTRINOHD = """<?xml version="1.0" encoding="UTF-8"?>
<zapit>
 <Bouquet name="[E019.2] Demo Provider" hidden="0" locked="0">
  <S i="d175" n="Demo Service" t="2718" on="f001" s="192" frq="12188"/>
 </Bouquet>
</zapit>"""

BOUQUETS_NEUTRINO = """1 Demo Bouquet"""

# (short_)id was guessed
SERVICES_BOUQUET_NEUTRINO = """<?xml version="1.0" encoding="UTF-8"?>
<channellist>
<channel>
<number>1</number>
<bouquet>1</bouquet>
<id>1922718f001d175</id>
<short_id>2718f001d175</short_id>
<name>Demo Service</name>
<logo>/share/tuxbox/neutrino/icons/logo/2718f001d175.jpg</logo>
</channel>
</channellist>"""

EPGSERVICE_NEUTRINO = """<?xml version="1.0" encoding="UTF-8"?>
 <epglist>
 <channel_id>%s</channel_id>
 <channel_name><![CDATA[Demo Service]]></channel_name>%s
 </epglist>"""

EPGSERVICE_NEUTRINO_ENTRY = """
 <prog>
 <eventid>309903955495411052</eventid>
 <eventid_hex>44d00016dcadd6c</eventid_hex>
 <start_sec>1148314800</start_sec>
 <start_t>18:20</start_t>
 <date>02.10.2006</date>
 <stop_sec>1148316600</stop_sec>
 <stop_t>18:50</stop_t>
 <duration_min>30</duration_min>
 <description><![CDATA[Demo Event]]></description>%s
 </prog>
 </epglist>"""

EPGSERVICE_NEUTRINO_DETAILS = """
 <info1><![CDATA[Event short description]]></info1>
 <info2><![CDATA[Event description.]]></info2>"""
### /DOCUMENTS

TYPE_E2 = 0
TYPE_E1 = 1
TYPE_NEUTRINO = 2

RADIO_E2 = '1:7:2:0:0:0:0:0:0:0:(type == 2)FROM BOUQUET "bouquets.radio" ORDER BY bouquet'
FAVOURITES_E2 = '1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.favourites.tv" ORDER BY bouquet'
FAVOURITES_RADIO_E2 = '1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.favourites.radio" ORDER BY bouquet'
PROVIDERS_E2 = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) FROM PROVIDERS ORDER BY name'
PROVIDERS_RADIO_E2 = '1:7:2:0:0:0:0:0:0:0:(type == 2) FROM PROVIDERS ORDER BY name'
ALLSERVICES_E2 = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) ORDER BY name'
ALLSERVICES_RADIO_E2 = '1:7:2:0:0:0:0:0:0:0:(type == 2) ORDER BY name'

PlaylistEntry=1
SwitchTimerEntry=2
RecTimerEntry=4
recDVR=8
recVCR=16
recNgrab=131072
stateWaiting=32
stateRunning=64
statePaused=128
stateFinished=256
stateError=512
errorNoSpaceLeft=1024
errorUserAborted=2048
errorZapFailed=4096
errorOutdated=8192
boundFile=16384
isSmartTimer=32768
isRepeating=262144
doFinishOnly=65536
doShutdown=67108864
doGoSleep=134217728
Su=524288
Mo=1048576
Tue=2097152
Wed=4194304
Thu=8388608
Fr=16777216
Sa=33554432

SHUTDOWN = 1
NEXTPROGRAM = 2
ZAPTO = 3
STANDBY = 4
RECORD = 5
REMIND = 6
SLEEPTIMER = 7
EXEC_PLUGIN = 8
class Timer:
	weekdayMon = 1 << 0
	weekdayTue = 1 << 1
	weekdayWed = 1 << 2
	weekdayThu = 1 << 3
	weekdayFri = 1 << 4
	weekdaySat = 1 << 5
	weekdaySun = 1 << 6

	afterEventNothing = 0
	afterEventStandby = 1
	afterEventDeepstandby = 2
	afterEventAuto = 3

	def __init__(self, sRef, begin, end, name, description, eit, disabled, justplay, afterevent, repeated):
		self.sRef = sRef
		self.begin = begin
		self.end = end
		self.name = name
		self.description = description
		self.eit = eit
		self.disabled = disabled
		self.justplay = justplay
		self.afterevent = afterevent
		self.repeated = repeated

	def setTypedata(self, action, afterevent, repeating, mo, tu, we, th, fr, sa, su):
		if (afterevent & doGoSleep) > 0: self.afterevent = self.afterEventStandby
		elif (afterevent & doShutdown) > 0: self.afterevent = self.afterEventDeepstandby
		else: self.afterevent = self.afterEventNothing

		self.justplay = action == "zap"

		if repeating:
			if mo: self.repeated |= self.weekdayMon
			if tu: self.repeated |= self.weekdayTue
			if we: self.repeated |= self.weekdayWed
			if th: self.repeated |= self.weekdayThu
			if fr: self.repeated |= self.weekdayFri
			if sa: self.repeated |= self.weekdaySat
			if su: self.repeated |= self.weekdaySun

	def getType(self):
		now = time.time()
		if self.end < now: typedata = stateFinished
		elif self.begin < now: typedata = stateRunning
		else: typedata = stateWaiting

		if self.afterevent == self.afterEventStandby: typedata |= doGoSleep
		elif self.afterevent == self.afterEventDeepstandby: typedata |= doShutdown
		else:
			pass # TODO: ???

		# TODO: disabled == statePaused ?
		if self.justplay: typedata |= SwitchTimerEntry
		else:
			typedata |= RecTimerEntry
			typedata |= recDVR # TODO: add ngrab?

		if self.repeated:
			typedata |= isRepeating
			if self.repeated & self.weekdaySun: typedata |= Su
			if self.repeated & self.weekdayMon: typedata |= Mo
			if self.repeated & self.weekdayTue: typedata |= Tue
			if self.repeated & self.weekdayWed: typedata |= Wed
			if self.repeated & self.weekdayThu: typedata |= Thu
			if self.repeated & self.weekdayFri: typedata |= Fr
			if self.repeated & self.weekdaySat: typedata |= Sa

		return typedata

	type = property(getType)

	def getRepresentation(self, type, useId=False):
		now = time.time()
		if type == TYPE_E2:
			timerstate = 0
			if self.end < now: timerstate = 3
			elif self.begin < now: timerstate = 2
			return TIMERTEMPLATE_E2 % (self.sRef, self.eit, self.name, self.description, self.begin, self.end, self.end-self.begin, self.begin-10, self.justplay, self.afterevent, timerstate, self.repeated)
		elif type == TYPE_E1:
			if self.end < now:
				typedata = stateFinished
				status = "FINISHED"
			elif self.begin < now:
				typedata = stateRunning
				status = "ACTIVE"
			else:
				typedata = stateWaiting
				status = "ACTIVE" # ???

			if self.afterevent == self.afterEventStandby:
				typedata |= doGoSleep
				postaction = "Standby"
			elif self.afterevent == self.afterEventDeepstandby:
				typedata |= doShutdown
				postaction = "Shutdown"
			else:
				# TODO: all ???
				postaction = "None"

			# TODO: disabled == statePaused ?
			if self.justplay:
				typedata |= SwitchTimerEntry
				action = "ZAP"
			else:
				typedata |= RecTimerEntry
				# TODO: add ngrab o0
				action = "DVR"
				typedata |= recDVR

			if self.repeated:
				typeString = "REPEATING"
				days = ""
				typedata |= isRepeating
				if self.repeated & self.weekdaySun:
					typedata |= Su
					days += "Su "
				if self.repeated & self.weekdayMon:
					typedata |= Mo
					days += " Mo"
				if self.repeated & self.weekdayTue:
					typedata |= Tue
					days += "Tue "
				if self.repeated & self.weekdayWed:
					typedata |= Wed
					days += "Wed "
				if self.repeated & self.weekdayThu:
					typedata |= Thu
					days += "Thu "
				if self.repeated & self.weekdayFri:
					typedata |= Fr
					days += "Fr "
				if self.repeated & self.weekdaySat:
					typedata |= Sa
					days += "Sa "
			else:
				typeString = "SINGLE"
				days = ""

			dateString = time.strftime('%d.%m.%Y', time.localtime(self.begin))
			timeString = time.strftime('%H:%M', time.localtime(self.begin))
			return TIMERTEMPLATE_E1 % (typeString, days, action, postaction, status, typedata, self.sRef, dateString, timeString, self.begin, self.end-self.begin, self.name)
		elif type == TYPE_NEUTRINO:
			# XXX: demo only knows one service anyway
			if useId:
				if EMULATE_NEUTRINOHD:
					data = "1922718f001d175"
				else:
					data = "2718f001d175"
			else:
				data = "Demo Service"
			type = ZAPTO if self.justplay else RECORD
			repeat = self.repeated << 8 # XXX: only support weekdays for now
			repcount = 0
			announceTime = self.begin - 10
			return "%d %d %d %d %d %d %d %s\n" % (self.eit, type, repeat, repcount, announceTime, self.begin, self.end, data)

class Service:
	def __init__(self, sref, sname):
		self.sname = sname
		self.sref = sref

class State:
	CURRENT_TYPE_STANDBY, CURRENT_TYPE_LIVE, CURRENT_TYPE_RECORDING, CURRENT_TYPE_MAX = xrange(4)
	def __init__(self):
		self.movies = []
		self.timers = []
		self.is_muted = False
		self.currentType = self.CURRENT_TYPE_STANDBY
		self.reset()

	def getBouquetsForType(self, type="tv"):
		if type == "radio":
			return self.bouquets_r
		elif type == "providers_radio":
			return self.providers_r
		elif type == "providers":
			return self.providers_t
		return self.bouquets_t

	def getServicesForBouquet(self, bRef):
		return self.services.setdefault(bRef, [])

	def reset(self):
		self.setupMovies()
		self.setupTimers()
		self.setupServices()

	def setupServices(self):
		self.bouquets_r = [Service(FAVOURITES_RADIO_E2, "Demo Radio Bouquet")]
		self.bouquets_t = [Service(FAVOURITES_E2, "Demo Bouquet")]
		self.providers_r = [Service(PROVIDERS_RADIO_E2, "Sole Radio Provider")]
		self.providers_t = [Service(PROVIDERS_E2, "Sole Provider")]
		self.services = {
				FAVOURITES_RADIO_E2: [Service(':::::::::::DUNNO:::::::::::', 'Demo Radio Service')],
				PROVIDERS_RADIO_E2: [Service(':::::::::::DUNNO:::::::::::', 'Demo Radio Service')],
				ALLSERVICES_RADIO_E2: [Service(':::::::::::DUNNO:::::::::::', 'Demo Radio Service'), Service("-99", "Some Radio Service without Provider")],
				FAVOURITES_E2: [Service('1:0:1:445D:453:1:C00000:0:0:0:', 'Demo Service')],
				PROVIDERS_E2: [Service('1:0:1:445D:453:1:C00000:0:0:0:', 'Demo Service'), Service("-1", "Some Service"), Service("-2", "Some other Service")],
				ALLSERVICES_E2: [Service('1:0:1:445D:453:1:C00000:0:0:0:', 'Demo Service'), Service("-1", "Some Service"), Service("-2", "Some other Service"), Service("-3", "Some Service without Provider")],
		}

	def setupMovies(self):
		del self.movies[:]
		self.movies.append(('/hdd/movie/Demofilename.ts', 'Recording title', 'Recording short description', 'Recording description', 'Demo Service'))

	def getMovies(self, type):
		moviestrings = ''
		for movie in self.movies:
			fname, title, desc, edesc, sname = movie
			if type == TYPE_E2:
				moviestrings += MOVIETEMPLATE_E2 % (fname, title, desc, edesc, sname, fname)
			elif type == TYPE_E1:
				moviestrings += MOVIETEMPLATE_E1 % (fname, title)
		return moviestrings

	def deleteMovie(self, sRef, type):
		if type == TYPE_E2:
			if sRef == '1:0:0:0:0:0:0:0:0:0:/hdd/movie/Demofilename.ts' and len(self.movies):
				movies.pop()
				return True
		elif type == TYPE_E1:
			if sRef == '1:0:1:6dcf:44d:1:c00000:93d2d1:0:0:/hdd/movie/Demofilename.ts' and len(self.movies):
				movies.pop()
				return True
		return False

	def addTimer(self, sRef, begin, end, name, description, eit, disabled, justplay, afterevent, repeated):
		timer = Timer(sRef, begin, end, name, description, eit, disabled, justplay, afterevent, repeated)
		self.timers.append(timer)
		return timer

	def getTimers(self, type, useId=False):
		timerstrings = ''
		for timer in self.timers:
			timerstrings += timer.getRepresentation(type, useId=useId)
		return timerstrings

	def deleteTimer(self, sRef, begin, end):
		idx = 0
		for timer in self.timers:
			if timer.sRef == sRef and timer.begin == begin and timer.end == end:
				del self.timers[idx]
				return True
			idx += 1
		return False

	def findTimer(self, findSref, findBegin):
		for timer in self.timers:
			if timer.sRef == findSref and timer.begin == findBegin: return timer
		return None

	def findTimerOverlap(self, findSref, findBegin, findEnd):
		for timer in self.timers:
			# XXX: we don't support "same transponder" policy... but then again, there is only one demo service :-)
			# NOTE: different service and begin/end in our timespan or begins before us and ends after us
			if timer.sRef != findSref and ((timer.begin > findBegin and timer.begin < findEnd) or (timer.end > findBegin and timer.end < findEnd) or (timer.begin < findBegin and timer.end > findEnd)):
				return True
		return False

	def setupTimers(self):
		del self.timers[:]
		self.addTimer('1:0:1:445D:453:1:C00000:0:0:0:', 1205093400, 1205097600, "Demo Timer", "Timer description", 1, 0, 0, 0, 0)

	def toggleMuted(self):
		self.is_muted = not self.is_muted

	def setMuted(self, mute):
		self.is_muted = mute

	def isMuted(self):
		return self.is_muted

	def getCurrentType(self):
		self.currentType = (self.currentType + 1) % self.CURRENT_TYPE_MAX
		return self.currentType

state = State()

# returns sample documents, stupid demo contents :-)
class Simple(resource.Resource):
	isLeaf = True
	def render_GET(self, req):
		def get(name, default=None):
			ret = req.args.get(name)
			return ret[0] if ret else default
		returndoc = ''
		lastComp = req.postpath[-1]
# ENIGMA2
		if lastComp == "getcurrent":
			curtype = state.getCurrentType()
			now = time.time()
			returndoc = GETCURRENT[curtype] % {'start_now':now-179, 'now':now, 'start_next':now+1381}
		elif lastComp == "recordnow":
			returndoc = SIMPLEXMLRESULT % ('True', 'instant record started')
		elif lastComp == "about":
			returndoc = ABOUT
		elif lastComp == "zap":
			sRef = req.args.get('sRef')
			sRef = sRef and sRef[0]
			returndoc = SIMPLEXMLRESULT % ('True', 'Active service switched to '+sRef)
		elif req.path == "/web/getservices":
			sRef = get('sRef')
			if sRef == RADIO_E2:
				services = state.getBouquetsForType("radio")
			elif sRef == PROVIDERS_E2:
				services = state.getBouquetsForType("providers")
			elif sRef == PROVIDERS_RADIO_E2:
				services = state.getBouquetsForType("providers_radio")
			elif not sRef: # XXX: what is real tv bouquets sref?
				services = state.getBouquetsForType("tv")
			# TODO: implement provider and "all services"
			else:
				services = state.getServicesForBouquet(sRef)
			returndoc = SERVICES_E2 % {"services": ''.join([SERVICE_E2 % {"sref": x.sref, "sname": x.sname} for x in services])}
		elif lastComp == "epgnow" or lastComp == "epgnext":
			sRef = req.args.get('bRef')
			sRef = sRef and sRef[0]
			FAVOURITES = '1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.favourites.tv" ORDER BY bouquet'
			FAVOURITES_RADIO = '1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.favourites.radio" ORDER BY bouquet'
			if sRef and sRef in (FAVOURITES, FAVOURITES_RADIO):
				now = time.time()
				if lastComp == "epgnext": now += 1560
				event = EVENTTEMPLATE % (now, now, sRef)
				returndoc = EPGSERVICE % (event,)
			else:
				returndoc = "UNHANDLED REQUEST"
		elif lastComp == "epgservice":
			sRef = req.args.get('sRef')
			sRef = sRef and sRef[0]
			if sRef:
				now = time.time()
				event = EVENTTEMPLATE % (now, now, sRef)
				returndoc = EPGSERVICE % (event,)
			else:
				returndoc = EPGSERVICE % ('',)
		elif lastComp == "powerstate":
			returndoc = POWERSTATE % ('false',)
		elif lastComp == "vol":
			set = req.args.get('set')
			set = set and set[0]
			if set:
				if len(set) > 3 and set[:3] == 'set':
					vol = int(set[3:])
					message = "Volume set to %d" % (vol,)
				elif set == 'mute':
					state.toggleMuted()
					message = "Mute toggled"
				else:
					message = "OMFG SOMETHING WENT WRONG"
			else:
				message = "State"
			returndoc = VOLUME % (message, 'True' if state.isMuted() else 'False')
		elif lastComp == "signal":
			returndoc = SIGNAL_E2 # TODO: add jitter?
		elif lastComp == "remotecontrol":
			command = int(req.args.get('command')[0])
			if command > 0:
				returndoc = REMOTECONTROL % ('True', "RC command '"+str(command)+"' has been issued")
			else:
				returndoc = REMOTECONTROL % ('False', 'the command was not &gt; 0')
		elif req.path == "/web/message":
			text = req.args.get('text')
			ttype = req.args.get('type')
			if not text or not text[0]:
				returndoc = SIMPLEXMLRESULT % ('False', 'No Messagetext given')
			else:
				try: ttype = int(ttype[0])
				except: returndoc = SIMPLEXMLRESULT % ('False', 'Type %s is not a number' % (ttype[0],))
				else: returndoc = SIMPLEXMLRESULT % ('True', 'Message sent successfully!')
		elif lastComp == "grab":
			returndoc = "Grab is not installed at /usr/bin/grab. Please install package aio-grab." # TODO: add sample pictures?
		elif lastComp == "epgsearch":
			search = req.args.get('search')
			event = ''
			if search and search[0] in "Demo Event":
				now = time.time()
				event = EVENTTEMPLATE % (now, now, '1:0:1:445D:453:1:C00000:0:0:0:')
			returndoc = EPGSERVICE % (event,)
		elif lastComp == "epgsimilar":
			# e2 webif i used for testing crashes on not given / wrong eit, copy this behavior :-D
			eit = int(req.args.get('eventid')[0])

			returndoc = EPGSERVICE % ('',)
### TIMERS
		elif lastComp == "timerlist":
			timerstrings = state.getTimers(TYPE_E2)
			returndoc = TIMERLIST_E2 % (timerstrings,)
		elif lastComp in ("timeradd", "timerchange", "timeraddbyeventid"):
			returndoc = ''
			if lastComp == "timerchange":
				delete = int(get('deleteOldOnSave', 0))
				sRef = get('channelOld')
				begin = int(get('beginOld'))
				end = int(get('endOld'))
				if delete: state.deleteTimer(sRef, begin, end)
			sRef = get('sRef')
			eventid = int(get('eventid', 0))
			if lastComp == "timeraddbyeventid":
				# XXX: our events are dynamic and use time() as begin, so just copy that here
				now = time.time()
				if sRef == '':
					returndoc = SIMPLEXMLRESULT % ('False', 'Missing Parameter: sRef')
				elif eventid == 0:
					returndoc = SIMPLEXMLRESULT % ('False', 'Missing Parameter: eventid')
				elif sRef != '1:0:1:445D:453:1:C00000:0:0:0:' or eventid != 45183:
					returndoc = SIMPLEXMLRESULT % ('False', 'EventId not found')
				else:
					begin = now
					end = now + 1560
					name = "Demo Event"
					desc = "Event Short description"
					afterevent = 3
					repeated = 0
					disabled = 0
			else:
				begin = int(get('begin'))
				end = int(get('end'))
				name = get('name')
				desc = get('description')
				afterevent = int(get('afterevent'))
				repeated = int(get('repeated'))
				disabled = int(get('disabled'))
			justplay = int(get('justplay'))
			dirname = get('dirname')
			tags = get('tags')
			state.addTimer(sRef, begin, end, name, desc, eventid, disabled, justplay, afterevent, repeated)
			if lastComp == "timerchange":
				returndoc = SIMPLEXMLRESULT % ('True', 'Timer changed successfully')
			elif lastComp == "timeraddbyeventid":
				if returndoc == '':
					returndoc = SIMPLEXMLRESULT % ('True', "Timer '%s' added" % (name,))
			else:
				returndoc = SIMPLEXMLRESULT % ('True', 'Timer added successfully')
		elif lastComp == "timerdelete":
			sRef = req.args.get('sRef')[0]
			begin = int(req.args.get('begin')[0])
			end = int(req.args.get('end')[0])
			if state.deleteTimer(sRef, begin, end): returndoc = SIMPLEXMLRESULT % ('True', 'SOME TEXT')
			else: returndoc = SIMPLEXMLRESULT % ('False', 'No matching Timer found')
### /TIMERS
### MOVIES
		elif lastComp == "getlocations":
			returndoc = LOCATIONLIST
		elif lastComp == "movielist":
			returndoc = MOVIELIST_E2 % (state.getMovies(TYPE_E2),)
		elif lastComp == "moviedelete":
			sRef = req.args.get('sRef')
			sRef = sRef and sRef[0]
			if state.deleteMovie(sRef, TYPE_E2):
				returndoc = SIMPLEXMLRESULT % ('True', "SOME TEXT'")
			else:
				returndoc = SIMPLEXMLRESULT % ('False', "Could not delete Movie 'this recording'")
### /MOVIES
### MEDIAPLAYER
		elif lastComp == "mediaplayerlist":
			path = req.args.get('path')
			path = path and path[0]
			if path == "playlist":
				files = FILE % ("empty", "True", "playlist")
			else:
				files = ''
			returndoc = FILELIST % (files,)
### /MEDIAPLAYER
### SERVICE EDITOR
		elif req.path.startswith("/bouqueteditor"):
			MODE_TV = 0
			MODE_RADIO = 1
			if lastComp == "addbouquet":
				name = get("name")
				if name:
					mode = int(get("mode", 0))
					if mode == MODE_RADIO:
						bouquets = state.bouquets_r
					else:
						bouquets = state.bouquets_t
					bouquets.append(Service(name, name))
				else:
					returndoc = SIMPLEXMLRESULT % ('False', "Bla, bla, bla - something wrong, not the real error message - bla, bla...")
			elif lastComp == "removebouquet":
				bRef = get("sBouquetRef")
				mode = int(get("mode", 0))
				if mode == MODE_RADIO:
					bouquets = state.bouquets_r
				else:
					bouquets = state.bouquets_t
				for bouquet in bouquets[:]:
					if bouquet.sref == bRef:
						bouquets.remove(bouquet)
						break
			elif lastComp == "movebouquet":
				bRef = get("sBouquetRef")
				mode = int(get("mode", 0))
				position = int(get("position"))
				if mode == MODE_RADIO:
					bouquets = state.bouquets_r
				else:
					bouquets = state.bouquets_t
				idx = 0
				for bouquet in bouquets[:]:
					if bouquet.sref == bRef:
						break
					idx += 1
				bouquets.insert(position, bouquets.pop(idx))
			elif lastComp == "moveservice":
				bRef = get("sBouquetRef")
				sRef = get("sRef")
				mode = int(get("mode", 0))
				position = int(get("position"))
				services = state.getServicesForBouquet(bRef)
				idx = 0
				for service in services[:]:
					if service.sref == sRef:
						break
					idx += 1
				services.insert(position, services.pop(idx))
			elif lastComp == "renameservice":
				bRef = get("sBouquetRef")
				sRef = get("sRef")
				newName = get("newName")
				mode = int(get("mode", 0))
				sRefBefore = get("sRefBefore")
				if bRef is not None:
					# assume moving services
					# XXX: we assume sRefBefore always is the next service or in other words that we won't change our position
					services = state.getServicesForBouquet(bRef)
					for service in services:
						if service.sref == sRef:
							service.sname = newName
							break
				else:
					# assume moving bouquets
					if mode == MODE_RADIO:
						bouquets = state.bouquets_r
					else:
						bouquets = state.bouquets_t
					for bouquet in bouquets:
						if bouquet.sref == sRef:
							bouquet.sname = newName
							break
			elif lastComp == "addservicetoalternative":
				# TODO: implement
				returndoc = "UNHANDLED METHOD"
			elif lastComp == "addservicetobouquet":
				bRef = get("sBouquetRef")
				sRef = get("sRef")
				name = get("Name")
				if sBouquetRed and sRef and Name:
					services = state.getServicesForBouquet(bRef)
					services.append(Service(sRef, name))
				else:
					returndoc = SIMPLEXMLRESULT % ('False', "Bla, bla, bla - something wrong, not the real error message - bla, bla...")
			elif lastComp == "removeservice":
				bRef = get("sBouquetRef")
				sRef = get("sRef")
				services = state.getServicesForBouquet(bRef)
				for service in services[:]:
					if service.sref == sRef:
						services.remove(service)
			elif lastComp == "removealternativeservices":
				# TODO: implement
				returndoc = "UNHANDLED METHOD"
			elif lastComp == "addmarkertobouquet":
				bRef = get("sBouquetRef")
				name = get("Name")
				sRefBefore = get("sRefBefore")
				idx = 0
				services = state.getServicesForBouquet(bRef)
				marker = Service("1:64:1:0:0:0:0:0:0:0::"+name, name)
				if sRefBefore:
					for service in services[:]:
						if service.sref == sRefBefore:
							services.insert(idx, marker)
							break
						idx += 1
				else:
					services.append(marker)
			if not returndoc:
				returndoc = SIMPLEXMLRESULT % ('True', "SOME TEXT - and not really sure if everything worked :D'")
### /SERVICE EDITOR
### AUTOTIMER
		elif req.path.startswith("/autotimer"):
			if lastComp == "get":
				pass
			elif lastComp == "set":
				pass
			elif lastComp == "parse":
				pass
			elif lastComp == "remove":
				pass
			elif lastComp == "edit":
				pass
			elif req.path == "/autotimer":
				pass
			returndoc = "UNHANDLED DOCUMENT" # dummy so we won't send a 404
### /AUTOTIMER
### EPGREFRESH
		elif req.path.startswith("/epgrefresh"):
			if lastComp == "refresh":
				pass
			elif lastComp == "add":
				pass
			elif lastComp == "del":
				pass
			elif lastComp == "set":
				pass
			elif lastComp == "get":
				pass
			elif req.path == "/epgrefresh":
				pass
			returndoc = "UNHANDLED DOCUMENT" # dummy so we won't send a 404
### /EPGREFRESH
# ENIGMA
		elif lastComp == "boxstatus":
			returndoc = BOXSTATUS
		elif lastComp == "currentservicedata":
			curtype = state.getCurrentType()
			now = time.time()
			returndoc = GETCURRENT_E1[curtype] % {'start_now':now-179, 'now':now, 'start_next':now+1381}
		elif lastComp == "zapTo":
			returndoc = "IMO RETURN OF E1 SUCKS"
		elif req.path == "/xml/getServices":
			if EMULATE_OLD_E1 != 3:
				req.setResponseCode(404)
				returndoc = "emulating younger enigma 1"
			# OLD DOCUMENT
			else:
				returndoc = SERVICES_E1_OLD
		elif req.path == "/xml/getservices":
			# OLD API, NEW DOCUMENT
			if EMULATE_OLD_E1 == 1:
				returndoc = SERVICES_E1 % ("4097:7:0:33fc5:0:0:0:0:0:0:/var/tuxbox/config/enigma/userbouquet.33fc5.tv", "Demo Bouquet", "1:0:1:6dca:44d:1:c00000:0:0:0:", "Demo Service")
			# OLD API, OLD DOCUMENT
			elif EMULATE_OLD_E1 == 2:
				returndoc = SERVICES_E1_OLD
			else:
				req.setResponseCode(404)
				if EMULATE_OLD_E1 == 3:
					returndoc = "emulating older enigma 1"
				else:
					returndoc = "emulating younger enigma 1"
		elif lastComp == "services":
			if EMULATE_OLD_E1:
				req.setResponseCode(404)
				returndoc = "emulating old enigma 1"
			else:
				mode = int(get('mode', 0))
				submode = int(get('submode', 2))
				if mode == 3 and submode == 4:
					returndoc = MOVIELIST_E1 % (state.getMovies(TYPE_E1),)
				elif mode == 1 and submode == 4:
					# TODO: find better sample values
					returndoc = SERVICES_E1 % ("4097:7:0:33fc5:0:0:0:0:0:0:/var/tuxbox/config/enigma/userbouquet.33fc5.radio", "Demo Bouquet", ":::::::::::DUNNO:::::::::::", "Demo Radio Service")
				elif mode == 0 and submode == 4:
					returndoc = SERVICES_E1 % ("4097:7:0:33fc5:0:0:0:0:0:0:/var/tuxbox/config/enigma/userbouquet.33fc5.tv", "Demo Bouquet", "1:0:1:6dca:44d:1:c00000:0:0:0:", "Demo Service")
				else:
					returndoc = "UNHANDLED METHOD"
		elif lastComp == "serviceepg":
			sRef = req.args.get('ref')
			sRef = sRef and sRef[0]
			returndoc = EPGSERVICE_E1
### TIMERS
		elif lastComp == "timers":
			timerstrings = state.getTimers(TYPE_E1)
			returndoc = TIMERLIST_E1 % (timerstrings,)
		elif lastComp == "addTimerEvent":
			sRef = get('ref')
			# TODO: support string time, not just unix timestamps
			start = int(get('start', -1))
			duration = int(get('duration', 0))
			descr = get('descr', '')
			after_event = int(get('after_event', 0))
			action = get('action')
			repeating = True if get('timer', '') == "repeating" else False
			mo = get('mo', '') == 'on'
			tu = get('tu', '') == 'on'
			we = get('we', '') == 'on'
			th = get('th', '') == 'on'
			fr = get('fr', '') == 'on'
			sa = get('so', '') == 'on'
			su = get('su', '') == 'on'
			# TODO: are there additional parameters I left out b/c dreamote does not use them?
			if state.findTimerOverlap(sRef, start, start+duration):
				returndoc = "Timer event could not be added because time of the event overlaps with an already existing event."
			else:
				timer = state.addTimer(sRef, start, start+duration, descr, '', -1, 0, 0, 0, 0)
				timer.setTypedata(action, after_event, repeating, mo, tu, we, th, fr, sa, su)
				returndoc = "Timer event was created successfully."
		elif lastComp == "deleteTimerEvent":
			sRef = get('ref')
			start = int(get('start', -1))
			type = int(get('type', -1))
			force = True if get('force', 'no') == "yes" else False
			timer = state.findTimer(sRef, start)
			now = time.time()
			if timer and timer.type == type and timer.begin < now and not timer.end < now and not force:
				newUri = req.uri.replace('force=no', 'force=yes')
				if not 'force=yes' in newUri and '?' in newUri:
					newUri += '&force=yes'
				returndoc = QUERYDELETETIMER_E1 % (newUri,)
			else:
				if timer: state.deleteTimer(timer.sRef, timer.begin, timer.end)
				returndoc = CLOSEWINDOW_E1 % ("Timer event deleted successfully.",)
### /TIMERS
		elif lastComp == "deleteMovie":
			sRef = req.args.get('ref')
			sRef = sRef and sRef[0]
			state.deleteMovie(sRef, TYPE_E1)
			returndoc = "IMO RETURN OF E1 SUCKS"
		elif lastComp == "videocontrol":
			returndoc = "UNHANDLED METHOD"
		elif lastComp == "currentservicedata":
			returndoc = "UNHANDLED METHOD"
		elif lastComp == "admin":
			command = req.args.get('command')
			command = command and command[0]
			returndoc = "UNHANDLED METHOD"
		elif lastComp == "audio":
			toggleMute = 'mute' in req.args
			if toggleMute:
				state.toggleMuted()
				returndoc = """mute set
volume: 0
mute: %d""" % (1 if state.isMuted() else 0,)
			else:
				returndoc = """Volume set.
volume: 0
mute: %d""" % (1 if state.isMuted() else 0,)
			returndoc = "UNHANDLED METHOD"
		elif lastComp == "rc":
			returndoc = "UNHANDLED METHOD"
		elif lastComp == "streaminfo":
			returndoc = SIGNAL_E1 # TODO: add jitter?
		elif lastComp == "xmessage":
			body = req.args.get('body')
			caption = req.args.get('caption')
			timeout = req.args.get('timeout')
			icon = req.args.get('icon')
			body = body and body[0]
			caption = caption and caption[0]
			timeout = timeout and int(timeout[0])
			icon = icon and int(icon[0])
			returndoc = "UNHANDLED METHOD"
		elif lastComp == "osdshot":
			display = get('display', 'yes')
			if True: #creating osdshot succeeded ;-)
				if display == "yes":
					req.setResponseCode(307)
					req.setHeader("location", "/root/tmp/osdshot.png")
					returndoc = "+ok"
				else:
					returndoc = CLOSEWINDOW_E1 % ("",)
			else:
				returndoc = "-error"
		elif lastComp == "osdshot.png":
			returndoc = "UNHANDLED METHOD"
# NEUTRINO
		elif lastComp == "info":
			returndoc = "UNHANDLED METHOD"
		elif lastComp == "zapto":
			# action depends on arg, there are fixed value but if you give a service name or id it will zap to that channel
			returndoc = "UNHANDLED METHOD"
		elif lastComp == "getbouquets":
			returndoc = BOUQUETS_NEUTRINO
		elif lastComp == "getbouquet":
			mode = get("mode", "TV") # not actually default, default is current
			xml = True if get("xml", "") != "" else False
			bouquet = int(get("bouquet", 0))
			if mode != "TV" or not xml or bouquet != 1:
				returndoc = "UNHANDLED METHOD"
			else:
				returndoc = SERVICES_BOUQUET_NEUTRINO
		elif lastComp == "getbouquetsxml":
			if EMULATE_NEUTRINOHD:
				returndoc = SERVICES_NEUTRINOHD
			else:
				returndoc = SERVICES_NEUTRINO
		elif lastComp == "epg":
			isXml = True if get('xml', 'false') == 'true' else False
			sRef = req.args.get('channelId') or req.args.get('channelid') # XXX: api suggest channelid is correct though channelId seems to be ok too
			sRef = sRef and sRef[0]
			sname = req.args.get('channel_name')
			sname = sname and sname[0]
			details = req.args.get('details')
			details = True if details and details[0] == 'true' else False
			max = int(get('max', -1))
			if not isXml:
				returndoc = "UNHANDLED METHOD"
			else:
				if sRef and sRef in ("d175", "2718f001d175", "1922718f001d175") or sname and sname == "Demo Service":
					add = ''
					if max != 0:
						add = EPGSERVICE_NEUTRINO_ENTRY % (EPGSERVICE_NEUTRINO_DETAILS if details else '',)
					returndoc = EPGSERVICE_NEUTRINO % ("1922718f001d175" if EMULATE_NEUTRINOHD else "2718f001d175", add,)
				else:
					returndoc = "UNHANDLED METHOD"
		elif lastComp == "timer":
			format = get('format', '')
			useId = True if format == 'id' else False
			action = get('action')
			# according to nhttpd source format != "" also results in timerlist
			if not action or format:
				returndoc = state.getTimers(TYPE_NEUTRINO, useId=useId)
			elif action == "new":
				start = int(get('alarm', 0))
				stop = int(get('stop', 0))
				type = int(get('type', 0))
				name = get('channel_id', get('channel_name', ''))

				# check if this is the demo service
				if name in ("1922718f001d175", "2718f001d175", "Demo Service"):
					sRef = '1:0:1:445D:453:1:C00000:0:0:0:'
					timer = state.addTimer(sRef, start, stop, '', '', len(state.timers)+999, 0, 0, 0, 0)
					timer.justplay = type == ZAPTO
					returndoc = "IMO RETURN OF NEUTRINO SUCKS"
				else:
					returndoc = "WRONG SERVICE, YOU SUCK o0"
			elif action == "modify":
				# TODO: figure out behavior without given id
				id = int(get('id', 0))
				start = int(get('alarm', 0))
				stop = int(get('stop', 0))
				type = int(get('type', 0))
				name = get('channel_id', get('channel_name', ''))
				rep = int(get('rep', 0))
				repcount = int(get('repcount', 0))

				# check if this is the demo service
				if name in ("1922718f001d175", "2718f001d175", "Demo Service"):
					name = '1:0:1:445D:453:1:C00000:0:0:0:'

					idx = 0
					for timer in state.timers:
						if timer.eit == id:
							timer.begin = start
							timer.end = stop
							timer.justplay = type == ZAPTO
							timer.sref = name
							break
						idx += 1
					returndoc = "IMO RETURN OF NEUTRINO SUCKS"
				else:
					returndoc = "WRONG SERVICE, YOU SUCK o0"
			elif action == "remove":
				id = int(get('id', 0))

				idx = 0
				for timer in state.timers:
					if timer.eit == id:
						del state.timers[idx]
						break
					idx += 1
				returndoc = "IMO RETURN OF NEUTRINO SUCKS"
			else:
				returndoc = "UNHANDLED METHOD"
		elif lastComp == "shutdown" or lastComp == "reboot":
			returndoc = "ok"
		elif lastComp == "standby":
			if 'on' in req.args:
				returndoc = "ok"
			elif 'off' in req.args:
				returndoc = "ok"
			else:
				returndoc = "off" # or on :P
		elif lastComp == "volume":
			if 'status' in req.args:
				returndoc = '1' if state.isMuted() else '0'
			elif 'mute' in req.args:
				state.setMuted(True)
				returndoc = 'mute'
			elif 'unmute' in req.args:
				state.setMuted(False)
				returndoc = 'unmute'
			else:
				# gui does not really care about return and i don't feel like implementing this
				returndoc = "whatever dude"
		elif lastComp == "setmode":
			returndoc = "ok"
		elif lastComp == "rcem":
			returndoc = "ok"
		elif req.path == "/control/message":
			if 'nmsg' in req.args:
				returndoc = ''
			elif 'popup' in req.args:
				returndoc = ''
			else:
				returndoc = "UNHANDLED METHOD"
# CUSTOM
		elif lastComp == "RESET":
			state.reset()
			returndoc = "reset of demo server triggered"
		elif lastComp == '':
			# XXX: this actually indicates a trailing slash, but we use this to detect requests for /
			returndoc = """<html><head><title>dreaMote Demo Server</title></head><body>
<pre>Welcome to the dreaMote Demo Server.
This is a really dumb piece of software that emulates the HTTP-APIs to Enigma2, Enigma and Neutrino.

It does in no way claim to be complete or correct, but it can be used to test the functionality of dreaMote.
You may use this to test other software, but keep in mind that this may yield false positive errors in the software.
I welcome you though to tell me about these bugs so they can be fixed in future versions.

Since parts of the functionality removes information from the database (e.g. deleting movies) that normally could not be reversed this software has a reset functionality.</pre>
<a href="/RESET">Just click here!</a><br />
<pre>So have fun testing your software...

Oh, I almost forgot: to change the listening port, just add the one you want to the command line (e.g. python bin/dreamote_demo_server.py 31337)</pre>
</body></html>"""
		else:
			req.setResponseCode(404)
			returndoc = "UNHANDLED DOCUMENT"

		print req.uri, returndoc
		return returndoc

def main(port):
	site = server.Site(Simple())
	print "Listening on port", port
	reactor.listenTCP(port, site)
	reactor.run()

if __name__ == '__main__':
	from sys import argv
	port = 8080 if len(argv) != 2 else int(argv[1])
	main(port)
