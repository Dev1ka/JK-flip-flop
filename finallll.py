class LogicGate:
    def __init__(self, n):
        self.name = n
        self.output = 0
        self.next_output = 0

    def get_output(self):
        return self.output

    def update(self):
        self.next_output = self.perform_gate_logic()

    def finalise(self):
        self.output = self.next_output


class BinaryGate(LogicGate):
    def __init__(self, n):
        super(BinaryGate, self).__init__(n)
        self.pin_a = None
        self.pin_b = None

    def get_pin_a(self):
        if self.pin_a:
            return self.pin_a.get_from().get_output()
        return 0

    def get_pin_b(self):
        if self.pin_b:
            return self.pin_b.get_from().get_output()
        return 0

    def set_next_pin(self, source):
        if self.pin_a is None:
            self.pin_a = source
        else:
            self.pin_b = source


class NandGate(BinaryGate):
    def __init__(self, n):
        BinaryGate.__init__(self, n)

    def perform_gate_logic(self):
        a = self.get_pin_a()
        b = self.get_pin_b()
        if a == 1 and b == 1:
            return 0
        else:
            return 1


class Switch(LogicGate):
    def set_val(self, val):
        self.output = val

    def perform_gate_logic(self):
        return self.output


class Connector:
    def __init__(self, fgate, tgate):
        self.fromgate = fgate
        tgate.set_next_pin(self)

    def get_from(self):
        return self.fromgate


class JkFlipFlop:
    def __init__(self):
        self.j = Switch('J')
        self.k = Switch('K')
        self.g1 = NandGate('G1')
        self.g2 = NandGate('G2')
        self.g3 = NandGate('G3')   # Q
        self.g4 = NandGate('G4')   # not Q

        Connector(self.j, self.g1)
        Connector(self.g4, self.g1)

        Connector(self.k, self.g2)
        Connector(self.g3, self.g2)

        Connector(self.g1, self.g3)
        Connector(self.g4, self.g3)
        Connector(self.g2, self.g4)
        Connector(self.g3, self.g4)

        self.g3.output = 0
        self.g4.output = 1

    def perform_logic(self, j_in, k_in):
        self.j.set_val(j_in)
        self.k.set_val(k_in)

        # Handle JK behaviour directly so state updates reliably
        current_q = self.g3.output

        if j_in == 0 and k_in == 0:       # hold
            next_q = current_q
        elif j_in == 0 and k_in == 1:     # reset
            next_q = 0
        elif j_in == 1 and k_in == 0:     # set
            next_q = 1
        else:                             # toggle
            next_q = 1 - current_q

        self.g3.output = next_q
        self.g4.output = 1 - next_q

        return f'Q:{self.g3.output} Q_bar:{self.g4.output}'

    def get_q(self):
        return self.g3.output


# Main Loop
jk = JkFlipFlop()
button_press = -1
previous_button = -1
j = 1
k = 0

while True:
    activate = False
    pprevious_button = previous_button
    previous_button = button_press
    button_press = int(input("Button Pressed? "))

    j_new = int(input('Enter j val: '))
    k_new = int(input('Enter k val: '))

    if button_press not in (0, 1):
        print("Please enter 0 or 1.")
        continue

    # Output logic
    if button_press == 1 and previous_button == 1 and pprevious_button == 0:
        print("Pulse sent")
        activate = True
    else:
        print("No pulse")

    # Clock update:
    # store current button value into the flip-flop for next tick
    if activate:
        print(jk.perform_logic(j_new, k_new))
        j = j_new
        k = k_new
    else:
        print(jk.perform_logic(j, k))
    print()
