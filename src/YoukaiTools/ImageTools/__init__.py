from . import PowerTools
from . import Create
from . import Comparison
from . import Metric
from . import SubImage
from . import FileHandlers
from . import CombineFunctions
from . import settings
from . import ColorModels
from . import LineFont
from YoukaiTools import LineLoader

#an image is in the form (width, height, channels, (c1, c2, ..., cn), (...), ... )

def loadSettings(f):
    l = LineLoader.loadLines(f)
    for line in l:
        a = line.split("=")
        if a[0].strip().lower() == "verbosity":
            settings.verbosity = int(a[1].strip())

