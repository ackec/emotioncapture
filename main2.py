import openpifpaf_mouse
import openpifpaf
from  openpifpaf.train import main as main_3
import os
import sys
assert "mouse" not in openpifpaf.DATAMODULES
openpifpaf_mouse.register()
assert "mouse" in openpifpaf.DATAMODULES
# args= ["--dataset", "mouse", "--basenet", "shufflenetv2k16"]
main_3()

# sys.argv = [main_3, "--dataset", "mouse", "--basenet=shufflenetv2k16"]
# exec(openpifpaf.train)

os.system("python openpifpaf.train --dataset mouse --basenet=shufflenetv2k16")