import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color

    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(win, color, self.rect)
        text_surf = self.font.render(self.text, True, "black")
        win.blit(text_surf, (
            self.rect.centerx - text_surf.get_width() / 2,
            self.rect.centery - text_surf.get_height() / 2
        ))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos())