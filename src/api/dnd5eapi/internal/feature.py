class Feature:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
