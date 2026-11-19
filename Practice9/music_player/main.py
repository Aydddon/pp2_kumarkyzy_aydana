"""Keyboard-controlled local music player."""

from pathlib import Path

import pygame

from player import MusicPlayer


def format_time(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def main() -> None:
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Audio could not be initialized. Check your audio device/backend.")
        pygame.quit()
        return

    screen = pygame.display.set_mode((720, 360))
    pygame.display.set_caption("Keyboard Music Player")
    title_font = pygame.font.Font(None, 46)
    body_font = pygame.font.Font(None, 30)
    timer = pygame.time.Clock()
    player = MusicPlayer(Path(__file__).parent / "music")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    player.toggle_pause()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.navigate(1)
                elif event.key == pygame.K_b:
                    player.navigate(-1)

        screen.fill((28, 34, 48))
        heading = title_font.render("Music Player", True, (244, 204, 80))
        screen.blit(heading, heading.get_rect(center=(360, 70)))
        track = player.current_track
        track_name = track.name if track else "No tracks found — add audio files to music/"
        name_surface = body_font.render(track_name, True, (245, 245, 245))
        screen.blit(name_surface, name_surface.get_rect(center=(360, 145)))
        position = body_font.render(f"Position: {format_time(player.elapsed_seconds())}", True,
                                    (190, 205, 220))
        screen.blit(position, position.get_rect(center=(360, 195)))
        controls = body_font.render("P Play/Resume   S Stop   N Next   B Previous   Q Quit",
                                    True, (190, 205, 220))
        screen.blit(controls, controls.get_rect(center=(360, 285)))
        pygame.display.flip()
        timer.tick(20)

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
