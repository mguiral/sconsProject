from _external import *
from boost import *

boost_thread = LibWithHeaderChecker( 'boost_thread', 'boost/thread.hpp', 'c++',
                                     name='boost_thread', dependencies=[boost] )

