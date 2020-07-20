from queue import Queue
import random as ran

actions = ['Up', 'Down', 'Left', 'Right']
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class Puzzle:
    heuristic, evaluation = None, None
    needs_hueristic = False
    num_of_instances = 0
    def __init__(self, state, parent, action, path_cost, needs_hueristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent: self.path_cost = parent.path_cost + path_cost
        else: self.path_cost = path_cost
        if needs_hueristic:
            self.needs_hueristic=True
            self.generate_heuristic()
            self.evaluation=self.heuristic+self.path_cost
        Puzzle.num_of_instances+=1

    def generate_heuristic(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - goal_state.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j

    def goal_test(self):
        if self.state == goal_state: return True
        else: return False

    @staticmethod
    def find_legal_actions(i,j):
        legal_action = actions.copy()
        if i == 0: legal_action.remove(actions[0])
        elif i == 2: legal_action.remove(actions[1])
        if j == 0: legal_action.remove(actions[2])
        elif j == 2: legal_action.remove(actions[3])
        return legal_action

    def generate_child(self):
        children=[]
        x = self.state.index(0)
        i, j = int(x / 3), int(x % 3)
        legal_actions=self.find_legal_actions(i,j)
        for action in legal_actions:
            new_state = self.state.copy()
            if action == actions[0]:
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == actions[1]:
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == actions[2]:
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == actions[3]:
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state, self, action, 1, self.needs_hueristic))
        return children

    def find_solution(self):
        solution, states = [], []
        solution.append(self.action)
        path = self
        states.append(goal_state)
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
            states.append(path.state)
        solution.reverse()
        states.reverse()
        return solution, states

def breadth_first_search(initial_state):
    start_node = Puzzle(initial_state, None, None, 0)
    if start_node.goal_test():
        return start_node.find_solution()
    q = Queue()
    q.put(start_node)
    explored=[]
    while not(q.empty()):
        node=q.get()
        explored.append(node.state)
        children = node.generate_child()
        for child in children:
            print("#",child.state)
            if child.state not in explored:
                if child.goal_test():
                    solu, states = child.find_solution()
                    show_steps(states)
                    return solu
                q.put(child)
    return None

def best_first_search(initial_state):
    node = BFS_search(Puzzle(initial_state, None, None, 0, True))
    solu, states = node[0].find_solution()
    show_steps(states)
    return solu

def BFS_search(node):
    successors=[]
    if node.goal_test():
        return node,None
    children=node.generate_child()
    if not len(children):
        return None, maxsize
    count=-1
    for child in children:
        print("#",child.state)
        count+=1
        successors.append((child.evaluation,count,child))
    while len(successors):
        successors.sort()
        best_node=successors[0][2]
        alternative=successors[1][0]
        result, best_node.evaluation = BFS_search(best_node)
        successors[0]=(best_node.evaluation, successors[0][1], best_node)
        if result!=None: break
    return result, None

def show_steps(states):
    for i in states:
        print("---------")
        print( str(i[0:3])+"\n"+str(i[3:6])+"\n"+str(i[6:9]) )

#state = ran.sample(range(9), 9)
state = [2, 3, 6, 1, 5, 0, 4, 7, 8]
print("\n* Breadth First Search *\n")
breadth_first_search(state)
print("\n* Best First Search *\n")
best_first_search(state)
