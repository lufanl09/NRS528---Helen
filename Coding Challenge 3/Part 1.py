# 1. Simple Directory Tree

#start by importing os package
import os

#create directory tree
os.mkdir("C:\draft_code")
os.mkdir("C:\draft_code\pending")
os.mkdir("C:\draft_code\complete")

os.mkdir("C:\includes")

os.mkdir("C:\layouts")
os.mkdir("C:\layouts\default")
os.mkdir("C:\layouts\post")
os.mkdir("C:\layouts\post\posted")

os.mkdir("C:\site")

#delete directory tree
os.removedirs("C:\draft_code\pending")
os.removedirs("C:\draft_code\complete")

os.removedirs("C:\includes")

os.removedirs("C:\layouts\default")
os.removedirs("C:\layouts\post\posted")

os.removedirs("C:\site")
