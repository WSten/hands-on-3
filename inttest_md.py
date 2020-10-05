import md
import os
import sys
md.run_md()

if os.path.exists('cu.traj'):
    print("OK")
else:
    print("FAILED")
    sys.exit()
