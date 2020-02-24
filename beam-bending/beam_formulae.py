## beam formulae
import numpy as np

class beam_formulae:

    def circ_area(diameter):
        A = np.pi*(diameter/2)**2
        return A

    def square_area(length,width):
        A = length*width
        return A

    def P_result(distributed_load,x):
        P_res = distributed_load*x
        return P_res

    def moment(F,x_arm):
        M = F*x_arm
        return M
    
    def stress(moment, r):
        sigma = (moment * r)/(1/4*np.pi*r**4)
        return sigma