from Control import PieChart_Module

def Create():
    global Specific_Caller
    global Specific_Called

    def Caller(Number):
        print("Caller")
        Caller_Charts = PieChart_Module.Pie_Chart(Number)
        Caller_Charts.All_Users_Calls()
        Caller_Charts.Analyze_Calls()
        Caller_Charts.Separate_IO_Calls()
        Caller_Charts.All_Users_Input_Calls()
        Caller_Charts.All_Users_Output_Calls()

    def Called(Number):
        print("Called")
        Called_Charts = PieChart_Module.Pie_Chart(Number)
        Called_Charts.All_Users_Calls()
        Called_Charts.Analyze_Calls()
        Called_Charts.Separate_IO_Calls()
        Called_Charts.All_Users_Input_Calls()
        Called_Charts.All_Users_Output_Calls()

    if Specific_Caller != '' and Specific_Called != '':
        Caller(Specific_Caller)
        Called(Specific_Called)
    elif Specific_Caller != '':
        Caller(Specific_Caller)
    elif Specific_Called != '':
        Called(Specific_Called)

    Specific_Caller = ''
    Specific_Called = ''