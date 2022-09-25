import wx
import wx.lib.newevent
import os

drop_event, EVT_DROP_EVENT = wx.lib.newevent.NewEvent()

class DropTarget(wx.FileDropTarget):
    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.obj = parent

    def OnDropFiles(self, x, y, filenames):
        files = self.get_nested_files(filenames)
        evt = drop_event(data=files)
        wx.PostEvent(self.obj.frame, evt)
        return True
    
    def get_nested_files(self, filenames):
        temp_path = []
        for path in filenames:
            if os.path.isfile(path):
                temp_path.append(path)
            if os.path.isdir(path):
                for curDir, deep_dirs, files in os.walk(path):
                    for file in files:
                        temp_path.append(os.path.join(curDir, file))
        return temp_path

class GUI:
    def __init__(self):
        self.frame = wx.Frame(None, -1, 'list')
        self.frame.SetTitle(u'Drop Here')
        self.frame.Centre()
        panel = wx.Panel(self.frame, wx.ID_ANY, size=(200,200))
        panel.SetToolTip(u'Drop Here')
        text = wx.StaticText(panel, wx.ID_ANY, 'Drop Files Here')

        self.frame.drop = DropTarget(self)
        self.frame.SetDropTarget(self.frame.drop)
        self.frame.Bind(EVT_DROP_EVENT, self.OnDropped)

        self.frame.Show()
    
    def OnDropped(self, event):
        self.frame.data = event.data
        self.frame.Close(True)

def get_filelist() -> list[str]:
    app = wx.App()
    gui = GUI()
    app.SetTopWindow(gui.frame)
    app.MainLoop()
    return gui.frame.data


if __name__ == '__main__':
    test = get_filelist()
    print(test)