import keyboard

#Separates Time Automatically For Time Textbox
def Time(Time):
    if len(Time.get()) >= 2 and len(Time.get()) < 3:
        Time.insert(2, ":")
    if len(Time.get()) >= 5 and len(Time.get()) < 6:
        Time.insert(5, ":")
    if keyboard.is_pressed('backspace'):
        Time.delete(len(Time.get()) - 1)
    Time.delete(7, "end")
    print(Time.get())
