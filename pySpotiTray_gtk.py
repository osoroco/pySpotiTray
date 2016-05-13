#!/usr/bin/python
import dbus
import gtk
import os.path

session_bus = dbus.SessionBus()
spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify","/org/mpris/MediaPlayer2")
spotify_interface = dbus.Interface(spotify_bus,'org.mpris.MediaPlayer2.Player')
spotify_properties = dbus.Interface(spotify_bus,"org.freedesktop.DBus.Properties")
def getSong():
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player","Metadata")
    artist = str(metadata['xesam:artist'][0])
    song = str(metadata['xesam:title'])
    return artist+" - "+song
def nextSong():
    spotify_interface.Next()
def pauseSong(null):
    spotify_interface.Pause()
def playSong(null):
    spotify_interface.Play()
def prevSong():
    spotify_interface.Previous()
def isPlaying():
    status = str(spotify_properties.Get("org.mpris.MediaPlayer2.Player","PlaybackStatus"))
    if status == "Paused":
        return False
    elif status == "Playing":
        return True

def next_song(event):
    nextSong()
def prev_song(event):
    prevSong()
def quit(event):
    try:
        os.remove('/tmp/spot_tray_icon.png')
        exit()
    except OSError:
        exit()

def make_menu(event_button, event_time, data=None):
    menu=gtk.Menu()
    if isPlaying():
        play_mnu = gtk.MenuItem("Pause")
        play_mnu.connect_object("activate", pauseSong,"PlayPause")
    else:
        play_mnu = gtk.MenuItem("Play")
        play_mnu.connect_object("activate", playSong,"PlayPause")
    current_mnu = gtk.MenuItem(getSong())
    next_mnu = gtk.MenuItem("Next")
    prev_mnu = gtk.MenuItem("Previous")
    exit_mnu = gtk.MenuItem("Exit")

    menu.append(current_mnu)
    menu.append(play_mnu)
    menu.append(next_mnu)
    menu.append(prev_mnu)
    menu.append(exit_mnu)

    next_mnu.connect_object("activate", next_song,"NextSong")
    prev_mnu.connect_object("activate", prev_song,"PrevSong")
    exit_mnu.connect_object("activate", quit, "Quit")

    current_mnu.show()
    current_mnu.set_sensitive(False)
    play_mnu.show()
    next_mnu.show()
    prev_mnu.show()
    exit_mnu.show()
    menu.popup(None,None,None, event_button, event_time)

def on_right_click(data, event_button, event_time):
    make_menu(event_button, event_time)
def on_left_click(event):
    print "we should play/pause here"
def getIcon():
    if os.path.exists('/usr/shar/spotify/icons/spotify-linux-24.png'):
        return gtk.status_icon_new_from_file('/usr/share/spotify/icons/spotify-linux-24.png')
    else:
        import urllib
        f = open('/tmp/spot_tray_icon.png',"w")
        url = "https://raw.githubusercontent.com/osoroco/pySpotiTray/master/spotify-linux-24.png"
        f.write(urllib.urlopen(url).read())
        f.close()
        return gtk.status_icon_new_from_file('/tmp/spot_tray_icon.png')


if __name__ == '__main__':
    icon = getIcon()
    icon.set_tooltip('poop')
    icon.connect('popup-menu',on_right_click)
    icon.connect('activate', on_left_click)
    gtk.main()
