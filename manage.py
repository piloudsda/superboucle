from PyQt5.QtWidgets import QDialog, QFileDialog
from manage_ui import Ui_Dialog
from learn import LearnDialog
from device import Device
from clip import verify_ext
import json
from os.path import expanduser


class ManageDialog(QDialog, Ui_Dialog):

    def __init__(self, parent):
        super(ManageDialog, self).__init__(parent)
        self.gui = parent
        self.setupUi(self)
        for device in self.gui.devices[1:]:
            self.list.addItem(device.name)
        self.editButton.clicked.connect(self.onEdit)
        self.deleteButton.clicked.connect(self.onDelete)
        self.importButton.clicked.connect(self.onImport)
        self.exportButton.clicked.connect(self.onExport)
        self.finished.connect(self.onFinished)
        self.show()

    def onEdit(self):
        if self.list.currentRow() != -1:
            device = self.gui.devices[self.list.currentRow() + 1]
            self.gui.learn_device = LearnDialog(self.gui,
                                                self.updateDevice,
                                                device)
            self.gui.is_learn_device_mode = True

    def onDelete(self):
        if self.list.currentRow() != -1:
            device = self.gui.devices[self.list.currentRow() + 1]
            self.gui.devices.remove(device)
            self.list.takeItem(self.list.currentRow())

    def onImport(self):
        file_name, a = (
            QFileDialog.getOpenFileName(self,
                                        'Open file',
                                        expanduser('~'),
                                        'Super Boucle Mapping (*.sbm)'))
        with open(file_name, 'r') as f:
            read_data = f.read()
        mapping = json.loads(read_data)
        self.list.addItem(mapping['name'])
        self.gui.devices.append(Device(mapping))

    def onExport(self):
        device = self.gui.devices[self.list.currentRow() + 1]
        file_name, a = (
            QFileDialog.getSaveFileName(self,
                                        'Save As',
                                        expanduser('~'),
                                        'Super Boucle Mapping (*.sbm)'))

        if file_name:
            file_name = verify_ext(file_name, 'sbm')
            with open(file_name, 'w') as f:
                f.write(json.dumps(device.mapping))

    def onFinished(self):
        self.gui.updateDevices()

    def updateDevice(self, device):
        self.list.clear()
        for device in self.gui.devices[1:]:
            self.list.addItem(device.name)
        self.gui.is_learn_device_mode = False
        self.gui.redraw()
