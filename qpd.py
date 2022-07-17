from qiskit import *
from qiskit.compiler import transpile
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit.quantum_info import process_fidelity
from qiskit.quantum_info import Statevector
import cmath
import numpy as np
import warnings
import sys,os,argparse,subprocess,shutil,time,glob,fnmatch
from math import sqrt

 #!/usr/bin/env python -W ignore::DeprecationWarning

        ############################################
        ##                                        ##
        ##     ####      ########   #######       ##
        ##   ##    ##    ##    ##   ##     ##     ##
        ##   ##    ##    #######    ##      ##    ##
        ##     #####     ##         ##     ##     ##
        ##         ###   ##         #######       ##
        ############################################            

##Author: Haddy Alchaer & Lawal Ogunfowora
##This program illustrates the Quantum Advantage of resolving the Nash Equilibirium in non-zero sum games specifically in the case of Prisoners' Dilemma in Game Theory.

warnings.filterwarnings("ignore", category=DeprecationWarning) 

def main(argv):

    parser = argparse.ArgumentParser(description='Executes Quantum version of Prisoners\' Dilemma;')
    
    #required (positional) arguments  
    parser.add_argument('strategies', help = 'A quoted list of the players\' strategies in the right order (options are C -- to cooperate, D -- to defect & Q -- to deploy a quantum strategy).')

    #optional arguments
    parser.add_argument('-e',dest='entanglement', default=100,
                         help = 'The entanglement parameter for the degree of quantum effect in the game; ranges between 0 (no entanglement) and 100 (maximum entanglement), default is maximum entanglement')
    parser.add_argument('-r',dest='rounds', default=1,
                         help = 'The number of rounds the players\' wish to play')

    # parse strategies into QPD function                                                                                                                                                                                                    
    args    = parser.parse_args()
    stratA = args.strategies.split(' ')[0].upper()
    stratB = args.strategies.split(' ')[1].upper()
    pie = 0.5*np.pi
    gamma=(float(args.entanglement)/100)*pie
    round = int(args.rounds)
    scoreA, scoreB = 0, 0 

    while round > 0:
        x, y = QPD(stratA, stratB, gamma)
        scoreA+=x
        scoreB+=y
        round-=1
        if round > 0: stratA, stratB = input('What\'s your next strategy (quoted) in the same order?').split(' ')
        stratA, stratB = str(stratA).upper(), str(stratB).upper()

    print(f"Player A's total reward is: " + str(scoreA))
    print(f"Player B's total reward is: " + str(scoreB))

    return;

# QPD Function runs the players strategies through a quantum simulator 
def QPD(stratA, stratB, gamma):

    qc = QuantumCircuit()                     #creating a quantum circuit for the set-up
    qr = QuantumRegister(2,'player')          # registering two qubits, one for each player
    qc.add_register( qr )                     #adding qubits to the circuit
    qc.draw()

    # creating the unitary J and J dagger operators #
    m1 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    m1 = np.multiply(m1, np.cos(gamma * 0.5))
    m2 = [[0, 0, 0, 1], [0, 0, -1, 0], [0, -1, 0, 0], [1, 0, 0, 0]]
    m2 = np.multiply(m2, 1j * np.sin(gamma * 0.5))
    m3 = m1 + m2
    m4 = m1 - m2

    J = Operator(m3)
    Jdag = Operator(m4)

    #strategy matrices
    cooperate = [[1,0],[0,1]]
    defect = [[0,1],[-1,0]]
    quantum = [[1j,0],[0,-1j]]
    # quantum = [[sqrt(2)*0.5*1j,sqrt(2)*0.5],[-1*sqrt(2)*0.5,sqrt(2)*0.5*-1j]]
    # quantum = [[sqrt(2)*0.5 + sqrt(2)*0.5*1j, 0],[0, sqrt(2)*0.5 - sqrt(2)*0.5*1j]]
    # quantum = [[1j/(sqrt(2)), -1/(sqrt(2))],[1/(sqrt(2)), -1j/(sqrt(2))]]

    #interphasing matrices with player's strategies
    if stratA == "C" :
      mA = cooperate
    elif stratA == "D" :
      mA = defect
    elif stratA == "Q" :
      mA = quantum
    else :
      print("error, not a strategy")

    if stratB == "C" :
      mB = cooperate
    elif stratB == "D" :
      mB = defect
    elif stratB == "Q" :
      mB = quantum
    else :
      print("error, not a strategy")

    #tensor product of the strategies for generating new state vector
    mAB = np.tensordot(mA, mB, axes=0)
    mAB = mAB.transpose((0, 2, 1, 3)).reshape(4, 4)
    UAB = Operator(mAB)

    # applying all the parameters to the circuit
    qc.append(J, [0, 1])
    qc.append(UAB, [0, 1])
    qc.append(Jdag, [0, 1])
    qc.draw()

    #simulating the players' playoff
    sv_sim = Aer.get_backend('aer_simulator')
    qc.save_statevector()
    qobj = assemble(qc)
    job = sv_sim.run(qobj)
    ket = job.result().get_statevector()
    
    #classical rewards
    coeffsA = [3, 0, 5, 1]  ##CC, CD, DC, DD
    coeffsB = [3, 5, 0, 1]  ##CC, DC, CD, DD
    scoreA = 0
    scoreB = 0

    #Quantum Advantage
    for x in range(len(ket)) :
      amplitude = ket[x]
      scoreA += round(abs(amplitude)**2 * coeffsA[x], 2) 
      scoreB += round(abs(amplitude)**2 * coeffsB[x], 2) 

    print(f"Player A played {stratA}: " + str(scoreA))
    print(f"Player B played {stratB}: " + str(scoreB))

    return scoreA, scoreB;

if __name__ == "__main__":
    main(sys.argv[1:])
