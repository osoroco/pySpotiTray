#!/usr/bin/python
import dbus
import os.path
from PyQt4 import QtGui,QtCore

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
def pauseSong():
    spotify_interface.Pause()
def playSong():
    spotify_interface.Play()
def prevSong():
    spotify_interface.Previous()
def isPlaying():
    status = str(spotify_properties.Get("org.mpris.MediaPlayer2.Player","PlaybackStatus"))
    if status == "Paused":
        return False
    elif status == "Playing":
        return True
def getIcon():
    if os.path.exists('/usr/share/spotify/icons/spotify-linux-24.png'):
        icon = QtGui.QIcon('/usr/share/spotify/icons/spotify-linux-24.png')
        return icon
    else:
        import urllib
        url = "https://raw.githubusercontent.com/osoroco/pySpotiTray/master/spotify-linux-24.png"
        pix = QtGui.QPixmap()
        pix.loadFromData(urllib.urlopen(url).read())
        icon = QtGui.QIcon(pix)
        return icon

class RightClickMenu(QtGui.QMenu):
    def __init__(self,parent=None):
        QtGui.QMenu.__init__(self,"File",parent)

        self.current_song = QtGui.QAction(getSong(),self)
        self.current_song.setEnabled(False)
        self.addAction(self.current_song)

        self.play_song = QtGui.QAction("Play",self)
        self.play_song.triggered.connect(playSong)
        self.addAction(self.play_song)

        next_song = QtGui.QAction("Next",self)
        next_song.triggered.connect(nextSong)
        self.addAction(next_song)

        prev_song = QtGui.QAction("Previous",self)
        prev_song.triggered.connect(prevSong)
        self.addAction(prev_song)

        exitAction = QtGui.QAction("&Exit",self)
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.addAction(exitAction)

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self,parent=None):
        QtGui.QSystemTrayIcon.__init__(self,parent)
        self.setIcon(getIcon())
        self.right_menu=RightClickMenu()
        self.setContextMenu(self.right_menu)
        self.setToolTip(getSong())
        self.activated.connect(self.onTrayIconActivated)
    def event(self,event):
        if event.type() == QtCore.QEvent.ToolTip:
            self.setToolTip(getSong())
            self._last_event_post = event.globalPos()
            return True
        elif event.type() == QtCore.QEvent.Leave:
            self._last_event_post = None
            QtGui.QToolTip.hideText()
    def onTrayIconActivated(self,reason):
        if reason == QtGui.QSystemTrayIcon.Context:
            if isPlaying():
                self.right_menu.play_song.setText("Pause")
                self.right_menu.play_song.triggered.connect(pauseSong)
            else:
                self.right_menu.play_song.setText("Play")
                self.right_menu.play_song.triggered.connect(playSong)
            self.right_menu.current_song.setText(getSong())
    def show(self):
        QtGui.QSystemTrayIcon.show(self)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    tray = SystemTrayIcon()
    tray.show()
    app.exec_()
