#-*-encoding:utf-8-*-'
import sys, glob, os
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QMainWindow, QListWidget, QLineEdit, QPushButton, QApplication, QFileDialog, QCheckBox

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('imageviewer.ui', self)
        self.setWindowTitle('Image Viewer')
        self.setWindowIcon(QIcon('viewer.ico'))

        self.lineInput = self.findChild(QLineEdit,'lineInput')
        self.buttonInput = self.findChild(QPushButton, 'buttonInput')
        self.listFiles = self.findChild(QListWidget, 'listFiles')
        self.buttonOpen = self.findChild(QPushButton, 'buttonOpen')
        self.imageView = self.findChild(QLabel, 'imageView')
        self.fixSize = self.findChild(QCheckBox, 'fixSize')

        ## connections
        self.buttonInput.clicked.connect(self.open_directory)
        self.buttonOpen.clicked.connect(self.make_filelist)
        self.listFiles.currentItemChanged.connect(self.show_image)

    def open_directory(self):
        tmp_directory = str(QFileDialog.getExistingDirectory(self, 'Select Directory'))
        self.lineInput.setText(tmp_directory)

    def make_filelist(self):
        self.listFiles.clear()
        self.directory = self.lineInput.text()
        files = []
        files += glob.glob(self.directory + '/*.png')
        files += glob.glob(self.directory + '/*.jpg')
        files += glob.glob(self.directory + '/*.bmp')
        files += glob.glob(self.directory + '/*.jpeg')
        files += glob.glob(self.directory + '/*.gif')

        files = sorted(files)

        for i in range(len(files)):
            self.listFiles.insertItem(i, os.path.basename(files[i]))
        self.listFiles.setCurrentItem(self.listFiles.item(0))

    def show_image(self):
        try:
            pixmap = QPixmap(self.directory + '/'+ self.listFiles.currentItem().text())
            if pixmap.width() > pixmap.height():
                if pixmap.width() > 1080:
                    pixmap = pixmap.scaledToWidth(1080)
                else:
                    pixmap = pixmap.scaledToWidth(pixmap.width())
            else:
                if pixmap.height() > 720:
                    pixmap = pixmap.scaledToHeight(720)
                else:
                    pixmap = pixmap.scaledToHeight(pixmap.height())

            self.imageView.setPixmap(pixmap)
            if not self.fixSize.isChecked():
                self.resize(pixmap.size())
        except:
            pass

def main():
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()