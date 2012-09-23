from SCons.Script.SConscript import SConsEnvironment

import os
import sys
import subprocess

windows = os.name.lower() == "nt" and sys.platform.lower().startswith("win")

ld_library_path = 'LD_LIBRARY_PATH' if not windows else 'PATH'
mpsep = ':' if not windows else ';'


#
# Function taken from scons Wiki
#
def builder_unit_test(target, source, env):
	app = str(source[0].abspath)
	procenv = env['ENV']
	ldPaths = []
	for p in env['LIBPATH']:
		pp = p.replace('#', env['TOPDIR']+'/')
		pEval = env.subst(pp)
		if pEval:
			ldPaths.append(pEval)
	procenv[ld_library_path] = mpsep.join(ldPaths)
	if subprocess.call(app, env=procenv) == 0:
		open(str(target[0]), 'w').write("PASSED\n")
	else:
		return 1


def UnitTest(env, source, **kwargs):
	target = []
	if 'target' not in kwargs:
		raise RuntimeError( 'No target for unittest.' )
	
	if isinstance( kwargs['target'], list ):
		target = kwargs['target']
	elif isinstance( kwargs['target'], str ):
		target = [kwargs['target']]
	target.insert( 0, 'unittest' )
	
	test = env.Program( target='-'.join( target ), source=source )
	
	unittest = env.Test( test[0].abspath+'.unittest_passed', test )
	
	for i in range(1,len(target)+1):
		#print '-'.join(target[0:i])
		env.Alias('-'.join(target[0:i]), unittest)
	return test


def generate(env):
	"""
	Add builders and construction variables for unittest.
	"""
	import SCons.Builder
	unitTestBuilder = SCons.Builder.Builder(action = builder_unit_test)
	env.Append(BUILDERS = {'Test' : unitTestBuilder })

	SConsEnvironment.UnitTest = UnitTest


def exists(env):
	return True


