import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

class GIFmaker(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title('GIF Maker')
        self.geometry("640x700")
        
        # State variables
        self.image_paths = []
        self.output_path = ''
        self.drive_paths = {
            f'{letter}:': f'{letter}:\\'
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if os.path.exists(f'{letter}:\\')
        }

        # Menu and Keybinds
        self.create_menu()
        self.bind('<F1>', lambda event: self.show_help())
        color = '#222222'
        self.configure(bg=color)

        # Widget Construction
        self.select_images_button = tk.Button(self, text='Select Images', command=self.select_images)
        self.select_images_button.pack(padx=15, pady=8)

        # Image Listbox Frame
        list_frame = tk.Frame(self)
        list_frame.pack(fill=tk.X, padx=10, pady=5)
        self.image_listbox = tk.Listbox(list_frame, height=4, exportselection=False)
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar = tk.Scrollbar(list_frame, command=self.image_listbox.yview)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_listbox.config(yscrollcommand=list_scrollbar.set)
        self.image_listbox.bind('<<ListboxSelect>>', self.preview_selected_image)

        self.preview_label = tk.Label(self, text="Image Preview")
        self.preview_label.pack(pady=(5, 0))

        # Preview Canvas
        self.canvas = tk.Canvas(self, width=400, height=250, background="white")
        self.canvas.pack(pady=5)

        # Scale Control
        self.scale_label = tk.Label(self, text='Scale (0.1 - 100.0):')
        self.scale_label.pack(pady=(5, 0))
        self.scale_entry = tk.Entry(self, width=10)
        self.scale_entry.pack()
        self.scale_entry.insert(0, '1.0')

        # Export Buttons
        action_frame = tk.Frame(self)
        action_frame.pack(pady=10)
        self.export_button = tk.Button(action_frame, text='Export to GIF', command=self.export_gif)
        self.export_button.pack(side=tk.LEFT, padx=5)
        self.drive_button = tk.Button(action_frame, text='Save to Selected Drive Folder', command=self.save_to_drive)
        self.drive_button.pack(side=tk.LEFT, padx=5)

        # Drive Explorer Widgets
        self.drive_var = tk.StringVar()
        self.drive_selector = ttk.Combobox(
            self, textvariable=self.drive_var, values=list(self.drive_paths.keys()), state='readonly'
        )
        self.drive_selector.pack(pady=(5, 2))
        self.drive_selector.bind('<<ComboboxSelected>>', self.select_drive)

        self.drive_label = tk.Label(self, text='Drive Explorer')
        self.drive_label.pack(pady=(2, 2))
        
        c_drive_frame = tk.Frame(self)
        c_drive_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.c_drive_listbox = tk.Listbox(c_drive_frame, height=5, exportselection=False)
        self.c_drive_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        c_drive_scrollbar = tk.Scrollbar(c_drive_frame, command=self.c_drive_listbox.yview)
        c_drive_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.c_drive_listbox.config(yscrollcommand=c_drive_scrollbar.set)
        self.c_drive_listbox.bind('<Double-1>', self.open_c_drive_folder)

        if not self.drive_paths:
            self.drive_label.config(text='No drives found')
        else:
            initial_drive = 'C:' if 'C:' in self.drive_paths else next(iter(self.drive_paths))
            self.drive_var.set(initial_drive)
            self.refresh_drive()

        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        self.progress.pack(pady=5)

        self.exit_button = tk.Button(self, text='Exit', width=15, command=self.destroy)
        self.exit_button.pack(pady=5)

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)
        
        filemenu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Select Images", command=self.select_images)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)

        # Generate Help Icon dynamically
        icon_image = Image.new('RGBA', (32, 32), (255, 255, 255, 0))
        icon_draw = ImageDraw.Draw(icon_image)
        try:
            icon_font = ImageFont.truetype('arialbd.ttf', 24)
        except OSError:
            icon_font = ImageFont.load_default()
            
        icon_draw.text((8, 0), '?', font=icon_font, fill='orange')
        self.help_icon = ImageTk.PhotoImage(icon_image)

        helpmenu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Help Guide", command=self.show_help, image=self.help_icon, compound="right")

    def show_help(self):
        help_window = tk.Toplevel(self)
        help_window.title('Help')
        help_window.geometry('400x300')
        help_window.configure(bg='#222222')
        help_window.transient(self)
        help_window.grab_set()

        tk.Label(
            help_window, text='Help', font=('Arial', 18, 'bold'), fg='white', bg='#000000'
        ).pack(pady=20)
        
        help_text = (
            "1. Click 'Select Images' to import frame images.\n"
            
            
            
        )
        tk.Label(
            help_window, text=help_text, justify=tk.LEFT, fg='white', bg='#222222', font=('Arial', 10)
        ).pack(padx=20, pady=10)

    def select_images(self):
        paths = filedialog.askopenfilenames(
            title='Select images',
            filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp *.webp'), ('All files', '*.*')]
        )
        if not paths:
            return

        self.image_paths = list(paths)
        self.image_listbox.delete(0, tk.END)
        for path in self.image_paths:
            self.image_listbox.insert(tk.END, os.path.basename(path))
        self.image_listbox.selection_set(0)

        self.show_image(self.image_paths[0])
        self.preview_label.config(text=f'{len(self.image_paths)} image(s) selected')

    def preview_selected_image(self, event=None):
        selection = self.image_listbox.curselection()
        if selection and selection[0] < len(self.image_paths):
            self.show_image(self.image_paths[selection[0]])

    def show_image(self, path):
        try:
            image = Image.open(path).convert('RGB')
        except (OSError, ValueError) as error:
            messagebox.showerror('Error', f'Could not open the selected image:\n{error}')
            return

        image.thumbnail((400, 250))
        self.preview_image = ImageTk.PhotoImage(image)
        self.canvas.delete('all')
        self.canvas.create_image(200, 125, image=self.preview_image)

    def export_gif(self, initial_dir=None):
        if not self.image_paths:
            messagebox.showwarning('Select images', 'Please select images first.')
            return

        try:
            scale = float(self.scale_entry.get())
            if not 0.1 <= scale <= 100.0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Invalid scale', 'Enter a number from 0.1 to 100.0.')
            return

        output_path = filedialog.asksaveasfilename(
            title='Save GIF',
            defaultextension='.gif',
            filetypes=[('GIF files', '*.gif')],
            initialdir=initial_dir
        )
        if not output_path:
            return

        frames = []
        self.progress.start(10)
        try:
            frame_size = None
            for path in self.image_paths:
                with Image.open(path) as source:
                    image = source.convert('RGB')
                width, height = image.size
                target_size = (max(1, int(width * scale)), max(1, int(height * scale)))
                if frame_size is None:
                    frame_size = target_size
                image = image.resize(frame_size, Image.Resampling.LANCZOS)
                frames.append(image)
        except (OSError, ValueError) as error:
            messagebox.showerror('Error', f'Could not process image:\n{error}')
            return
        finally:
            self.progress.stop()

        if not frames:
            messagebox.showerror('Error', 'No images were selected.')
            return

        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=500,
            loop=0,
            optimize=True
        )
        messagebox.showinfo('Complete', f'GIF saved to:\n{output_path}')
        return output_path

    def save_to_drive(self):
        current_path = self.drive_paths.get(self.drive_var.get())
        if current_path:
            self.export_gif(initial_dir=current_path)

    def select_drive(self, event=None):
        self.refresh_drive()

    def refresh_drive(self):
        current_path = self.drive_paths.get(self.drive_var.get())
        if not current_path:
            return

        self.c_drive_listbox.delete(0, tk.END)
        self.c_drive_listbox.insert(tk.END, '[Folder] .. (Up Parent Directory)')
        
        try:
            entries = sorted(os.listdir(current_path), key=str.lower)
        except OSError as error:
            self.drive_label.config(text=f'Cannot read {current_path}: {error}')
            return

        for entry in entries:
            full_path = os.path.join(current_path, entry)
            prefix = '[Folder] ' if os.path.isdir(full_path) else '[File] '
            self.c_drive_listbox.insert(tk.END, prefix + entry)

        self.drive_label.config(text=f'{self.drive_var.get()} drive: {current_path}')

    def open_c_drive_folder(self, event=None):
        selection = self.c_drive_listbox.curselection()
        if not selection:
            return

        selected = self.c_drive_listbox.get(selection[0])
        if not selected.startswith('[Folder] '):
            return

        folder_name = selected[len('[Folder] '):]
        current_path = self.drive_paths.get(self.drive_var.get())

        if folder_name.startswith('..'):
            parent_path = os.path.dirname(os.path.abspath(current_path))
            if parent_path and os.path.exists(parent_path):
                self.drive_paths[self.drive_var.get()] = parent_path
        else:
            self.drive_paths[self.drive_var.get()] = os.path.join(current_path, folder_name)
            
        self.refresh_drive()


if __name__ == '__main__':
    app = GIFmaker()
    app.mainloop()