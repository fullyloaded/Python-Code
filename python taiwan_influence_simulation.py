import pygame
import random
import math
import cv2
import numpy as np
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Taiwan Influence Dynamics Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
USA_COLOR = (59, 130, 246)  # #3B82F6
CHINA_COLOR = (249, 115, 22)  # #F97316
TAIWAN_COLOR = (16, 185, 129)  # #10B981
JAPAN_COLOR = (220, 38, 38)  # #DC2626
EU_COLOR = (124, 58, 237)  # #7C3AED
PARTICLE_COLOR = (67, 56, 202)  # #4338CA
CRISIS_COLOR = (220, 38, 38)  # #DC2626
GRAY = (128, 128, 128)

# Node data
nodes = [
    {"id": "美國", "x": 120, "y": 200, "color": USA_COLOR, "size": 35, "influence": 0.8},
    {"id": "中國", "x": 580, "y": 200, "color": CHINA_COLOR, "size": 35, "influence": 0.9},
    {"id": "台灣", "x": 350, "y": 250, "color": TAIWAN_COLOR, "size": 30, "influence": 0.6},
    {"id": "日本", "x": 200, "y": 120, "color": JAPAN_COLOR, "size": 25, "influence": 0.4},
    {"id": "歐盟", "x": 500, "y": 120, "color": EU_COLOR, "size": 25, "influence": 0.3}
]

# Influence flow connections
links = [
    {"source": "美國", "target": "台灣", "type": "support", "strength": 0.8},
    {"source": "中國", "target": "台灣", "type": "pressure", "strength": 0.9},
    {"source": "美國", "target": "日本", "type": "cooperation", "strength": 0.6},
    {"source": "美國", "target": "歐盟", "type": "cooperation", "strength": 0.5},
    {"source": "中國", "target": "日本", "type": "competition", "strength": 0.4},
    {"source": "中國", "target": "歐盟", "type": "competition", "strength": 0.3},
    {"source": "日本", "target": "台灣", "type": "cooperation", "strength": 0.5},
    {"source": "歐盟", "target": "台灣", "type": "cooperation", "strength": 0.4}
]

# Initialize particles
particles = [
    {
        "x": random.uniform(20, WIDTH - 20),
        "y": random.uniform(20, HEIGHT - 20),
        "vx": (random.random() - 0.5) * 1.5,
        "vy": (random.random() - 0.5) * 1.5,
        "life": random.random()
    } for _ in range(30)
]

# State variables
is_playing = False
crisis = False
is_recording = False
vacuum_bubbles = []
recording_frames = []
recording_start_time = 0
recording_progress = 0

# Font
font = pygame.font.SysFont("Arial", 12, bold=True)

# Video writer
video_writer = None

def apply_forces():
    # Simple force simulation for nodes
    for node in nodes:
        # Repulsion between nodes
        for other in nodes:
            if node != other:
                dx = node["x"] - other["x"]
                dy = node["y"] - other["y"]
                distance = max(math.sqrt(dx**2 + dy**2), 1)
                if distance < (node["size"] + other["size"] + 20):
                    force = 200 / distance
                    node["x"] += dx / distance * force * 0.1
                    node["y"] += dy / distance * force * 0.1

        # Keep nodes within bounds
        node["x"] = max(node["size"] + 20, min(WIDTH - node["size"] - 20, node["x"]))
        node["y"] = max(node["size"] + 20, min(HEIGHT - node["size"] - 20, node["y"]))

def toggle_animation():
    global is_playing
    is_playing = not is_playing

def trigger_crisis():
    global crisis, vacuum_bubbles
    crisis = not crisis
    if crisis:
        vacuum_bubbles = [
            {
                "id": i,
                "x": 350 + (random.random() - 0.5) * 120,
                "y": 250 + (random.random() - 0.5) * 120,
                "radius": random.random() * 20 + 15,
                "opacity": 0.7
            } for i in range(5)
        ]
    else:
        vacuum_bubbles = []

def start_recording():
    global is_recording, recording_frames, recording_start_time, video_writer
    if is_recording:
        return

    is_recording = True
    recording_frames = []
    recording_start_time = pygame.time.get_ticks()

    # Initialize video writer
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Taiwan-Influence-Dynamics-{timestamp}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(filename, fourcc, 30, (WIDTH, HEIGHT))
    print(f"Started recording: {filename}")

def stop_recording():
    global is_recording, recording_frames, video_writer
    if not is_recording:
        return

    # Write frames to video
    for frame in recording_frames:
        video_writer.write(frame)
    video_writer.release()
    video_writer = None
    is_recording = False
    recording_frames = []
    print("Recording stopped and saved.")

def draw_scene():
    global recording_progress
    screen.fill(WHITE)

    # Apply forces if animation is playing or recording
    if is_playing or is_recording:
        apply_forces()

    # Draw influence flow lines
    for link in links:
        source_node = next(n for n in nodes if n["id"] == link["source"])
        target_node = next(n for n in nodes if n["id"] == link["target"])
        
        stroke_color = GRAY
        stroke_width = link["strength"] * 3
        
        if link["type"] == "support":
            stroke_color = USA_COLOR
        elif link["type"] == "pressure":
            stroke_color = CHINA_COLOR
        elif link["type"] == "cooperation":
            stroke_color = TAIWAN_COLOR
        elif link["type"] == "competition":
            stroke_color = JAPAN_COLOR

        if crisis and (link["source"] == "台灣" or link["target"] == "台灣"):
            stroke_width *= (1 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01))

        pygame.draw.line(screen, stroke_color, (source_node["x"], source_node["y"]),
                        (target_node["x"], target_node["y"]), int(stroke_width))

    # Draw flowing particles
    for particle in particles:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["life"] += 0.01

        if particle["x"] < 10 or particle["x"] > WIDTH - 10:
            particle["vx"] *= -1
            particle["x"] = max(10, min(WIDTH - 10, particle["x"]))
        if particle["y"] < 10 or particle["y"] > HEIGHT - 10:
            particle["vy"] *= -1
            particle["y"] = max(10, min(HEIGHT - 10, particle["y"]))
        
        if particle["life"] > 1:
            particle["life"] = 0

        opacity = math.sin(particle["life"] * math.pi)
        color = (*PARTICLE_COLOR, int(opacity * 128))
        pygame.draw.circle(screen, color, (particle["x"], particle["y"]), 2)

    # Draw vacuum bubbles during crisis
    if crisis:
        for bubble in vacuum_bubbles:
            x = max(bubble["radius"], min(WIDTH - bubble["radius"], bubble["x"]))
            y = max(bubble["radius"], min(HEIGHT - bubble["radius"], bubble["y"]))
            pulse_radius = bubble["radius"] * (1 + 0.2 * math.sin(pygame.time.get_ticks() * 0.005 + bubble["id"]))
            opacity = bubble["opacity"] * math.sin(pygame.time.get_ticks() * 0.003 + bubble["id"])
            color = (*CRISIS_COLOR, int(opacity * 255))
            pygame.draw.circle(screen, color, (x, y), int(pulse_radius), 2)

    # Draw country nodes
    for node in nodes:
        node_size = node["size"]
        node_color = node["color"]

        if crisis and node["id"] == "台灣":
            node_size *= (1 + 0.4 * math.sin(pygame.time.get_ticks() * 0.008))
            node_color = (
                int(node["color"][0] + (CRISIS_COLOR[0] - node["color"][0]) * 0.3),
                int(node["color"][1] + (CRISIS_COLOR[1] - node["color"][1]) * 0.3),
                int(node["color"][2] + (CRISIS_COLOR[2] - node["color"][2]) * 0.3)
            )

        pygame.draw.circle(screen, node_color, (node["x"], node["y"]), node_size)
        pygame.draw.circle(screen, WHITE, (node["x"], node["y"]), node_size, 3)

        text = font.render(node["id"], True, WHITE)
        text_rect = text.get_rect(center=(node["x"], node["y"] + 5))
        screen.blit(text, text_rect)

    # Update recording progress
    if is_recording:
        elapsed = (pygame.time.get_ticks() - recording_start_time) / 1000
        recording_progress = min(elapsed / 10 * 100, 100)
        if elapsed >= 10:
            stop_recording()

        # Capture frame for recording
        frame = pygame.surfarray.array3d(screen)
        frame = np.transpose(frame, (1, 0, 2))  # Convert to (height, width, channels)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        recording_frames.append(frame)

    # Draw UI elements
    button_y = HEIGHT - 40
    buttons = [
        ("Start/Pause Animation" if not is_playing else "Pause Animation", (0, 255, 0) if not is_playing else (255, 0, 0), toggle_animation),
        ("Trigger φ₃ Crisis" if not crisis else "Stop φ₃ Crisis", (0, 0, 255) if not crisis else (255, 165, 0), trigger_crisis),
        (f"Record Video (10s) {int(recording_progress)}%" if is_recording else "Record Video (10s)", (128, 128, 128) if is_recording else (128, 0, 128), start_recording if not is_recording else stop_recording)
    ]

    for i, (text, color, action) in enumerate(buttons):
        button_rect = pygame.Rect(10 + i * 220, button_y, 200, 30)
        pygame.draw.rect(screen, color, button_rect, border_radius=5)
        button_text = font.render(text, True, WHITE)
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

    # Draw recording progress bar
    if is_recording:
        progress_rect = pygame.Rect(10, HEIGHT - 60, WIDTH - 20, 10)
        pygame.draw.rect(screen, (200, 200, 200), progress_rect)
        progress_fill = pygame.Rect(10, HEIGHT - 60, (WIDTH - 20) * recording_progress / 100, 10)
        pygame.draw.rect(screen, (128, 0, 128), progress_fill)

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                button_y = HEIGHT - 40
                for i, (_, _, action) in enumerate([
                    (None, None, toggle_animation),
                    (None, None, trigger_crisis),
                    (None, None, start_recording if not is_recording else stop_recording)
                ]):
                    button_rect = pygame.Rect(10 + i * 220, button_y, 200, 30)
                    if button_rect.collidepoint(mouse_pos):
                        action()

        draw_scene()
        pygame.display.flip()
        clock.tick(30)

    if is_recording:
        stop_recording()
    pygame.quit()

if __name__ == "__main__":
    main()
