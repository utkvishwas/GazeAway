import PyInstaller.__main__
import os
import shutil
from PIL import Image
import sys

def create_ico():
    """Create icon.ico if it doesn't exist"""
    if not os.path.exists('icon.ico'):
        # Create a simple eye icon
        size = 256
        image = Image.new('RGB', (size, size), color='white')
        pixels = image.load()
        
        # Draw a simple eye shape
        for x in range(size):
            for y in range(size):
                # Calculate distance from center
                dx = x - size/2
                dy = y - size/2
                distance = (dx**2 + dy**2)**0.5
                
                # Draw outer circle
                if 100 < distance < 110:
                    pixels[x, y] = (0, 0, 0)
                # Draw iris
                elif distance < 50:
                    pixels[x, y] = (0, 120, 255)
                # Draw pupil
                elif distance < 25:
                    pixels[x, y] = (0, 0, 0)
        
        # Save as ICO
        image.save('icon.ico', format='ICO')

def create_notification_sound():
    """Create a simple notification.wav if it doesn't exist"""
    if not os.path.exists('notification.wav'):
        import wave
        import struct
        import math

        # Create a simple beep sound
        sampleRate = 44100
        duration = 0.5  # seconds
        frequency = 440  # Hz
        
        wavefile = wave.open('notification.wav', 'w')
        wavefile.setnchannels(1)
        wavefile.setsampwidth(2)
        wavefile.setframerate(sampleRate)
        
        for i in range(int(duration * sampleRate)):
            value = int(32767.0 * math.sin(frequency * math.pi * 2 * i / sampleRate))
            data = struct.pack('<h', value)
            wavefile.writeframesraw(data)
        
        wavefile.close()

def build_app():
    """Build the executable"""
    # Create necessary resources
    create_ico()
    create_notification_sound()
    
    # Create build directory
    if not os.path.exists('build'):
        os.makedirs('build')
    
    # Copy resources
    shutil.copy('icon.ico', 'build/')
    shutil.copy('notification.wav', 'build/')
    
    # Define additional files to include
    additional_files = [
        ('icon.ico', '.'),
        ('notification.wav', '.')
    ]
    
    # Convert additional_files to PyInstaller format
    datas = [f"{src};{dst}" for src, dst in additional_files]
    
    # PyInstaller options
    PyInstaller.__main__.run([
        'main.py',
        '--name=GazeAway',
        '--onefile',
        '--windowed',
        '--icon=build/icon.ico',
        *[f'--add-data={data}' for data in datas],
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=PIL._imaging',
        '--hidden-import=PIL._imagingcms',
        '--clean',
        '--uac-admin',
        # Optimize and exclude unnecessary modules
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=PyQt5',
        '--exclude-module=PySide2',
        '--exclude-module=wx',
        # Optimize for size
        '--noupx',
        # Reduce false positive detection
        '--disable-windowed-traceback',
        '--strip',
    ])

if __name__ == "__main__":
    build_app()