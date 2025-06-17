import pygame

class Dropdown:
    def __init__(self, x, y, width, height, font, options, main_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = main_color
        self.hover_color = hover_color
        self.font = font
        self.options = options
        self.selected = options[0]
        self.expanded = False

    def draw(self, win):
        pygame.draw.rect(win, self.hover_color if self.expanded else self.color, self.rect)
        selected_text = self.font.render(self.selected, True, "black")
        win.blit(selected_text, (self.rect.x + 5, self.rect.y + 5))

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x, 
                    self.rect.y + (i + 1) * self.rect.height, 
                    self.rect.width, 
                    self.rect.height
                )
                pygame.draw.rect(win, self.color, option_rect)
                option_text = self.font.render(option, True, "black")
                win.blit(option_text, (option_rect.x + 5, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                self.expanded = not self.expanded
                return self.selected
            elif self.expanded:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x, 
                        self.rect.y + (i + 1) * self.rect.height, 
                        self.rect.width, 
                        self.rect.height
                    )
                    if option_rect.collidepoint(mouse_pos):
                        self.selected = option
                        self.expanded = False
                        return self.selected
                self.expanded = False
        return self.selected