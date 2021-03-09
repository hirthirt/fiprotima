from pubsub import pub

def log_message(message, lvl):
    pub.sendMessage("logging", message=message, lvl=lvl)