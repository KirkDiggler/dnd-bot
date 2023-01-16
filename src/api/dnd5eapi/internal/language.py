from src.api.lib import language

class Language:
    def __init__(self, *initial_data):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

    def to_model(self):
        return language.Language(
            key=self.index,
            name=self.name,
            typical_speakers=self.typical_speakers,
            script=self.script
        )