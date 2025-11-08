import pygame
import pyperclip
import sys

pygame.init()
pygame.display.set_caption("Calcolatrice Pygame")

# Dimensioni finestra
WIDTH, HEIGHT = 400, 550
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
#nonono
# Colori
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# Font
FONT_INPUT = pygame.font.SysFont("Arial", 40)
FONT_BUTTON = pygame.font.SysFont("Arial", 30)
FONT_SMALL = pygame.font.SysFont("Arial", 20)

# Pulsante definizione
class Button:
    def __init__(self, text, x, y, w, h, color, text_color=BLACK):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        text_surface = FONT_BUTTON.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Calcolatrice
class Calculator:
    def __init__(self):
        self.expression = ""
        self.result = ""
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        btn_w = 80
        btn_h = 60
        margin_x = 20
        margin_y = 150
        spacing = 10
        labels = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '.', '+'],
            ['=', 'Copy', 'Paste']
        ]

        for row_idx, row in enumerate(labels):
            for col_idx, label in enumerate(row):
                x = margin_x + (btn_w + spacing) * col_idx
                y = margin_y + (btn_h + spacing) * row_idx
                color = LIGHT_GRAY
                if label == 'C':
                    color = (255, 102, 102)  # rosso chiaro
                elif label == '=':
                    color = ORANGE
                elif label in ('Copy', 'Paste'):
                    color = GRAY
                    text_color = WHITE
                else:
                    text_color = BLACK
                btn = Button(
                    label, x, y, btn_w, btn_h, color, text_color if 'text_color'
 in locals() else BLACK
                )
                self.buttons.append(btn)

    def draw(self):
        SCREEN.fill(WHITE)

        # Disegna campo input
        pygame.draw.rect(SCREEN, LIGHT_GRAY, (20, 20, WIDTH - 40, 100), border_radius=10)
        input_surface = FONT_INPUT.render(self.expression if self.expression
 else "0", True, BLACK)
        input_rect = input_surface.get_rect(right=WIDTH-30, centery=70)
        SCREEN.blit(input_surface, input_rect)

        # Disegna risultati (sotto input)
        if self.result != "":
            result_surface = FONT_SMALL.render("Risultato: " + self.result, True
, GRAY)
            SCREEN.blit(result_surface, (20, 130))

        # Disegna pulsanti
        for btn in self.buttons:
            btn.draw(SCREEN)

        pygame.display.flip()

    def append_char(self, char):
        if self.result != "":
            # Se c'è risultato e si digita un numero/operatori, resetta
            self.expression = ""
            self.result = ""
        self.expression += char

    def clear(self):
        self.expression = ""
        self.result = ""

    def calculate(self):
        try:
            # Sicurezza base: disabilitiamo built-ins
            self.result = str(eval(self.expression, {"__builtins__": None}, {}
))
            self.expression = self.result
        except Exception:
            self.result = "Errore"
            self.expression = ""

    def copy_to_clipboard(self):
        if self.expression:
            pyperclip.copy(self.expression)
            self.result = "Copiato negli appunti"

    def paste_from_clipboard(self):
        try:
            text = pyperclip.paste()
            # Filtriamo input: solo caratteri validi
            allowed = "0123456789+-/*()."
            filtered = ''.join(ch for ch in text if ch in allowed)
            self.expression += filtered
        except:
            self.result = "Errore incolla"

def main():
    clock = pygame.time.Clock()
    calc = Calculator()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for btn in calc.buttons:
                    if btn.is_clicked(pos):
                        label = btn.text
                        if label == 'C':
                            calc.clear()
                        elif label == '=':
                            calc.calculate()
                        elif label == 'Copy':
                            calc.copy_to_clipboard()
                        elif label == 'Paste':
                            calc.paste_from_clipboard()
                        else:
                            calc.append_char(label)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    calc.calculate()
                elif event.key == pygame.K_BACKSPACE:
                    calc.expression = calc.expression[:-1]
                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    calc.copy_to_clipboard()
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    calc.paste_from_clipboard()
                else:
                    # Mappa tastiera numeri e operatori
                    allowed_keys = {
                        pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2',
 pygame.K_3: '3',
                        pygame.K_4: '4', pygame.K_5: '5', pygame.K_6: '6',
 pygame.K_7: '7',
                        pygame.K_8: '8', pygame.K_9: '9', pygame.K_PERIOD: '.',
                        pygame.K_PLUS: '+', pygame.K_MINUS: '-',
                        pygame.K_ASTERISK: '*', pygame.K_SLASH: '/',
                        pygame.K_LEFTPAREN: '(', pygame.K_RIGHTPAREN: ')',
                    }
                    char = allowed_keys.get(event.key)
                    if char:
                        calc.append_char(char)

        calc.draw()
        clock.tick(30)

if __name__ == '__main__':
    main()
