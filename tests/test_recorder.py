import os
import sys
TEST_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
INTERPRETER_PATH = TEST_DIR + "../SRC/interpreter/"
sys.path.append(INTERPRETER_PATH)

import opensees as opy


def test_recorder_time_step_is_stable():
    opy.model('basic', '-ndm', 2, '-ndf', 2)
    opy.loadConst('-time', 1e+13)
    opy.node(1, 0.0, 0.0)
    opy.node(2, 0.5, 0.0)
    opy.node(3, 0.0, -0.5)
    opy.node(4, 0.5, -0.5)
    opy.equalDOF(3, 4, 1, 2)
    opy.node(5, 0.0, -1.0)
    opy.node(6, 0.5, -1.0)
    opy.equalDOF(5, 6, 1, 2)
    opy.node(7, 0.0, -1.5)
    opy.node(8, 0.5, -1.5)
    opy.equalDOF(7, 8, 1, 2)
    opy.node(9, 0.0, -2.0)
    opy.node(10, 0.5, -2.0)
    opy.equalDOF(9, 10, 1, 2)
    opy.node(11, 0.0, -2.5)
    opy.node(12, 0.5, -2.5)
    opy.equalDOF(11, 12, 1, 2)
    opy.node(13, 0.0, -3.0)
    opy.node(14, 0.5, -3.0)
    opy.equalDOF(13, 14, 1, 2)
    opy.fix(13, 0, 1)
    opy.fix(14, 0, 1)
    opy.node(15, 0.0, -3.0)
    opy.node(16, 0.0, -3.0)
    opy.fix(15, 1, 1)
    opy.fix(16, 0, 1)
    opy.equalDOF(13, 14, 1)
    opy.equalDOF(13, 16, 1)
    opy.nDMaterial('ElasticIsotropic', 1, 212500.0, 0.0, 1.7)
    opy.element('SSPquad', 1, 3, 4, 2, 1, 1, 'PlaneStrain', 1.0, 0.0, 16.677)
    opy.element('SSPquad', 2, 5, 6, 4, 3, 1, 'PlaneStrain', 1.0, 0.0, 16.677)
    opy.element('SSPquad', 3, 7, 8, 6, 5, 1, 'PlaneStrain', 1.0, 0.0, 16.677)
    opy.element('SSPquad', 4, 9, 10, 8, 7, 1, 'PlaneStrain', 1.0, 0.0, 16.677)
    opy.element('SSPquad', 5, 11, 12, 10, 9, 1, 'PlaneStrain', 1.0, 0.0, 16.677)
    opy.element('SSPquad', 6, 13, 14, 12, 11, 1, 'PlaneStrain', 1.0, 0.0, 16.677)
    opy.uniaxialMaterial('Viscous', 2, 212.5, 1.0)
    opy.element('zeroLength', 7, 15, 16, '-mat', 2, '-dir', 1)
    opy.constraints('Transformation')
    opy.test('NormDispIncr', 0.0001, 30, 0, 2)
    opy.algorithm('Newton', False, False, False)
    opy.numberer('RCM')
    opy.system('ProfileSPD')
    opy.integrator('Newmark', 0.5, 0.25)
    opy.analysis('Transient')
    opy.analyze(40, 1.0)
    opy.analyze(50, 0.5)
    opy.setTime(1.0e3)
    opy.wipeAnalysis()
    opy.recorder('Node', '-file', 'time_0_01.txt', '-precision', 16, '-dT', 0.01, '-rTolDt', 0.00001, '-time', '-node', 1, '-dof', 1, 'accel')
    opy.recorder('Element', '-file', 'etime_0_01.txt', '-precision', 16, '-dT', 0.01, '-rTolDt', 0.00001, '-time',
                 '-ele', 1, 2, 'stress')
    opy.recorder('EnvelopeNode', '-file', 'entime_0_01.txt', '-precision', 16, '-dT', 0.01, '-time', '-node', 1, '-dof', 1, 'accel')
    # opy.recorder('Drift', '-file', 'dtime_0_01.txt', '-precision', 16, '-dT', 0.01, '-time',
    #              '-iNode', 1, '-jNode', 2, '-dof', 1, '-perpDirn', 2)
    opy.timeSeries('Path', 1, '-dt', 0.01, '-values', -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -7.51325e-05)
    opy.pattern('Plain', 1, 1)
    opy.load(13, 1.0, 0.0)
    opy.algorithm('Newton', False, False, False)
    opy.system('SparseGeneral')
    opy.numberer('RCM')
    opy.constraints('Transformation')
    opy.integrator('Newmark', 0.5, 0.25)
    opy.rayleigh(0.17952, 0.000909457, 0.0, 0.0)
    opy.analysis('Transient')
    opy.test('EnergyIncr', 1e-07, 10, 0, 2)
    opy.record()
    opy.analyze(1, 0.001)
    for i in range(1100):
        print(i)
        opy.analyze(1, 0.001)
        cur_time = opy.getTime()
    opy.wipe()

    a = open('time_0_01.txt').read().splitlines()
    for i in range(len(a) - 1):
        dt = float(a[i + 1].split()[0]) - float(a[i].split()[0])
        assert abs(dt - 0.01) < 0.0001, (i, dt)


def test_recorder_time_step_can_handle_fp_precision():
    import tempfile
    opy.model('basic', '-ndm', 2, '-ndf', 3)
    opy.node(1, 0.0, 0.0)
    opy.node(2, 0.0, 5.0)
    opy.fix(2, 0, 1, 0)
    opy.fix(1, 1, 1, 1)
    opy.equalDOF(2, 1, 2)
    opy.mass(2, 1.0, 0.0, 0.0)
    opy.geomTransf('Linear', 1, '-jntOffset')
    opy.element('elasticBeamColumn', 1, 1, 2, 1.0, 1e+06, 0.00164493, 1)
    opy.timeSeries('Path', 1, '-dt', 0.1, '-values', 0.0, -0.001, 0.001, -0.015, 0.033, 0.105, 0.18)
    opy.pattern('UniformExcitation', 1, 1, '-accel', 1)
    opy.rayleigh(0.0, 0.0159155, 0.0, 0.0)
    opy.wipeAnalysis()
    opy.algorithm('Newton')
    opy.system('SparseSYM')
    opy.numberer('RCM')
    opy.constraints('Transformation')
    opy.integrator('Newmark', 0.5, 0.25)
    opy.analysis('Transient')
    opy.test('EnergyIncr', 1e-07, 10, 0, 2)
    node_rec_ffp = tempfile.NamedTemporaryFile(delete=False).name
    ele_rec_ffp = tempfile.NamedTemporaryFile(delete=False).name
    rdt = 0.01
    adt = 0.001
    opy.recorder('Node', '-file', node_rec_ffp, '-precision', 16, '-dT', rdt, '-rTolDt', 0.00001, '-time', '-node', 1, '-dof', 1, 'accel')
    opy.recorder('Element', '-file', ele_rec_ffp, '-precision', 16, '-dT', rdt, '-rTolDt', 0.00001, '-time', '-ele', 1, 'force')

    opy.record()
    for i in range(1100):
        opy.analyze(1, adt)
        opy.getTime()
    opy.wipe()

    a = open(node_rec_ffp).read().splitlines()
    for i in range(len(a) - 1):
        dt = float(a[i + 1].split()[0]) - float(a[i].split()[0])
        assert abs(dt - 0.01) < adt * 0.1, (i, dt)
    a = open(ele_rec_ffp).read().splitlines()
    for i in range(len(a) - 1):
        dt = float(a[i + 1].split()[0]) - float(a[i].split()[0])
        assert abs(dt - 0.01) < adt * 0.1, (i, dt)


if __name__ == '__main__':
    test_recorder_time_step_can_handle_fp_precision()
