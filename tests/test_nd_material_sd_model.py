import os
import sys
TEST_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
INTERPRETER_PATH = TEST_DIR + "../SRC/interpreter/"
sys.path.append(INTERPRETER_PATH)

import opensees as opy
opy.wipe()
opy.model('basic', '-ndm', 2, '-ndf', 2)
opy.node(1, 0.0, 0.0)
opy.node(2, 1.0, 0.0)
opy.node(3, 1.0, 1.0)
opy.node(4, 0.0, 1.0)
for i in range(4):
    opy.fix(1 + 1 * i, 1, 1)
opy.nDMaterial('stressDensity', 1, 1.8, 0.7, 250.0, 0.6, 0.2, 0.592, 0.021, 291.0, 55.0, 98.0, 13.0, 4.0, 0.22, 0.0, 0.0055, 0.607, 98.1)
opy.nDMaterial('InitStressNDMaterial', 2, 1, -100.0, 2)
opy.element('SSPquad', 1, 1, 2, 3, 4, 2, 'PlaneStrain', 1.0, 0.0, 0.0)
opy.constraints('Penalty', 1e+15, 1e+15)
opy.algorithm('Linear', False, False, False)
opy.numberer('RCM')
opy.system('FullGeneral')
opy.integrator('LoadControl', 0.1, 1)
opy.analysis('Static')
opy.timeSeries('Path', 1, '-values', 0, 0, 0, 0.1, '-time', 0.0, 1.0, 2.0, 1002.0, '-factor', 1.0)
opy.pattern('Plain', 1, 1)
opy.sp(3, 1, 1)
opy.sp(4, 1, 1)
opy.analyze(1)
opy.setParameter('-val', 1, '-ele', 1, 'materialState')
# opy.analyze(1)
