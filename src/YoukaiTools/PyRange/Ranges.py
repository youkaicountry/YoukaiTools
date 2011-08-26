#unsimplified range conversion equation:
#(((val - abs(min_s)) / (max_s - min_s)) * (max_t - min_t)) + min_t
def rangeToRange(value, min_source, max_source, min_target, max_target):
    return (normalize(value, min_source, max_source) * (max_target - min_target)) + min_target

def normalize(value, min_source, max_source):
    return ((value - min_source) / (max_source - min_source))
    
#finds min and max of a given list, and returns range converted values
def histogramConvert(values, min_target, max_target):
    return

