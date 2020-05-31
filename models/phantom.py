import random

class PhantomMemory():

    def __init__(self):
        self.__mem = {}
        self.__excitability = 0.0
        self.__max_excitability = 10.0

    def reset_excitability(self):
        self.__excitability = 0.0

    def recall(self,state,status,action,new_status,reward):
        # recall excitability
        #memkey = state
        #if memkey in self.__mem:
        #    phantoms = self.__mem[memkey]
        #    phantoms.sort(key=lambda x:-x[1])
        #    phantom_status = phantoms[0][0]
        #    self.__excitability = phantoms[0][1]

        # trigger phantom memory or not
        has_phantom = False        
        if random.random() < self.__excitability/self.__max_excitability:
            has_phantom = True

        # udpate excitability
        self.__excitability += reward
        if self.__excitability > 10.0:
            self.__excitability = 10.0
        elif self.__excitability < 0.0:
            self.__excitability = 0.0

        # return phantom or not
        memkey = state #tuple(state.flatten(),Status.status_to_int(status))
        phantom_status = status
        if has_phantom and memkey in self.__mem:
            phantoms = self.__mem[memkey]
            phantoms.sort(key=lambda x:-x[1])
            phantom_status = phantoms[0][0]
            phantom_status = has_phantom and new_status or status

        # update phantom memory
        if not memkey in self.__mem:
            self.__mem[memkey] = [(new_status,self.__excitability)]
        else:
            memdict = dict(self.__mem[memkey])
            # only change if current excitability is bigger
            if not new_status in memdict or self.__excitability > memdict[new_status]:
                memdict[new_status] = self.__excitability
            #memdict[new_status] = self.__excitability
            self.__mem[memkey] = list(memdict.items())

        return phantom_status

    def __str__(self):
        return str(self.__mem)
