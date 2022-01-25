# HELPER FUNCTIONS
def most_common(lst):
    return max(set(lst), key=lst.count)

def flatten_list(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten_list(el))
        else:
            result.append(el)
    return result