
class GameContext: #Central of dependencies, removes almost all the existing parameter work
    def __init__(self):
        self.clock = None
        self.audio = None
        self.actors = None
        self.screens = None
        self.current_screen = None
        self.player = None
        self.questions = None
        self.transitions = None
        self.sounds = None

    def inject_dependencies(self, clock, actors, audio, questions, transitions, sounds):
        self.clock = clock
        self.actors = actors
        self.audio = audio
        self.player = actors.swimmer
        self.questions = questions
        self.transitions = transitions
        self.sounds = sounds