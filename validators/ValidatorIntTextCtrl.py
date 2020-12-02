import wx


# Validates data as it is entered into the first year and last year controls.
class ValidatorIntTextCtrl(wx.Validator):

    def __init__(self):
        wx.Validator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):

        return ValidatorIntTextCtrl()

    def Validate(self, win):

        return True

    def TransferToWindow(self):

        return True

    def TransferFromWindow(self):

        return True

    @staticmethod
    def OnChar(event):

        keycode = int(event.GetKeyCode())

        if keycode < 256:
            key = chr(keycode)
            if not key.isdigit() and key != '\b' and keycode != 127:
                return

        event.Skip()
