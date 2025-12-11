import tkinter as tk
from tkinter import ttk



def main():
    root = tk.Tk()
    root.title("Line Break Remover")
    root.geometry("800x400")
    root.resizable(False, False)

    def remove_linebreaks():
        text = input_text.get("1.0", tk.END).strip()
        no_breaks = text.replace("\n", " ").replace("\r", "").replace("\\\\\\\\", "\n\\\\\\\\\n")

        original_output.delete("1.0", tk.END)
        original_output.insert("1.0", text)

        modified_output.delete("1.0", tk.END)
        modified_output.insert("1.0", no_breaks)

    def clear():
        original_output.delete("1.0", tk.END)
        modified_output.delete("1.0", tk.END)
        input_text.delete("1.0", tk.END)


    # Input frame
    input_label = ttk.Label(root, text="Enter Text:")
    input_label.pack(anchor="w", padx=10, pady=(10, 0))

    input_text = tk.Text(root, height=6, width=90, wrap="word")
    input_text.pack(padx=10, pady=5)

    process_btn = ttk.Button(root, text="Remove Line Breaks", command=remove_linebreaks)
    process_btn.pack(pady=10)

    clear_btn = ttk.Button(root, text="Clear", command=clear)
    clear_btn.pack(pady=10)


    # Output frame
    output_frame = ttk.Frame(root)
    output_frame.pack(fill="both", expand=True, padx=10, pady=5)

    original_label = ttk.Label(output_frame, text="Original Text")
    original_label.grid(row=0, column=0, sticky="w")

    modified_label = ttk.Label(output_frame, text="No Line Breaks")
    modified_label.grid(row=0, column=1, sticky="w")

    original_output = tk.Text(output_frame, height=8, width=45, wrap="word")
    original_output.grid(row=1, column=0, padx=5, pady=5)

    modified_output = tk.Text(output_frame, height=8, width=45, wrap="word")
    modified_output.grid(row=1, column=1, padx=5, pady=5)

    root.mainloop()

