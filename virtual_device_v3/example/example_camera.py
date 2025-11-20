#!/usr/bin/env python3
"""
Camera Example
==============
This example demonstrates the SafeHome Camera with:
- Pan left/right (range: -5 to +5)
- Zoom in/out (range: 1x to 9x)
- Real-time view display
- Time counter

This is the main example extracted from device_camera.py

Requirements:
    - Pillow (PIL) library: pip install Pillow
    - Optional: camera1.jpg in current directory for image display

Usage:
    python -m example.example_camera
    OR
    python example_camera.py (when run from example directory)
"""

import sys
import tkinter as tk
from tkinter import Label, Button, Frame
from pathlib import Path

def main():
    """Run the Camera example."""
    
    try:
        from PIL import Image, ImageTk
        # Try relative import first (for package execution), fall back to absolute
        try:
            from device.device_camera import DeviceCamera
        except ImportError:
            from ..device.device_camera import DeviceCamera


        # Create main window
        root = tk.Tk()
        root.title("SafeHome Camera Viewer")
        root.geometry("820x900")
        root.resizable(False, False)
        
        # Create camera
        camera = DeviceCamera()
        camera.set_id(1)
        
        # Wait for image to be loaded
        max_wait = 10  # Maximum 1 second wait
        wait_count = 0
        while camera.imgSource is None and wait_count < max_wait:
            root.update()  # Process pending events
            import time
            time.sleep(0.1)
            wait_count += 1
        
        if camera.imgSource is None:
            print("ERROR: Failed to load camera image!")
            root.destroy()
            return
        
        print(f"✓ Camera image loaded: {camera.imgSource.size}")
        
        # Header
        header = Label(root, text="🎥 SafeHome Camera Viewer", 
                      font=('Arial', 16, 'bold'), fg='blue', bg='lightgray')
        header.pack(pady=10, fill='x')
        
        canvas = tk.Canvas(root, width=500, height=500, bg='black', highlightthickness=2, highlightbackground='gray')
        canvas.pack(pady=10, padx=10)
        
        # Initialize canvas with first frame
        from PIL import ImageTk  # ensure in scope
        first_img = camera.get_view()
        if first_img.mode != 'RGB':
            first_img = first_img.convert('RGB')
        first_photo = ImageTk.PhotoImage(first_img, master=canvas)
        canvas_image_id = canvas.create_image(0, 0, image=first_photo, anchor='nw')
        canvas._current_photo = first_photo
        
        print(f"✓ Initial frame set on canvas (ID: {canvas_image_id})")

        # Status label
        status_label = Label(root, text="", font=('Courier', 11, 'bold'), 
                           fg='blue', bg='lightyellow', bd=2, relief='ridge')
        status_label.pack(pady=5, padx=10, fill='x')
        
        # Control frame
        control_frame = Frame(root, bg='lightgray', bd=2, relief='groove')
        control_frame.pack(pady=10, padx=10, fill='x')
        
        control_title = Label(control_frame, text="Camera Controls", 
                            font=('Arial', 12, 'bold'), bg='lightgray')
        control_title.pack(pady=5)
        
        # Control buttons
        btn_frame = Frame(control_frame, bg='lightgray')
        btn_frame.pack(pady=5)
        
        btn_width = 15
        btn_height = 2
        
        # Pan controls
        pan_frame = Frame(btn_frame, bg='lightgray')
        pan_frame.grid(row=0, column=0, padx=20)
        Label(pan_frame, text="Pan", font=('Arial', 10, 'bold'), 
              bg='lightgray').pack()
        Button(pan_frame, text="◀◀ Left", 
               command=lambda: camera.pan_left(), 
               width=btn_width, height=btn_height, bg='lightblue',
               font=('Arial', 10, 'bold')).pack(side='left', padx=2)
        Button(pan_frame, text="Right ▶▶", 
               command=lambda: camera.pan_right(), 
               width=btn_width, height=btn_height, bg='lightblue',
               font=('Arial', 10, 'bold')).pack(side='left', padx=2)
        
        # Zoom controls
        zoom_frame = Frame(btn_frame, bg='lightgray')
        zoom_frame.grid(row=0, column=1, padx=20)
        Label(zoom_frame, text="Zoom", font=('Arial', 10, 'bold'), 
              bg='lightgray').pack()
        Button(zoom_frame, text="🔍+ In", 
               command=lambda: camera.zoom_in(), 
               width=btn_width, height=btn_height, bg='lightgreen',
               font=('Arial', 10, 'bold')).pack(side='left', padx=2)
        Button(zoom_frame, text="🔍- Out", 
               command=lambda: camera.zoom_out(), 
               width=btn_width, height=btn_height, bg='lightgreen',
               font=('Arial', 10, 'bold')).pack(side='left', padx=2)
        
        # Info panel
        info_text = """Camera Controls:
• Pan: Move view left/right (range: -5 to +5)
• Zoom: Adjust zoom level (range: 1x to 9x)
• Time: Updates automatically every second
• View: Real-time camera feed with overlays"""
        
        info_label = Label(root, text=info_text, justify='left', 
                          font=('Arial', 9), fg='darkblue', bg='lightyellow',
                          bd=2, relief='ridge', padx=10, pady=5)
        info_label.pack(pady=5, padx=10, fill='x')
        
        # Update function
        update_count = [0]  # Using list for mutable counter
        
        def update_view():
            """Update camera view and status."""
            update_count[0] += 1
            
            try:
                img = camera.get_view()
                
                # Debug first few updates
                if update_count[0] <= 3:
                    print(f"Update #{update_count[0]}: img size={img.size}, mode={img.mode}")
                
                # Ensure image is in correct format
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Convert to PhotoImage and update canvas
                photo = ImageTk.PhotoImage(img, master=canvas)
                # Update existing canvas image item
                canvas.itemconfig(canvas_image_id, image=photo)
                canvas._current_photo = photo  # Keep reference to prevent garbage collection
                
                # Force canvas to redraw
                canvas.update_idletasks()
                
                if update_count[0] == 1:
                    print(f"  PhotoImage created and set to canvas")
                
            except Exception as e:
                print(f"  ERROR in update_view: {e}")
                import traceback
                traceback.print_exc()
            
            # Update status
            status = f"Camera ID: {camera.get_id()} | "
            status += f"Time: {camera.time:02d} sec | "
            status += f"Zoom: {camera.zoom}x | "
            if camera.pan > 0:
                status += f"Pan: Right {camera.pan}"
            elif camera.pan == 0:
                status += "Pan: Center"
            else:
                status += f"Pan: Left {abs(camera.pan)}"
            status_label.config(text=status)
            
            # Schedule next update
            root.after(100, update_view)
        
        # Start updating
        update_view()
        
        # Cleanup on close
        def on_closing():
            camera.stop()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except ImportError as e:
        sys.exit(1)


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    main()
