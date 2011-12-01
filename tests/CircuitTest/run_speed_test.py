import os
import sys

start_name = sys.argv[1]

print("Python:")
os.system("python -m cProfile -o "+start_name+"_python.profile test_nn_speed.py")
print("PyPy:")
os.system("pypy -m cProfile -o "+start_name+"_pypy.profile test_nn_speed.py")
