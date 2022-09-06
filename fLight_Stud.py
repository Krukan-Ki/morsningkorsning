# Studentversion av filen.
# Givet Ã¤r ett skal till klassen Light
# och kod (funktionen demo_light) som testar klassen Light.
# Fyll i det som saknas i klassen Light sÃ¥ att utskriften nedan fÃ¥s.

class Light:
    """Representerar ett trafikljus"""
    """Se specifikation av klassen pÃ¥ kursens webbbsida"""
    # HÃ¤r saknas kod...
    # ...
    # ...
    # ...
    
    def __init__(self, period, green_time):
        self.period = period
        self.green_time = green_time
        self.color = "(G)"
        self.clock = 1
    
    def __str__(self):
        return f'{self.color}'
    
    def step(self):
        if self.clock < self.green_time:
            self.clock += 1
        elif self.clock >= self.green_time and self.clock < self.period:
            self.clock += 1
            self.color = "(R)"
        else:
            self.clock = 1
            self.color = "(G)"
        
    
    def is_green(self):
        if self.color == "(G)":
            return True
        else:
            return False

def demo_light():
    """FÃ¶r demonstration av klassen Light"""
    a_light = Light(7, 3) # Skapa ett trafikljus, period 7, green time 3
    # Simulera 15 tidssteg
    for t in range(15):
        print(t+1, a_light, a_light.is_green())
        a_light.step() # NÃ¤sta steg fÃ¶r trafikljuset

def main():
    print('\nLight demonstration')
    demo_light()

if __name__ == '__main__':  # If this file is the main program, you are running:
    main()                  # Call the main function above
    
# When the Python interpreter reads a python file, it defines
# the special variable __name__
# If you are running your module as the main program,
# the interpreter will assign the hard-coded string "__main__" to the __name__ variable
# If this python file is demo_light() imported by another program, and they run that program, the
# main function is not called

""" NÃ¤r man kÃ¶r denna kod skall fÃ¶ljande hÃ¤nda:
Light demonstration
1 (G) True
2 (G) True
3 (G) True
4 (R) False
5 (R) False
6 (R) False
7 (R) False
8 (G) True
9 (G) True
10 (G) True
11 (R) False
12 (R) False
13 (R) False
14 (R) False
15 (G) True
"""