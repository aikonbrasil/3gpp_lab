import os
for f in os.listdir("."):
    r = f.replace(" ","_")
    #if( r != f):
    #    os.rename(f,r)
    x = r.replace("(","")
    #if (x != f):
    #    os.rename(f,x)
    y = x.replace(")","")
    if (x != f):
        os.rename(f,y)
