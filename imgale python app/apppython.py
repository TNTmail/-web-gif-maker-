

from tkinter import *
import tkinter as tk
import webbrowser
import subprocess
import os
from PIL import Image, ImageTk, ImageSequence



#windows size
window = tk.Tk()
window.title("there app")
window.geometry('316x510')


image_path = os.path.join(os.path.dirname(__file__), '620_screenshots_20260516182356_1.jpg')
background_image = ImageTk.PhotoImage(Image.open(image_path).resize((316, 511)))
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_image


gif_path = os.path.join(os.path.dirname(__file__), 'projects_create-a-gif-with-python_post_JYh9Z6ow3QIVUiAPPyh2_lain.gif')
if os.path.isfile(gif_path):
    gif = Image.open(gif_path)
    gif_frames = [ImageTk.PhotoImage(frame.convert('RGBA').resize((200, 143), Image.LANCZOS)) for frame in ImageSequence.Iterator(gif)]
    gif_label = tk.Label(window, bg='black')
    gif_label.place(x=59, y=150)


    def animate_gif(frame_index=0):
        gif_label.config(image=gif_frames[frame_index])
        gif_label.image = gif_frames[frame_index]
        delay = gif.info.get('duration', 190)  # Default to 190ms if duration is not specified
        window.after(delay, animate_gif, (frame_index + 1) % len(gif_frames))

    animate_gif()
else:
    print(f'GIF not found: {gif_path}')


#os spotify
def open_spotify():
    try:
        subprocess.Popen("spotify.exe")
    except:
        webbrowser.open("https://open.spotify.com")


# Create a Spotify button
button_spotify = tk.Button(window, text="Open Spotify", command=open_spotify, bg='green', fg='black', font=('Arial', 9, 'bold'))
button_spotify.pack(pady=20)





steam_label = tk.Label(window, text="Your Steam Friend Code: 1481895473", bg='grey', fg='yellow', font=('Arial', 9))
steam_label.pack(pady=15)




exit_button = tk.Button(window, text="EXIT", command=window.quit, bg='red', fg='white', font=('Arial', 12, 'bold'))
exit_button.pack(pady=100)



button_github = tk.Button(window,fg='white', text="GitHub",bg='fuchsia', command=lambda: webbrowser.open("https://github.com"))
button_github.pack(pady=10)

example_label = tk.Label(window, text="This is an example label", bg='blue', fg='white', font=('Arial', 14, ))
example_label.pack(pady=12)


menu = tk.Menu(window)
window.config(menu=menu)
filemenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New")
filemenu.add_command(label="Open...")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)

helpmenu = tk.Menu(menu, tearoff=1)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="i love you", command=lambda: webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))





window.mainloop()