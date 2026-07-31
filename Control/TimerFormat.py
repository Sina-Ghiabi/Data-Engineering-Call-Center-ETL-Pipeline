import keyboard

#Separates Timer Automatically For Timer Textbox
def Timer(Time):
    if len(Time.get()) >= 1 and len(Time.get()) < 2:
        Time.insert(1, ":")
    if keyboard.is_pressed('backspace'):
        Time.delete(len(Time.get()) - 1)
    Time.delete(3, "end")
    print(Time.get())
