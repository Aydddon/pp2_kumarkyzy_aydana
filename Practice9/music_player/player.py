"""Small playlist controller backed by pygame.mixer.music."""

from pathlib import Path

import pygame


SUPPORTED = {".wav", ".ogg", ".mp3"}


class MusicPlayer:
    """Manage track discovery, playback, navigation, and elapsed position."""

    def __init__(self, music_dir: Path):
        self.music_dir = music_dir
        self.tracks = sorted(
            (path for path in music_dir.iterdir()
             if path.is_file() and path.suffix.lower() in SUPPORTED),
            key=lambda path: path.name.lower(),
        )
        self.index = 0
        self.started_at: int | None = None
        self.offset_ms = 0
        self.paused = False

    @property
    def current_track(self) -> Path | None:
        return self.tracks[self.index] if self.tracks else None

    def play(self) -> None:
        """Start or resume the current track, if one is available."""
        track = self.current_track
        if track is None:
            return
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.started_at = pygame.time.get_ticks()
            return
        if pygame.mixer.music.get_busy():
            return
        try:
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.play(start=max(0, self.offset_ms / 1000))
        except (pygame.error, TypeError):
            # Some formats/backends cannot seek; retry from the beginning.
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.play()
            self.offset_ms = 0
        self.started_at = pygame.time.get_ticks()
        self.paused = False

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self.started_at = None
        self.offset_ms = 0
        self.paused = False

    def navigate(self, step: int) -> None:
        """Stop the current track and select the next/previous playlist item."""
        if not self.tracks:
            return
        self.stop()
        self.index = (self.index + step) % len(self.tracks)
        self.play()

    def elapsed_seconds(self) -> int:
        if self.started_at is not None and pygame.mixer.music.get_busy():
            return self.offset_ms // 1000 + (pygame.time.get_ticks() - self.started_at) // 1000
        return self.offset_ms // 1000

    def toggle_pause(self) -> None:
        if self.paused:
            self.play()
        elif pygame.mixer.music.get_busy():
            self.offset_ms = self.elapsed_seconds() * 1000
            pygame.mixer.music.pause()
            self.started_at = None
            self.paused = True
        else:
            self.play()
