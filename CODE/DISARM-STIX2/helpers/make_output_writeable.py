import os
import stat

for root, dirs, files in os.walk("output"):
    for f in files:
        filepath = os.path.join(root, f)
        os.chmod(filepath, stat.S_IWRITE)
