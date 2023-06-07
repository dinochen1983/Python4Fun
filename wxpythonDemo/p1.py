import openseespy.opensees as ops

# wipe model
ops.wipe()

# create model
ops.model('basic', '-ndm', 2, '-ndf', 3)

# print model
ops.printModel()