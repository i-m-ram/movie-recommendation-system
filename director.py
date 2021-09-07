import numpy as np
def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan