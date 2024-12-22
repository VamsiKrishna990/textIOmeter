import pygame
import tkinter as tk
from tkinter import filedialog

def handle_shortcuts(event, text, ctrl_pressed):
    if ctrl_pressed:
        if event.key == pygame.K_s:
            save_file(text)
            print("File saved!")
    return text