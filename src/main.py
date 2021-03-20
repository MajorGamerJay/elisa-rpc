import dbus

from time import sleep
from collections import deque
from datetime import timedelta as td

# Declare session bus from D-Bus.
session_bus = dbus.SessionBus()

# Proxy object for getting Elisa's Bus.
while True:
    try:
        elisa = session_bus.get_object('org.mpris.MediaPlayer2.elisa',
            '/org/mpris/MediaPlayer2')
    except dbus.exceptions.DBusException:
        print('Couldn\'t connect to Elisa\'s Bus')
        sleep(5)
    else:
        break

# Elisa interface for D-Bus
elisa_interface = dbus.Interface(elisa, dbus_interface='org.mpris.MediaPlayer2.Player')

# Properties interface for Elisa
elisa_properties = dbus.Interface(elisa, dbus_interface='org.freedesktop.DBus.Properties')

# Metadata interface
metadata = elisa_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

# Add list of artists to one variable and declare it by popping by dequed
while True:
    while True:
        try:
            track_length = str(td(microseconds=metadata.get('mpris:length')))
        except TypeError:
            print('Could not get length metadata. Please restart the program \
                    after playing a song.')
            sleep(5)
        else:
            print('Got length metadata of song')
            break

    track_name = metadata.get('xesam:title') or meta.get('xesam:url')
    track_artists = metadata.get('xesam:artist')

    if track_artists:
        track_artists = deque(track_artists)
        track_artist = track_artists.popleft()
        while len(track_artists) > 0:
            track_artist = track_artist + ', ' + track_artists.popleft()

    print(f'{str(elisa_properties.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus"))}: "{track_name}" by {track_artist}')

    # Sleep to increase count
    sleep(15)
