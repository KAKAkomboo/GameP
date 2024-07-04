import sys
import pygame
import Config

pygame.init()

screen = pygame.display.set_mode(Config.screen_size)
pygame.display.set_caption("GG")


main_font = pygame.font.SysFont('algerian', 32)
menu_soundtrack = pygame.mixer.Sound(r'Soundtrack\Dark Souls CD 1 TRACK 21 (320).mp3')
def exit_game():
    """Вихід з гри"""

    pygame.quit()
    sys.exit()

def empty():
    return



def draw_text(text, font, color, screen, centerx, centery):
    """Виведення тексту на екран"""

    text_test = font.render(text, True, color)
    text_field = text_test.get_rect()
    text_field.centerx = centerx
    text_field.centery = centery
    screen.blit(text_test, text_field)

def main_menu():
    """Головне меню гри"""

    global menu_soundtrack
    if not pygame.mixer.get_busy():
        menu_soundtrack.play(-1)


    while Config.running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(menu_items):
                    if Config.screen_size[1]/2+Config.vertical_offset+50*i-15 < my < Config.screen_size[1]/2+Config.vertical_offset+50*i+15:
                        menu_items_map[button]()
        screen.fill((0, 0, 0))
        for i, button in enumerate(menu_items):
            if Config.screen_size[1]/2+Config.vertical_offset+50*i-15 < my < Config.screen_size[1]/2+Config.vertical_offset+50*i+15:
                draw_text(button, main_font, Config.text_hover_color, screen, Config.screen_size[0]/4.3, Config.screen_size[1]/2+Config.vertical_offset + 55*i)
            else:
                draw_text(button, main_font, Config.text_color, screen, Config.screen_size[0]/4.3, Config.screen_size[1]/2+ Config.vertical_offset +55*i)
        pygame.display.flip()


def setting():
    """Налаштування гри"""

    setting_items = ["General", "Back"]
    setting_items_map = {
        "General": empty,
        "Back": main_menu
    }
    while Config.running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(setting_items):
                    if Config.screen_size[1]/2+Config.vertical_offset_setting+370*i-15 < my < Config.screen_size[1]/2+Config.vertical_offset_setting+370*i+15:
                        setting_items_map[button]()
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (250, 250, 250), (220, 15, 2, 450))
        for i, button in enumerate(setting_items):
            if Config.screen_size[1]/2+Config.vertical_offset_setting+370*i-15 < my < Config.screen_size[1]/2+Config.vertical_offset_setting+370*i+15:
                draw_text(button, main_font, Config.text_hover_color, screen, Config.screen_size[0]/7, Config.screen_size[1]/2+Config.vertical_offset_setting + 370 * i)
            else:
                draw_text(button, main_font, Config.text_color, screen, Config.screen_size[0]/7, Config.screen_size[1]/2+ Config.vertical_offset_setting + 370 * i)
        pygame.display.flip()

menu_items = ["Play", "Setting", "Exit"]
menu_items_map = {
    "Play": empty,
    "Setting": setting,
    "Exit": exit_game
}

if __name__ == "__main__":
    main_menu()