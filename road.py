#!/usr/bin/python

import socket, time, sys

class Road():
    def __init__(self, distance):
        self.distance=distance
	self.traffic = []


class Car():
    def __init__(self, accepted_client, road):
    	self.sock = accepted_client[0]
	self.ip = accepted_client[1][0]
        self.road = road

	self.input_buffer = []

	self.next = ThePeaceArchCrossing(self).next

    #def input(self, input):
        #"""Add the input to an array of lines of input for processing."""
        #self.input_buffer += input.split()

    

    def accelerate(self):
        """Add 1 to the speed of the car."""
        self.speed += 1

    def brake(self):
        """Cut the speed of the car in half."""
        self.speed /= 2

    def car_command(self, command):
        print "Handling car command %s" % command

    def get_input(self):
        """Get input from socket if available."""

        try:
	    self.input_buffer.append(self.sock.recv(80)[:-2])
	except socket.error:
	    pass
	# ^ might need to split this on newlines in case we
	#  get multiple or  partial line. would need to handle 
	#  the partial line.

	#if len(self.input_buffer):
	    #self.car_command(input_buffer.pop(0))


    def deny(self, diss=False):
        self.sock.send("Access denied! %s!\n" % 
	    ("Sucker" if diss else "Sorry dude"))
	self.close()


    def close(self):
        self.sock.close()


    def send(self, msg):
        self.sock.send(msg + "\n")


    def say(self, sayer, msg):
        self.send("%s tells you, \"%s\"" % (sayer, msg))


def ThePeaceArchCrossing(car):
    """The experience of a Canadian entering the U.S."""


    car.send("A gruff border guard takes your identification.")
    yield

    
    car.say("a border guard", "Hi there. What's your nationality?")
    yield

    while len(car.input_buffer) == 0: yield

    car.driver = {}

    car.driver["nationality"] = car.input_buffer.pop(0).lower()

    if not car.driver["nationality"].startswith("cana"):
        car.say("a border guard", "Another %s eh. We've been on the look-out for you." % 
	    car.driver["nationality"])
	car.next = TheDeportationProcedure(car).next
	yield

    car.say("a border guard", "OK.. where you headed?")
    yield

    while len(car.input_buffer) == 0: yield

    car.driver["destination"] = car.input_buffer.pop(0).lower()

    if not car.driver["destination"] in ("mexico","tijuana"):
        car.say("a border guard", "Hmm, yeah that's a likely story.")
        car.say("a border guard", "likely story.")
	yield
	car.say("a border guard", "But I'll bet you're really going to Mexico, "
	    "just like those other Canadians.")
	yield
	car.say("a border guard", "You can't pull the wool over our eyes very easy.")
	yield

    car.say("a smiling border guard", "OK, welcome to the U.S.A.")
    car.next = TheDrivingToMexicoExperience().next
    yield 
    
        
def TheDeportationProcedure(car):
    """The experience of being deported."""

    car.send("This may fly in %s, but not here in the U.S.A."
        % car.driver["nationality"])
    yield

    car.send("")
    yield
    
    car.send("You find yourself in the fuselage of a cessna "
        "next to several farm animals,\n"
	"on a plane back to your homeland.")

    car.deny(diss=True)
    yield True


def TheDrivingToMexicoExperience(car):
    """The experience of a Canadian driving to Mexico."""



        



#Start up on a sort of random port 
sport = 4013 + int(time.time()) % 20

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.0.110", sport))
server.setblocking(False)
server.listen(10)

print "Listening on: %d" % sport


master_client_list = []

I5 = Road(1381.29)

try:
    while True:

        #Note the time, check at end of loop.
        begin_time = time.time()

        #Collect new clients
        while True:
            try:
	        tmp_sock = server.accept()
		tmp_sock[0].setblocking(False)

		tmp_sock[0].send("Welcome %s:%s to Canadians Driving to Mexico.\n" 
		    % (tmp_sock[1][0], tmp_sock[1][1]))

                #OK, if no exception then
                I5.traffic.append(Car(tmp_sock, I5))

            except socket.error:
                break


        print "%d cars are driving!   \n" % len(I5.traffic),

        #

        for car in I5.traffic:
            try:
	        car.get_input()
	        if car.next():
		    raise socket.error 
		    #doesn't make sense but feeling lazy
            except socket.error:
	        car.close()
		I5.traffic.pop(I5.traffic.index(car))


        #sleep to make the loop 1 full second.

	time_diff = time.time() - begin_time

	print "%f seconds elapsed." % time_diff

	if time_diff < 1:
	    time.sleep(1-time_diff)

except KeyboardInterrupt:
    for c in I5.traffic:
        c.deny()


    print "All users kicked off :%d!\n" % sport




