'''A ludicrously simple event handler, for ludicrously simple events.

Each object that wants to be notified of a particular kind of event
must do two things: register itself with the event handler, and
have a receive_event(event) method.

This event handler was intended to be used with simple event types,
e.g. integers or strings representing types of events. To work with
arbitrary event classes, then an event of a given type must evaluate
as equal to any other event of the same type.
'''

registry = {"_all": []}


def register(object_to_register, *events):
    # First we have to make sure that the object hasn't been
    # registered for all events. Later, during iteration, we
    # will ensure that it hasn't already been registered for
    # particular events.
    if object_to_register in registry["_all"]: return None
    
    # If no event types are given, then the object will
    # be registered for all events.
    if len(events) == 0:
        events = ["_all"]
        # Now we remove dupilate entries for this event
        for event in registry:
            if object_to_register in registry[event]:
                registry[event].remove(object_to_register)
    for event in events:
        try:
            # Here we avoid registering an object for the same
            # event more than once.
            if object_to_register not in registry[event]:
                registry[event].append(object_to_register)
        except KeyError:
            registry[event] = [object_to_register]
            

def fire(event):
    '''Notifies the appropriate objects of the given event by
    calling object.receive_event(event).
    
    NOTE: This function does not test whether an event code is
    valid or not. If you pass it a malformed code, then objects
    registered to receive all events will receive the bad event.
    '''
    try:
        for obj in registry[event]:
            obj.receive_event(event)
    except KeyError:
        pass
        
    # Objects registered to the _all "event" are guaranteed
    # to not be registered for any other events, so this code
    # will not result in objects receiving duplicate events.
    for obj in registry["_all"]:
        obj.receive_event(event)