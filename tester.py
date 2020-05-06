from tkinter import *

ven = Tk()

#text = text.decode("utf-8")
#print(type(text))
#exit()

def reader():
    _file = open("text.txt", 'rb')
    text = _file.read()
    _file.close()
    return text
ven.createcommand("reader", reader)
ven.tk.eval("""
package require Tk

label .one
pack .one

label .two
pack .two

font create fixedFont  -family Courier   -size 10
font create boldFont   -family Helvetica -size 12 -weight bold

.one configure -text fixedFont -font fixedFont
.two configure -text boldFont -font boldFont
""")

# font create fixedFont  -family Courier   -size 10
# font create boldFont   -family Helvetica -size 12 -weight bold
ven.mainloop()

"""
image create photo ::img::view -format GIF -data {
    R0lGODlhEAAQAKIHAP///wwMDAAAAMDAwNnZ2SYmJmZmZv///yH5BAEAAAcALAAA
    AAAQABAAAANMKLos90+ASamDRxJCgw9YVnlDOXiQBgRDBRgHKE6sW8QR3doPKK27
    yg33q/GIOhdg6OsEJzeZykiBSUcs06e56Xx6np8ScIkFGuhQAgA7
}
"""