from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QRectF, Qt, QTimer
from gui import *

class Logic(QMainWindow, Ui_MainWindow):
    MIN_VOLUME = 0
    MAX_VOLUME = 9
    MIN_CHANNEL = 0
    MAX_CHANNEL = 9
    def __init__(self) -> None:
        """
        Method to set default values of television object.
        """
        super().__init__()
        self.setupUi(self)

        self.__status = False
        self.__muted = False
        self.__volume = Logic.MIN_VOLUME
        self.__channel = Logic.MIN_CHANNEL

        #Setup for GraphicView, necessary for linking images
        self.scene = QGraphicsScene(self.view_screen)
        self.view_screen.setScene(self.scene)
        self.screen_item = self.scene.addPixmap(QPixmap())
        QTimer.singleShot(0, self.set_screen)

        self.display_ch.display(self.__channel)
        self.display_vol.display(self.__volume)

        #Buttons and sliders
        self.button_vol_up.clicked.connect(lambda: self.volume_up())
        self.button_vol_down.clicked.connect(lambda: self.volume_down())
        self.button_ch_up.clicked.connect(lambda: self.channel_up())
        self.button_ch_down.clicked.connect(lambda: self.channel_down())
        self.button_power.clicked.connect(lambda: self.power())
        self.button_mute.clicked.connect(lambda: self.mute())
        self.slider_channel.valueChanged.connect(lambda: self.set_channel())
        self.slider_volume.valueChanged.connect(lambda: self.set_volume())

    def refresh_window(self) -> None:
        """
        Refreshes window to all current attribute states
        """
        self.display_ch.display(self.__channel if self.__status else 0)
        self.slider_channel.setValue(self.__channel if self.__status else 0)

        self.display_vol.display(0 if not self.__status or self.__muted else self.__volume)
        self.slider_volume.setValue(0 if not self.__status or self.__muted else self.__volume)
        self.set_screen()

    def power(self) -> None:
        """
        Toggles the TV power.
        """
        self.__status = not self.__status
        self.refresh_window()

    def mute(self) -> None:
        """
        Toggles the mute status if TV is on.
        """
        if self.__status:
            self.__muted = not self.__muted
            self.display_vol.display(self.__volume if not self.__muted else 0)
            self.slider_volume.setValue(self.__volume if not self.__muted else 0)

    def set_screen(self) -> None:
        """
        Loads channel image and fits view
        """
        if self.__status:
            picture = QPixmap(f"images/ch{self.__channel}.png")
        else:
            picture = QPixmap(f"images/nothingness.png")
        self.screen_item.setPixmap(picture)
        self.scene.setSceneRect(QRectF(picture.rect()))
        self.view_screen.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.IgnoreAspectRatio)

    def set_channel(self) -> None:
        """
        Updates channel from slider or moves to zero when powered off
        """
        if self.__status:
            self.__channel=self.slider_channel.value()
            self.display_ch.display(self.__channel)
            self.refresh_window()
        else:
            self.slider_channel.setValue(0)

    def set_volume(self) -> None:
        """
        Update volume from slider when on and not muted
        """
        if self.__status and not self.__muted:
            self.__volume = self.slider_volume.value()
            self.display_vol.display(self.__volume)

    def channel_up(self) -> None:
        """
        Increments the channel by 1, changes to minimum if at max when called
        """
        if self.__status:
            if self.__channel >= Logic.MAX_CHANNEL:
                self.__channel = Logic.MIN_CHANNEL
            else:
                self.__channel += 1
        self.refresh_window()

    def channel_down(self) -> None:
        """
        Decrements the channel by 1, changes to max if at minimum when called
        """
        if self.__status:
            if self.__channel <= Logic.MIN_CHANNEL:
                self.__channel = Logic.MAX_CHANNEL
            else:
                self.__channel -= 1
        self.refresh_window()

    def volume_up(self) -> None:
        """
        Increments the volume by 1 and resets mute status, volume remains unchanged if called at max.
        """
        if self.__status:
            self.__muted = False
            if self.__volume < Logic.MAX_VOLUME:
                self.__volume += 1
                self.refresh_window()

    def volume_down(self) -> None:
        """
        Decrements the volume by 1 and resets mute status, volume remains unchanged if called at min.
        """
        if self.__status:
            self.__muted = False
            if self.__volume > Logic.MIN_VOLUME:
                self.__volume -= 1
                self.refresh_window()