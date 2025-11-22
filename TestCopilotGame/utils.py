"""
TestCopilotGame - Utility Functions
Helper functions and utility classes used throughout the game.
"""

import pygame
import math
import random
from typing import Tuple, List


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between min and max."""
    return max(min_value, min(max_value, value))


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between start and end."""
    t = clamp(t, 0.0, 1.0)
    return start + (end - start) * t


def distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """Calculate distance between two points."""
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.sqrt(dx * dx + dy * dy)


def normalize_vector(x: float, y: float) -> Tuple[float, float]:
    """Normalize a vector to unit length."""
    length = math.sqrt(x * x + y * y)
    if length == 0:
        return (0, 0)
    return (x / length, y / length)


def angle_to_vector(angle: float) -> Tuple[float, float]:
    """Convert angle in radians to normalized vector."""
    return (math.cos(angle), math.sin(angle))


def vector_to_angle(x: float, y: float) -> float:
    """Convert vector to angle in radians."""
    return math.atan2(y, x)


def rotate_point(x: float, y: float, angle: float) -> Tuple[float, float]:
    """Rotate a point around origin by angle in radians."""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (
        x * cos_a - y * sin_a,
        x * sin_a + y * cos_a
    )


def point_in_rect(point: Tuple[float, float], rect: pygame.Rect) -> bool:
    """Check if point is inside rectangle."""
    return rect.collidepoint(point)


def rects_overlap(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """Check if two rectangles overlap."""
    return rect1.colliderect(rect2)


def random_color() -> Tuple[int, int, int]:
    """Generate a random RGB color."""
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def random_color_vibrant() -> Tuple[int, int, int]:
    """Generate a random vibrant RGB color."""
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (255, 0, 255), (0, 255, 255),
        (255, 165, 0), (128, 0, 128)
    ]
    return random.choice(colors)


def random_position(width: int, height: int) -> Tuple[float, float]:
    """Generate a random position within given dimensions."""
    return (
        random.randint(0, width),
        random.randint(0, height)
    )


def random_position_around(center_x: float, center_y: float, radius: float) -> Tuple[float, float]:
    """Generate a random position around a center point."""
    angle = random.uniform(0, math.pi * 2)
    dist = random.uniform(0, radius)
    return (
        center_x + math.cos(angle) * dist,
        center_y + math.sin(angle) * dist
    )


def wrap_position(x: float, y: float, width: int, height: int) -> Tuple[float, float]:
    """Wrap position around screen boundaries."""
    x = x % width
    y = y % height
    if x < 0:
        x += width
    if y < 0:
        y += height
    return (x, y)


def bounce_position(x: float, y: float, vx: float, vy: float, width: int, height: int) -> Tuple[float, float, float, float]:
    """Bounce position off screen boundaries."""
    if x < 0 or x > width:
        vx = -vx
        x = clamp(x, 0, width)
    if y < 0 or y > height:
        vy = -vy
        y = clamp(y, 0, height)
    return (x, y, vx, vy)


def ease_in_out(t: float) -> float:
    """Ease in-out function for smooth animations."""
    return t * t * (3.0 - 2.0 * t)


def ease_in(t: float) -> float:
    """Ease in function for animations."""
    return t * t


def ease_out(t: float) -> float:
    """Ease out function for animations."""
    return 1.0 - (1.0 - t) * (1.0 - t)


def smooth_step(t: float) -> float:
    """Smooth step function."""
    t = clamp(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def pulse(t: float, speed: float = 1.0) -> float:
    """Pulsing value between 0 and 1."""
    return (math.sin(t * speed * 2 * math.pi) + 1.0) / 2.0


def format_number(num: int) -> str:
    """Format large numbers with K, M suffixes."""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    else:
        return str(num)


def format_time(seconds: float) -> str:
    """Format time in MM:SS format."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color string."""
    return '#%02x%02x%02x' % rgb


def darken_color(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """Darken a color by a factor (0.0 to 1.0)."""
    factor = clamp(factor, 0.0, 1.0)
    return (
        int(color[0] * factor),
        int(color[1] * factor),
        int(color[2] * factor)
    )


def lighten_color(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """Lighten a color by a factor (0.0 to 1.0)."""
    factor = clamp(factor, 0.0, 1.0)
    return (
        int(color[0] + (255 - color[0]) * factor),
        int(color[1] + (255 - color[1]) * factor),
        int(color[2] + (255 - color[2]) * factor)
    )


def blend_colors(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """Blend two colors with interpolation factor t."""
    t = clamp(t, 0.0, 1.0)
    return (
        int(color1[0] * (1 - t) + color2[0] * t),
        int(color1[1] * (1 - t) + color2[1] * t),
        int(color1[2] * (1 - t) + color2[2] * t)
    )


class Timer:
    """Simple timer class for tracking elapsed time."""
    
    def __init__(self, duration: float):
        self.duration = duration
        self.elapsed = 0.0
        self.active = False
    
    def start(self):
        """Start the timer."""
        self.active = True
        self.elapsed = 0.0
    
    def update(self, dt: float):
        """Update the timer."""
        if self.active:
            self.elapsed += dt
            if self.elapsed >= self.duration:
                self.active = False
    
    def reset(self):
        """Reset the timer."""
        self.elapsed = 0.0
        self.active = False
    
    def is_done(self) -> bool:
        """Check if timer is complete."""
        return not self.active and self.elapsed >= self.duration
    
    def get_progress(self) -> float:
        """Get timer progress from 0.0 to 1.0."""
        if self.duration == 0:
            return 1.0
        return clamp(self.elapsed / self.duration, 0.0, 1.0)


class Counter:
    """Simple counter class with min/max bounds."""
    
    def __init__(self, initial: float = 0.0, min_value: float = None, max_value: float = None):
        self.value = initial
        self.min_value = min_value
        self.max_value = max_value
    
    def increment(self, amount: float = 1.0):
        """Increment counter."""
        self.value += amount
        if self.max_value is not None:
            self.value = min(self.value, self.max_value)
    
    def decrement(self, amount: float = 1.0):
        """Decrement counter."""
        self.value -= amount
        if self.min_value is not None:
            self.value = max(self.value, self.min_value)
    
    def reset(self, value: float = 0.0):
        """Reset counter."""
        self.value = value
    
    def get(self) -> float:
        """Get counter value."""
        return self.value


class FadeTransition:
    """Screen fade transition effect."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.alpha = 0
        self.fade_in = False
        self.fade_out = False
        self.surface = pygame.Surface((width, height))
        self.surface.set_alpha(self.alpha)
        self.speed = 500  # pixels per second
    
    def start_fade_in(self):
        """Start fade in transition."""
        self.fade_in = True
        self.fade_out = False
        self.alpha = 255
    
    def start_fade_out(self):
        """Start fade out transition."""
        self.fade_out = True
        self.fade_in = False
        self.alpha = 0
    
    def update(self, dt: float):
        """Update fade transition."""
        if self.fade_in:
            self.alpha = max(0, self.alpha - self.speed * dt)
            if self.alpha <= 0:
                self.fade_in = False
        elif self.fade_out:
            self.alpha = min(255, self.alpha + self.speed * dt)
            if self.alpha >= 255:
                self.fade_out = False
        
        self.surface.set_alpha(int(self.alpha))
    
    def render(self, screen: pygame.Surface):
        """Render fade overlay."""
        if self.alpha > 0:
            self.surface.fill((0, 0, 0))
            screen.blit(self.surface, (0, 0))
    
    def is_active(self) -> bool:
        """Check if fade is active."""
        return self.fade_in or self.fade_out


class ScreenShake:
    """Screen shake effect."""
    
    def __init__(self):
        self.duration = 0.0
        self.intensity = 0.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.active = False
    
    def shake(self, duration: float, intensity: float):
        """Start screen shake."""
        self.duration = duration
        self.intensity = intensity
        self.active = True
    
    def update(self, dt: float):
        """Update screen shake."""
        if self.active:
            self.duration -= dt
            if self.duration > 0:
                import random
                self.offset_x = random.uniform(-self.intensity, self.intensity)
                self.offset_y = random.uniform(-self.intensity, self.intensity)
                self.intensity *= 0.9  # Decay
            else:
                self.offset_x = 0.0
                self.offset_y = 0.0
                self.active = False
    
    def get_offset(self) -> Tuple[float, float]:
        """Get current shake offset."""
        return (self.offset_x, self.offset_y)


def load_image(path: str, scale: float = 1.0) -> pygame.Surface:
    """Load and optionally scale an image."""
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale != 1.0:
            size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, size)
        return image
    except:
        # Return placeholder surface if image not found
        surface = pygame.Surface((32, 32))
        surface.fill((255, 0, 255))  # Magenta for missing texture
        return surface


def create_text_surface(text: str, font: pygame.font.Font, color: Tuple[int, int, int]) -> pygame.Surface:
    """Create a text surface."""
    return font.render(text, True, color)


def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, 
              color: Tuple[int, int, int], x: int, y: int, 
              center: bool = False, shadow: bool = False) -> None:
    """Draw text on screen with optional centering and shadow."""
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    
    if shadow:
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect()
        shadow_rect.center = rect.center
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(shadow_surface, shadow_rect)
    
    screen.blit(surface, rect)


def draw_progress_bar(screen: pygame.Surface, x: int, y: int, width: int, height: int,
                     progress: float, color: Tuple[int, int, int],
                     border_color: Tuple[int, int, int] = None,
                     bg_color: Tuple[int, int, int] = None) -> None:
    """Draw a progress bar."""
    progress = clamp(progress, 0.0, 1.0)
    
    if bg_color:
        pygame.draw.rect(screen, bg_color, (x, y, width, height))
    
    fill_width = int(width * progress)
    if fill_width > 0:
        pygame.draw.rect(screen, color, (x, y, fill_width, height))
    
    if border_color:
        pygame.draw.rect(screen, border_color, (x, y, width, height), 2)


class Animation:
    """Animation class for sprite animations."""
    
    def __init__(self, frames: List[pygame.Surface], fps: float = 10.0, loop: bool = True):
        """Initialize animation."""
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.current_frame = 0
        self.frame_time = 0.0
        self.playing = False
        self.finished = False
    
    def play(self):
        """Start playing animation."""
        self.playing = True
        self.finished = False
        self.current_frame = 0
        self.frame_time = 0.0
    
    def stop(self):
        """Stop animation."""
        self.playing = False
        self.current_frame = 0
        self.frame_time = 0.0
    
    def update(self, dt: float):
        """Update animation frame."""
        if not self.playing:
            return
        
        self.frame_time += dt
        frame_duration = 1.0 / self.fps if self.fps > 0 else 0.0
        
        if self.frame_time >= frame_duration:
            self.current_frame += 1
            self.frame_time = 0.0
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.playing = False
                    self.finished = True
    
    def get_current_frame(self) -> pygame.Surface:
        """Get current animation frame."""
        if self.frames and 0 <= self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None
    
    def is_finished(self) -> bool:
        """Check if animation is finished."""
        return self.finished


class SpriteSheet:
    """Sprite sheet loader and manager."""
    
    def __init__(self, image_path: str, sprite_width: int, sprite_height: int):
        """Initialize sprite sheet."""
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.sprite_width = sprite_width
            self.sprite_height = sprite_height
            self.sheet_width = self.image.get_width() // sprite_width
            self.sheet_height = self.image.get_height() // sprite_height
        except:
            self.image = None
            self.sprite_width = 0
            self.sprite_height = 0
            self.sheet_width = 0
            self.sheet_height = 0
    
    def get_sprite(self, x: int, y: int) -> pygame.Surface:
        """Get sprite at grid position (x, y)."""
        if not self.image:
            return None
        
        if 0 <= x < self.sheet_width and 0 <= y < self.sheet_height:
            rect = pygame.Rect(
                x * self.sprite_width,
                y * self.sprite_height,
                self.sprite_width,
                self.sprite_height
            )
            return self.image.subsurface(rect)
        return None
    
    def get_animation(self, row: int, start_col: int = 0, end_col: int = None, fps: float = 10.0) -> Animation:
        """Get animation from a row of sprites."""
        if not self.image:
            return None
        
        if end_col is None:
            end_col = self.sheet_width - 1
        
        frames = []
        for col in range(start_col, min(end_col + 1, self.sheet_width)):
            sprite = self.get_sprite(col, row)
            if sprite:
                frames.append(sprite)
        
        if frames:
            return Animation(frames, fps)
        return None


class ColorPalette:
    """Color palette management."""
    
    def __init__(self, colors: List[Tuple[int, int, int]]):
        """Initialize color palette."""
        self.colors = colors
        self.current_index = 0
    
    def get_color(self, index: int = None) -> Tuple[int, int, int]:
        """Get color at index."""
        if index is None:
            index = self.current_index
        
        if 0 <= index < len(self.colors):
            return self.colors[index]
        return (255, 255, 255)  # Default white
    
    def next_color(self) -> Tuple[int, int, int]:
        """Get next color in palette."""
        color = self.get_color(self.current_index)
        self.current_index = (self.current_index + 1) % len(self.colors)
        return color
    
    def random_color(self) -> Tuple[int, int, int]:
        """Get random color from palette."""
        import random
        return random.choice(self.colors)


class InputHandler:
    """Input handler for keyboard and mouse."""
    
    def __init__(self):
        """Initialize input handler."""
        self.keys = {}
        self.keys_pressed = {}
        self.keys_released = {}
        self.mouse_pos = (0, 0)
        self.mouse_buttons = {}
        self.mouse_buttons_pressed = {}
        self.mouse_buttons_released = {}
    
    def update(self):
        """Update input state."""
        # Reset frame-specific states
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.mouse_buttons_pressed.clear()
        self.mouse_buttons_released.clear()
        
        # Update keyboard
        current_keys = pygame.key.get_pressed()
        for key in range(len(current_keys)):
            was_pressed = self.keys.get(key, False)
            is_pressed = current_keys[key]
            
            self.keys[key] = is_pressed
            
            if is_pressed and not was_pressed:
                self.keys_pressed[key] = True
            elif not is_pressed and was_pressed:
                self.keys_released[key] = True
        
        # Update mouse
        self.mouse_pos = pygame.mouse.get_pos()
        current_mouse = pygame.mouse.get_pressed()
        
        for button in range(len(current_mouse)):
            was_pressed = self.mouse_buttons.get(button, False)
            is_pressed = current_mouse[button]
            
            self.mouse_buttons[button] = is_pressed
            
            if is_pressed and not was_pressed:
                self.mouse_buttons_pressed[button] = True
            elif not is_pressed and was_pressed:
                self.mouse_buttons_released[button] = True
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if key is currently pressed."""
        return self.keys.get(key, False)
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if key was just pressed this frame."""
        return self.keys_pressed.get(key, False)
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if key was just released this frame."""
        return self.keys_released.get(key, False)
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if mouse button is currently pressed."""
        return self.mouse_buttons.get(button, False)
    
    def is_mouse_button_just_pressed(self, button: int) -> bool:
        """Check if mouse button was just pressed this frame."""
        return self.mouse_buttons_pressed.get(button, False)
    
    def is_mouse_button_just_released(self, button: int) -> bool:
        """Check if mouse button was just released this frame."""
        return self.mouse_buttons_released.get(button, False)
    
    def get_mouse_pos(self) -> Tuple[int, int]:
        """Get mouse position."""
        return self.mouse_pos

