#To import all the scripts, use a wildcard
import os
import glob
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")]
