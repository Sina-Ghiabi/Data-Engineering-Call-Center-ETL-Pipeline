import queue

Caller_Queue = queue.Queue()

#Clean Redundant Codes From Caller Number To Get Main Number
def Modifier(Number):
    # If Number Contains '42170' At The Beginning
    if str(Number).startswith('42170') and len(Number) > 4:
        New_Number = str(Number[5:])
        return Analyzer(New_Number)
    # If Number Contains '2142170' At The Beginning
    elif str(Number).startswith('2142170') and len(Number) > 4:
        New_Number = str(Number[7:])
        return Analyzer(New_Number)
    # If Number Contains '21' At The Beginning
    elif str(Number).startswith('21') and len(Number) > 4:
        New_Number = str(Number[2:])
        return Analyzer(New_Number)
    else:
        return Number

#Find Out Where Was The Number From
def Analyzer(Number):
     try:
         if len(Number) > 4:
             Caller = [('خارجي', Number)]
             Caller_Queue.put(Caller)
         elif len(Number) == 4:
             Caller = [('کارگزاري', Number)]
             Caller_Queue.put(Caller)
         elif len(Number) == 3:
             Caller = [('صندوق', Number)]
             Caller_Queue.put(Caller)
         elif len(Number) < 3:
             Caller = [('نامعتبر', Number)]
             Caller_Queue.put(Caller)
     except:
         Caller = [("None", "None")]
         Caller_Queue.put(Caller)
