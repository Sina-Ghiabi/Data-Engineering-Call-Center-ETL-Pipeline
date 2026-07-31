import keyboard

#Separates Date Automatically For Time Textbox
def Date(Date):
    if len(Date.get()) >= 4 and len(Date.get()) < 5:
        Date.insert(4, "/")
    if len(Date.get()) >= 7 and len(Date.get()) < 8:
        Date.insert(7, "/")
    if keyboard.is_pressed('backspace'):
        Date.delete(len(Date.get()) - 1)
    if len(Date.get()) >= 9 and len(Date.get()) < 10:
        Date.insert(9, "/")
    Date.delete(9, "end")
    print(Date.get())
