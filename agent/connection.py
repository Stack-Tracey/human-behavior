import labViewConnector
# Returns the non-negative cost of the connection
class Connection():

    def getCost():
        return NULL

# Returns the node that this connection came from
    def getFromNode():
        return null

# Returns the node that this connection leads to
    def getToNode():
        return null


con = labViewConnector.LabViewConnector('192.168.56.101', 1337)
while True:
    a = con.receive_fr()
    b = {'x' : 5} #placeholder for calculating stuff
    con.send_fr(b)

con.close()