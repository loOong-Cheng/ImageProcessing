# -*- coding: utf-8 -*-
import wx
from PIL import Image
from pylab import *
import os
import numpy as np
import serial as se


class KameraPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # dlg = wx.MessageDialog(self, u" 请在TERMINAL中输入点的个数", "About Sample Editor", wx.OK)
        # dlg.ShowModal()
        # dlg.Destroy()

        # 迭代值初始化
        self.i = 0
        self.dirname = '.'
        self.flcoorcamerax = []
        self.flcoorcameray = []
        self.flcoorrealx = []
        self.flcoorrealy = []
        self.fl0 = []
        self.fl1 = []
        self.Ports = ''

        # 打开图像按钮
        self.buttonOpen = wx.Button(self, label=u"打开图像", pos=(20, 5))
        self.Bind(wx.EVT_BUTTON, self.OnclickOpen, self.buttonOpen)

        # 下一个点按钮
        self.buttonNext = wx.Button(self, label=u"继续下一个输入", pos=(20, 110))
        self.Bind(wx.EVT_BUTTON, self.OnclickNext, self.buttonNext)

        # 计算按钮，此时点已全部输入完毕
        self.buttonSave = wx.Button(self, label=u"最后一点输入完毕,开始计算", pos=(230, 5))
        self.Bind(wx.EVT_BUTTON, self.OnclickSave, self.buttonSave)

        # 串口打开
        self.portslist = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7',
                          'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13', 'COM14', 'COM15']
        self.portslabel = wx.StaticText(self, label=u"请选择串口号", pos=(10, 350))
        self.portscombobox = wx.ComboBox(self, pos=(110, 350), size=(
            90, -1), choices=self.portslist, style=wx.CB_DROPDOWN)
        self.PortsOpen = wx.Button(self, label=u"开串口", pos=(190, 350))
        self.Bind(wx.EVT_BUTTON, self.OnclickOpenPorts, self.PortsOpen)
        self.Bind(wx.EVT_COMBOBOX, self.ChangePorts, self.portscombobox)

        # 串口读取
        self.PortsRead = wx.Button(self, label=u"读串口", pos=(10, 370))
        self.Bind(wx.EVT_BUTTON, self.OnclickReadPorts, self.PortsRead)
        # 串口写入
        self.PortsWrite = wx.Button(self, label=u"写串口", pos=(100, 370))
        self.Bind(wx.EVT_BUTTON, self.OnclickWritePorts, self.PortsWrite)

        # 串口关闭
        self.PortsClose = wx.Button(self, label=u"关串口", pos=(190, 370))
        self.Bind(wx.EVT_BUTTON, self.OnclickClosePorts, self.PortsClose)

        # 摄像头坐标的label及text控件初始化
        self.getcoorlabel = wx.StaticText(
            self, label=u"鼠标拾取像素坐标为 :", pos=(0, 30))
        self.coorcamerax = wx.TextCtrl(self, pos=(
            40, 50), size=(70, -1), style=wx.TE_READONLY)
        self.coorcameray = wx.TextCtrl(self, pos=(
            150, 50), size=(70, -1), style=wx.TE_READONLY)

        self.labelcamerax = wx.StaticText(self, label="X:", pos=(10, 50))
        self.labelcameray = wx.StaticText(self, label="Y:", pos=(120, 50))

        # 实际坐标的label及text控件初始化
        self.setcoorlabel = wx.StaticText(
            self, label=u"输入设置实际坐标为 :", pos=(0, 70))

        self.coorrealx = wx.TextCtrl(self, pos=(40, 90), size=(40, -1))
        self.coorrealy = wx.TextCtrl(self, pos=(120, 90), size=(40, -1))

        self.labelrealx = wx.StaticText(self, label="X:", pos=(10, 90))
        self.labelrealy = wx.StaticText(self, label="Y:", pos=(90, 90))

        # 显示数据历史窗口
        self.logger = wx.TextCtrl(self, pos=(10, 150), size=(
            400, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.Bind(wx.EVT_BUTTON, self.OnclickNext, self.logger)

    def askUserForFilename(self, **dialogOptions):
        dialog = wx.FileDialog(self, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename

    def defaultFileDialogOptions(self):
        ''' Return a dictionary with file dialog options that can be
            used in both the save file dialog as well as in the open
            file dialog. '''
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.*')


# 保存图像
    def OnclickOpen(self, event):
        if self.i == 0:

            self.askUserForFilename(
                style=wx.OPEN, **self.defaultFileDialogOptions())
            print self.filename
            print self.dirname
            im = array(Image.open(os.path.join(self.dirname, self.filename)))
            imshow(im)
            print 'Please click 1 points'
            self.x = ginput(1, timeout=300)
            print 'you clicked:', self.x
            self.coorcamerax.SetValue(unicode(self.x[0][0]))
            self.coorcameray.SetValue(unicode(self.x[0][1]))
            show()
            self.i = 1
        else:
            print 'Please click 1 points'
            self.x = ginput(1, timeout=300)
            print 'you clicked:', self.x
            self.coorcamerax.SetValue(unicode(self.x[0][0]))
            self.coorcameray.SetValue(unicode(self.x[0][1]))

# 下一个点
    def OnclickNext(self, event):
        self.flcoorcamerax.append(float(self.coorcamerax.GetValue()))
        self.flcoorcameray.append(float(self.coorcameray.GetValue()))
        self.flcoorrealx.append(float(self.coorrealx.GetValue()))
        self.flcoorrealy.append(float(self.coorrealy.GetValue()))
        self.fl0.append(5.)
        self.fl1.append(1.)

        self.logger.AppendText(u'摄像头坐标/实际坐标-（第%d个点）：\n' % (self.i + 1))
        self.logger.AppendText('(%f,%f)/(%f,%f)\n' % (self.flcoorcamerax[self.i], self.flcoorcameray[
                               self.i], self.flcoorrealx[self.i], self.flcoorrealy[self.i]))
        self.i += 1
        self.coorcamerax.SetValue('')
        self.coorcameray.SetValue('')
        self.coorrealx.SetValue('')
        self.coorrealy.SetValue('')
        self.OnclickOpen(self)


# 点选取结束后的总体计算
    def OnclickSave(self, event):
        self.flcoorcamerax.append(float(self.coorcamerax.GetValue()))
        self.flcoorcameray.append(float(self.coorcameray.GetValue()))
        self.flcoorrealx.append(float(self.coorrealx.GetValue()))
        self.flcoorrealy.append(float(self.coorrealy.GetValue()))
        self.fl0.append(0.)
        self.fl1.append(1.)

        self.logger.AppendText(u'摄像头坐标/实际坐标-（最后总共%d个点）：\n' % (self.i + 1))
        self.logger.AppendText('(%f,%f)/(%f,%f)\n' % (self.flcoorcamerax[self.i], self.flcoorcameray[
                               self.i], self.flcoorrealx[self.i], self.flcoorrealy[self.i]))
        self.i += 1
        self.coorcamerax.SetValue(u'敬请')
        self.coorcameray.SetValue(u'等待')
        self.coorrealx.SetValue(u'计算')
        self.coorrealy.SetValue(u'结果')

        # 矩阵运算
        self.stack_camera = np.row_stack(
            (self.flcoorcamerax, self.flcoorcameray, self.fl1))
        self.stack_real = np.row_stack(
            (self.flcoorrealx, self.flcoorrealy, self.fl0, self.fl1))
        self.matrix_camera = np.matrix(self.stack_camera)
        self.matrix_real = np.matrix(self.stack_real)
        self.matrix_camera_T = self.matrix_camera.T
        self.argmatrx = self.matrix_real.dot(self.matrix_camera_T).dot(
            (self.matrix_camera.dot(self.matrix_camera_T)).I)
        print self.argmatrx
        pass

# 串口打开
    def OnclickOpenPorts(self, event):
        self.ser = se.Serial('/dev/cu.wchusbserial1410', 57600, timeout=1)

# 串口关闭
    def OnclickClosePorts(self, event):
        self.ser.close()

# 串口读取
    def OnclickReadPorts(self, event):
        self.ser10 = self.ser.read(10)  # read up tp ten bytes
        # self.ser1 = ser.read()  # read one byte
        #self.serline = self.ser.readline()
        print '1'
        print self.ser10

# 串口写入
    def OnclickWritePorts(self, event):
        self.ser.write("???")

# 串口更改
    def ChangePorts(self, event):
        self.Ports = '/dev/cu.wchusbserial1410'
        self.logger.AppendText(u"您选择串口号为: %s \n" % self.Ports)


app = wx.App(False)
frame = wx.Frame(None)
panel = KameraPanel(frame)
frame.Show()
app.MainLoop()
