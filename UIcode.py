from PyQt5 import QtCore, QtWidgets
import EC2script
import S3script
import RDSscript
import sys
import os

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(413, 496)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(50, 60, 311, 141))
        self.listWidget.setObjectName("listWidget")
        self.EC2check = QtWidgets.QCheckBox(Dialog)
        self.EC2check.setGeometry(QtCore.QRect(60, 110, 111, 17))
        self.EC2check.setObjectName("EC2check")
        self.S3check = QtWidgets.QCheckBox(Dialog)
        self.S3check.setGeometry(QtCore.QRect(60, 140, 101, 17))
        self.S3check.setObjectName("S3check")
        self.RDScheck = QtWidgets.QCheckBox(Dialog)
        self.RDScheck.setGeometry(QtCore.QRect(60, 170, 111, 17))
        self.RDScheck.setObjectName("RDScheck")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 70, 271, 31))
        self.label.setObjectName("label")
        self.AccessID = QtWidgets.QLineEdit(Dialog)
        self.AccessID.setGeometry(QtCore.QRect(130, 220, 231, 20))
        self.AccessID.setObjectName("AccessID")
        self.AccountID = QtWidgets.QLineEdit(Dialog)
        self.AccountID.setGeometry(QtCore.QRect(130, 330, 231, 20))
        self.AccountID.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.AccountID.setObjectName("AccountID")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 220, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 250, 71, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(50, 330, 71, 16))
        self.label_4.setObjectName("label_4")
        self.SecretKey = QtWidgets.QTextEdit(Dialog)
        self.SecretKey.setGeometry(QtCore.QRect(130, 250, 231, 71))
        self.SecretKey.setObjectName("SecretKey")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 370, 311, 16))
        self.label_5.setObjectName("label_5")
        self.FolderName = QtWidgets.QLineEdit(Dialog)
        self.FolderName.setGeometry(QtCore.QRect(50, 400, 231, 20))
        self.FolderName.setObjectName("FolderName")
        self.browse_button = QtWidgets.QPushButton(Dialog)
        self.browse_button.setGeometry(QtCore.QRect(290, 400, 71, 23))
        self.browse_button.setObjectName("browse_button")
        self.run = QtWidgets.QPushButton(Dialog)
        self.run.setGeometry(QtCore.QRect(320, 460, 75, 23))
        self.run.setObjectName("run")

        self.browse_button.clicked.connect(self.get_directory_name)
        self.run.clicked.connect(self.run_program)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def get_directory_name(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        directory = file_dialog.getExistingDirectory(None, "Select Directory")
        self.FolderName.setText(directory)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.EC2check.setText(_translate("Dialog", "EC2 instances"))
        self.S3check.setText(_translate("Dialog", "S3 Buckets"))
        self.RDScheck.setText(_translate("Dialog", "RDS instances"))
        self.label.setText(_translate("Dialog", "Select all types of AWS services you wish to assess:"))
        self.label_2.setText(_translate("Dialog", "Access Key ID:"))
        self.label_3.setText(_translate("Dialog", "Secret Key:"))
        self.label_4.setText(_translate("Dialog", "Account ID:"))
        self.label_5.setText(_translate("Dialog", "Where do you wish to save the CSV files:"))
        self.browse_button.setText(_translate("Dialog", "Browse"))
        self.run.setText(_translate("Dialog", "Run"))

        if os.path.exists("creds.tmp"):
            with open("creds.tmp", "r", encoding="utf-8") as f:
                creds = f.readlines()
                self.AccessID.setText(creds[0].replace("\n", ""))
                self.SecretKey.setText(creds[1].replace("\n", ""))
                self.AccountID.setText(creds[2].replace("\n", ""))
                self.FolderName.setText(creds[3].replace("\n", ""))

    def run_program(self):
        access_key_id = self.AccessID.text()
        secret_key = self.SecretKey.toPlainText()
        account_id = self.AccountID.text()
        folder_name = self.FolderName.text()

        ec2_checked = self.EC2check.isChecked()
        s3_checked = self.S3check.isChecked()
        rds_checked = self.RDScheck.isChecked()

        if not (access_key_id and secret_key and account_id and folder_name):
            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Warning)
            message_box.setText("Please fill in all required fields.")
            if not access_key_id:
                message_box.setInformativeText("Access Key ID is required.")
                message_box.setWindowTitle("Access Key ID Required")
                message_box.setDetailedText("Please enter your AWS Access Key ID.")
            elif not secret_key:
                message_box.setInformativeText("Secret Key is required.")
                message_box.setWindowTitle("Secret Key Required")
                message_box.setDetailedText("Please enter your AWS Secret Key.")
            elif not account_id:
                message_box.setInformativeText("Account ID is required.")
                message_box.setWindowTitle("Account ID Required")
                message_box.setDetailedText("Please enter your AWS Account ID.")
            elif not folder_name:
                message_box.setInformativeText("Folder name is required.")
                message_box.setWindowTitle("Folder Name Required")
                message_box.setDetailedText("Please enter the folder where you wish to save the CSV files.")
            message_box.exec_()
        
        with open("creds.tmp", "w", encoding="utf-8") as f:
            f.write(access_key_id + "\n")
            f.write(secret_key + "\n")
            f.write(account_id + "\n")
            f.write(folder_name + "\n")

        if not (ec2_checked or s3_checked or rds_checked):
            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Warning)
            message_box.setText("Please select at least one AWS service.")
            message_box.setWindowTitle("AWS Service Required")
            message_box.setDetailedText("Please select at least one AWS service to assess.")
            message_box.exec_()
        
        if ec2_checked:
            try:
                EC2script.main(access_key_id, secret_access_key=secret_key, path=folder_name)
                message_box = QtWidgets.QMessageBox()
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                message_box.setWindowTitle("Success")
                message_box.setText("EC2 instances assessed successfully.")
                message_box.exec_()
            except:
                message_box = QtWidgets.QMessageBox()
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setText("An error occurred while assessing EC2 instances.\nPlease confirm that the access key and secret key are correct and try again.")
                message_box.setWindowTitle("Error")
                message_box.exec_()
        
        if s3_checked:
            try:
                S3script.main(access_key_id, secret_access_key=secret_key, path=folder_name)
                message_box = QtWidgets.QMessageBox()
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                message_box.setWindowTitle("Success")
                message_box.setText("S3 buckets assessed successfully.")
                message_box.exec_()
                

            except:
                message_box = QtWidgets.QMessageBox()
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setText("An error occurred while assessing S3 buckets.\nPlease confirm that the access key and secret key are correct and try again.")
                message_box.setWindowTitle("Error")
                message_box.exec_()
        
        if rds_checked:
            try:
                RDSscript.main(access_key_id, secret_access_key=secret_key, account_id=account_id, path=folder_name)
                message_box = QtWidgets.QMessageBox()
                message_box.setIcon(QtWidgets.QMessageBox.Information)
                message_box.setWindowTitle("Success!")
                message_box.setText("RDS instances assessed successfully.")
                message_box.exec_()
            except:
                message_box = QtWidgets.QMessageBox()
                message_box.setIcon(QtWidgets.QMessageBox.Warning)
                message_box.setText("An error occurred while assessing RDS instances.\nPlease confirm that the access key, secret key, and account ID are correct and try again.")
                message_box.setWindowTitle("Error")
                message_box.exec_()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
