import sys
sys.path.append('C:\\Users\\Jubabouche\\Documents\\pro\\Dsync\\pyModel\\lib')


import os 

def get_path(filename):
    script_dir = os.path.dirname(__file__)
    rel_path = f"res/analytics/{filename}"
    return os.path.join(script_dir, rel_path)
    
