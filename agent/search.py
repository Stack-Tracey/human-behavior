import sys
import numpy as np ## INSTALL
from copy import deepcopy
from queue import LifoQueue, Queue, PriorityQueue
from timeit import default_timer as timer

# Constants
bound	= 'x'
goal	= 'g'
start	= 's'
searches = ["bfs","dfs","astar"]

# Class

def MyPriorityQueue(PriorityQueue):
	def get(self):
		return super().get()[-1]

# Functions


# Print the given field
# field - Field to print
def printField(field):
	for i in range(len(field)):
		print(''.join(field[i]))

# Search for character in field
# c		- Character to find
# field	- Search space
def searchFor(c,field):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == c: return (i,j)

# Returns true if pos in field is a boundary
# pos	- Position in field
# field - Search space
def isBound(pos,field):
	return field[pos[0]][pos[1]] == bound

# Returns true if pos in field is a Portal
def isPortal(pos,field):
	return field[pos[0]][pos[1]] in [chr(el+ord('0')) for el in range(10)]

# Returns the position of the other point of the input portal position
def searchPortalPoint(pos,field):
	portalnumber = field[pos[0]][pos[1]]
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == portalnumber:
				if not (i == pos[0] and j == pos[1]):
					return (i,j)

# Returns a list of positions of all portal nodes
def getPortalList(field):
	portallist = []
	for i in range(len(field)):
		for j in range(len(field[i])):
			if isPortal((i,j),field):
				portallist.append((i,j))
	return portallist

# Draws the path in the field
# path	- the path to draw
# field - the field to draw on
def drawPath(path, field):
	tmp = deepcopy(field)
	if path:
		start = path[0]
		goal = path[-1]
		for el in path:
			if el is not start and el is not goal:
				tmp[el[0]][el[1]] = '+'
	return tmp

# This function enables the user to step through iterations and see the current path
def debug(field,path):
	printField(drawPath(path,field))
	print(path)
	input("step")

# Calculate the estimate cost of a given path to the goal position
# When working with portals an optimistic heuristic assumes that the shortest path the minimum of the normal Manhattan distance
# and a shortcut with portals, where the maximum shortcut is given by the
# Manhattan distance to the nearest portal from the current path + Manhattan distance from the goal to the nearest portal to the goal
# regargless of any more portals taken on the path
def heuristicCost(path,goal_pos,field):
	PortalList = getPortalList(field)
	if len(PortalList) > 1:
		nearestPortalHead = PortalList[np.argmin([getManhattanDistance(node,path[-1]) for node in PortalList])]
		nearestPortalGoal = PortalList[np.argmin([getManhattanDistance(node,goal_pos) for node in PortalList])]
		return len(path) + min(getManhattanDistance(path[-1],goal_pos),(getManhattanDistance(path[-1],nearestPortalHead)+getManhattanDistance(nearestPortalGoal,goal_pos)))
	return len(path) + getManhattanDistance(path[-1],goal_pos)

# Returns the 4 orthogonal neighbors in 2D Space of a Node
# If the neighbor is a portal the counterpart portalnode gets added instead
def getNeighbors(node,field):
	w = (node[0] + 1, node[1]  + 0)
	a = (node[0] + 0, node[1]  - 1)
	s = (node[0] - 1, node[1]  + 0)
	d = (node[0] + 0, node[1]  + 1)
	neighborlist = [w,a,s,d]
	for n in neighborlist:
		if isPortal(n,field):
			neighborlist[neighborlist.index(n)] = searchPortalPoint(n,field)
	return neighborlist

# Calculate the Manhattan distance between two points
def getManhattanDistance(pointA, pointB):
	return abs((pointA[0] - pointB[0])) + abs((pointA[1] - pointB[1]))

# Generic Search from a List of Starting Points to a List of Endpoints
# BFS,DFS or A* depends on the given dataStructure
def genericSearch(field, startPosList, endPosList, _dataStructure=Queue, _heuristic=False, _debug=False):
	visited = []
	frontier = _dataStructure()
	max_frontier_len = 0

	for startPos in startPosList:
		if _heuristic:
			frontier.put((0,[startPos]))
		else:
			frontier.put([startPos])

	while not frontier.empty():
		if frontier.qsize() > max_frontier_len: max_frontier_len = frontier.qsize()
		path = []
		if _heuristic:
			path = frontier.get()[-1]
		else:
			path = frontier.get()

		head = path[-1]

		if head not in visited:
			visited.append(head)
			if head in endPosList:
				return path,len(visited),max_frontier_len
			for neighbor in getNeighbors(head,field):
				if not isBound(neighbor, field):
					new_path = [n for n in path]
					new_path.append(neighbor)
					if _debug:
						debug(field,new_path)
					if _heuristic:
						frontier.put((heuristicCost(new_path,endPosList[0],field),new_path))
					else:
						frontier.put(new_path)
	return 0,len(visited),max_frontier_len

def printSearchInfo(time, maxFrontier,visitCount):
	print("Time: ", time)
	print("Biggest frontier had ", maxFrontier, " Elements")
	print("The search \"visited\" ", visitCount, " Points")

def askForAnswer(cli_arg, firstQuestion, followingQuestion, answers=[]):
	if cli_arg > 1 and len(sys.argv) > cli_arg: answer = sys.argv[cli_arg]
	else: answer = input(firstQuestion + " (" + "|".join(answers) + ") ")
	# Ask until valid answer is given
	while(answer not in answers):
		answer = input(followingQuestion + " (" + "|".join(answers) + ") ")
	return answer

def main():
	# Load the field
	if len(sys.argv) >= 2: field = [list(line.rstrip('\n')) for line in open(sys.argv[1])]
	else:
		print("There has to be at least one command line argument. It should be our enviroment.")
		return
	print(sys.argv[1])

	# Print the field
	print("Enviroment")
	printField(field)

	# Some Info
	print("Character", start, "found at", searchFor(start,field))
	print("Character", goal , "found at", searchFor(goal,field), "\n")

	# Ask for debug output
	if "y" == askForAnswer(3, "Do you want to debug and step through the pathfinding?", "I didn't understand you.", ["y","n"]):
		debugFlag = True
	else: debugFlag = False

	howToSearch = askForAnswer(2, "Which search should I use?", "I didn't understand you.", searches)

	# Run the search
	tstart = timer()
	if  (howToSearch == "dfs"  ): search_result = genericSearch(field,[searchFor(start,field)],[searchFor(goal,field)],_dataStructure=LifoQueue,_heuristic=False,_debug=debugFlag)
	elif  (howToSearch == "bfs"  ): search_result = genericSearch(field,[searchFor(start,field)],[searchFor(goal,field)],_dataStructure=Queue,_heuristic=False,_debug=debugFlag)
	elif  (howToSearch == "astar"  ): search_result = genericSearch(field,[searchFor(start,field)],[searchFor(goal,field)],_dataStructure=PriorityQueue,_heuristic=True,_debug=debugFlag)
	tend = timer()
	elapsed_time = tend - tstart
	search_path = search_result[0]

	# Print the path
	print("\nSearch has finished")
	if(search_path == 0):
		print("No Path found")
	else:
		print(howToSearch.upper(), "Path:\n", search_path, "\n")
		print("Visualized Path:\n")
		printField(drawPath(search_path,field)) # Draw the path to the field
		#printSearchInfo()
	if "y" == askForAnswer(4, "Some statistics?", "I didn't understand you.", ["y","n"]):
		printSearchInfo(elapsed_time, search_result[2] ,search_result[1])

# Run the main method
if __name__ == "__main__":
    main()