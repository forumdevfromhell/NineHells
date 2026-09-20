# Python exceptions are the internal protocol: class=message type, args=payload.
class HellMessage(Exception): pass
class AuthMessage(HellMessage): pass
class IntegrityMessage(HellMessage): pass
class ModerationMessage(HellMessage): pass
class EventMessage(HellMessage): pass

def rpc(message):
    try:
        raise message
    except HellMessage as delivered:
        return delivered.args
