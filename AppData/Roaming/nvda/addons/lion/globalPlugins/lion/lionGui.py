#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.9pre on Thu Sep  5 22:20:20 2019
#

import wx
import config
# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

sizer=None
class frmMain(wx.Frame):
	def fillPercents(self):
		return [str(i) for i in range(0,101)]
		
	def __init__(self, *args, **kwds):
		global sizer
		# begin wxGlade: frmMain.__init__
		print("a")
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetSize((400, 300))
		self.SetTitle(_("LION Settings"))
		
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		
		self.panel_1 = wx.Panel(self, wx.ID_ANY)
		sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
		
		sizer_2 = wx.WrapSizer(wx.HORIZONTAL)
		
		lblINterval = wx.StaticText(self.panel_1, wx.ID_ANY, _("Interval:"))
		sizer_2.Add(lblINterval, 0, 0, 0)
		
		self.chcInterval = wx.Choice(self.panel_1, wx.ID_ANY, choices=[_("0.1"), _("0.2")])
		self.chcInterval.SetSelection(0)
		self.chcInterval.SetItems([str(i/10.0) for i in range(1,101)])
		sizer_2.Add(self.chcInterval, 0, 0, 0)
		
		lblTarget = wx.StaticText(self.panel_1, wx.ID_ANY, _("OCR:"))
		sizer_2.Add(lblTarget, 0, 0, 0)
		
		self.clbTarget = wx.CheckListBox(self.panel_1, wx.ID_ANY, choices=[_("Navigator object"), _("Whole Screen"), _("current window"), _("current control")], style=wx.LB_SINGLE)
		self.clbTarget.SetSelection(0)
		sizer_2.Add(self.clbTarget, 0, 0, 0)
		
		lblSimilarityThreshold = wx.StaticText(self.panel_1, wx.ID_ANY, _("Text similarity threshold:"))
		sizer_2.Add(lblSimilarityThreshold, 0, 0, 0)
		
		self.chcThreshold = wx.Choice(self.panel_1, wx.ID_ANY, choices=[_("choice 1")])
		self.chcThreshold.SetSelection(0)
		self.chcThreshold.SetItems([str(i/100.0) for i in range(1,101)])
		sizer_2.Add(self.chcThreshold, 0, 0, 0)
		
		lblCropUp = wx.StaticText(self.panel_1, wx.ID_ANY, _("Crop pixels from above (%):"))
		sizer_2.Add(lblCropUp, 0, 0, 0)
		
		self.chcCropUp = wx.Choice(self.panel_1, wx.ID_ANY, choices=[_("choice 1")])
		self.chcCropUp.SetSelection(0)
		self.chcCropUp.SetItems(self.fillPercents())
		sizer_2.Add(self.chcCropUp, 0, 0, 0)
		
		lblCropDown = wx.StaticText(self.panel_1, wx.ID_ANY, _("crop pixels from below(%):"))
		sizer_2.Add(lblCropDown, 0, 0, 0)
		
		self.chcCropDown = wx.Choice(self.panel_1, wx.ID_ANY, choices=[_("choice 1")])
		self.chcCropDown.SetSelection(0)
		self.chcCropDown.SetItems(self.fillPercents())
		sizer_2.Add(self.chcCropDown, 0, 0, 0)
		
		lblCropLeft = wx.StaticText(self.panel_1, wx.ID_ANY, _("crop pixels from left(%):"))
		sizer_2.Add(lblCropLeft, 0, 0, 0)
		
		self.chcCropLeft = wx.Choice(self.panel_1, wx.ID_ANY, choices=[_("choice 1")])
		self.chcCropLeft.SetSelection(0)
		self.chcCropLeft.SetItems(self.fillPercents())
		sizer_2.Add(self.chcCropLeft, 0, 0, 0)
		
		lblCropRight = wx.StaticText(self.panel_1, wx.ID_ANY, _("crop pixels from right (%):"))
		sizer_2.Add(lblCropRight, 0, 0, 0)
		
		self.chcCropRight = wx.Choice(self.panel_1, wx.ID_ANY, choices=[_("choice 1")])
		self.chcCropRight.SetSelection(0)
		self.chcCropRight.SetItems(self.fillPercents())
		sizer_2.Add(self.chcCropRight, 0, 0, 0)
		
		self.btnSaveProfile = wx.Button(self.panel_1, wx.ID_ANY, _("Save current settings as a new profile"))
		self.btnSaveProfile.Enable(False)
		sizer_2.Add(self.btnSaveProfile, 0, 0, 0)
		
		self.btnOk = wx.Button(self.panel_1, wx.ID_ANY, _("OK"))
		sizer_2.Add(self.btnOk, 0, 0, 0)
		
		self.btnCancel = wx.Button(self.panel_1, wx.ID_ANY, _("Cancel"))
		sizer_2.Add(self.btnCancel, 0, 0, 0)
		
		self.panel_1.SetSizer(sizer_2)
		
		self.SetSizer(sizer_1)
		
		self.Layout()

		self.Bind(wx.EVT_BUTTON, self.btnOk_click, self.btnOk)
		self.Bind(wx.EVT_BUTTON, self.btnCancel_click, self.btnCancel)
		# end wxGlade
		self.chcCropUp.SetSelection(config.conf["lion"]["cropUp"])
		self.chcCropLeft.SetSelection(config.conf["lion"]["cropLeft"])
		self.chcCropDown.SetSelection(config.conf["lion"]["cropDown"])
		self.chcCropRight.SetSelection(config.conf["lion"]["cropRight"])
		self.chcInterval.SetSelection(int((config.conf["lion"]["interval"]*10)-1))
		self.clbTarget.SetSelection(config.conf["lion"]["target"])
		self.chcThreshold.SetSelection(int((config.conf["lion"]['threshold']*100)-1))

	def btnOk_click(self, event):  # wxGlade: frmMain.<event_handler>
		config.conf["lion"]["cropUp"]=self.chcCropUp.GetSelection()
		config.conf["lion"]["cropLeft"]=self.chcCropLeft.GetSelection()
		config.conf["lion"]["cropDown"]=self.chcCropDown.GetSelection()
		config.conf["lion"]["cropRight"]=self.chcCropRight.GetSelection()
		config.conf["lion"]["interval"]=float(self.chcInterval.GetString(self.chcInterval.GetSelection()))
		config.conf["lion"]["threshold"]=float(self.chcThreshold.GetString(self.chcThreshold.GetSelection()))
		config.conf["lion"]["target"]=self.clbTarget.GetSelection()
		
		self.Close()
		event.Skip()

	def btnCancel_click(self, event):  # wxGlade: frmMain.<event_handler>
		print("Event handler 'btnCancel_click' not implemented!")
		self.Close()
		event.Skip()

# end of class frmMain

class LION(wx.App):
	def OnInit(self):
		self.frame = frmMain(None, wx.ID_ANY, "")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

# end of class LION

if __name__ == "__main__":
	gettext.install("LionGui") # replace with the appropriate catalog name

	LionGui = LION(0)
	LionGui.MainLoop()
