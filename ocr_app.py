import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None

def select_image(text_widget):
    if Image is None or pytesseract is None:
        messagebox.showerror('Error', 'Required libraries are not installed.')
        return
    file_path = filedialog.askopenfilename(
        title='Select image',
        filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp *.gif')] )
    if file_path:
        try:
            image = Image.open(file_path)
            extracted = pytesseract.image_to_string(image)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, extracted)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to process image: {e}')


def main():
    root = tk.Tk()
    root.title('Image Text Reader')

    text_widget = tk.Text(root, wrap=tk.WORD, width=60, height=20)
    text_widget.pack(padx=10, pady=10)

    btn = tk.Button(root, text='Select Image',
                    command=lambda: select_image(text_widget))
    btn.pack(pady=5)

    root.mainloop()


if __name__ == '__main__':
    main()
