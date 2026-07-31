import queue

Called_Queue = queue.Queue()

#Clean Redundant Codes From Called Number To Get Main Number
def Modifier(Number):
    # If Number Contains 9 At The Beginning
    if str(Number).startswith('9') and len(Number) > 4:
        New_Number = str(Number[1:])
        # If Modified Number Contains '42170' At The Beginning
        if str(New_Number).startswith('42170'):
            New_Number = str(Number[5:])
            return Analyzer(New_Number)
        # If Modified Number Contains '21' At The Beginning
        elif str(New_Number).startswith('21') and len(Number) > 4:
            New_Number = str(Number[2:])
            return Analyzer(New_Number)
        else:
            return Analyzer(New_Number)
    # If Number Contains '42170' At The Beginning
    elif str(Number).startswith('42170') and len(Number) > 4:
        New_Number = str(Number[5:])
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
             Called = [('خارجي', Number)]
             Called_Queue.put(Called)
         elif len(Number) == 4:
             Called = [('کارگزاري', Number)]
             Called_Queue.put(Called)
         elif len(Number) == 3:
             Called = [('صندوق', Number)]
             Called_Queue.put(Called)
         elif len(Number) < 3:
             Called = [('نامعتبر', Number)]
             Called_Queue.put(Called)
     except:
         Called = [("None", "None")]
         Called_Queue.put(Called)
