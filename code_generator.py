

class code_generator:
    def __int__(self):
        self.semantic_routines = {
            'pid' : pid,
            'pnum' : pnum,
            'label' : label
        }



    def call_routine(self, routine, token):
        self.semantic_routines[routine]()

    def pid(self):
        pass