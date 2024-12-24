import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import pyperclip
import csv
from tkinter import ttk 
import pandas as pd
# Utility Functions
def validate_sequence(seq):
    pattern = r'^[ATCG]+$'
    return bool(re.match(pattern, seq.upper()))

def gc_content(seq):
    try:
        seq = seq.upper()
        if not validate_sequence(seq):
            raise ValueError("Invalid DNA sequence, DNA must be include A, T, C, G only")
        if len(seq) == 0:
            return 0
        return (seq.count("G") + seq.count("C")) / len(seq)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def complement(seq):
    try:
        seq = seq.upper()
        if not validate_sequence(seq):
            raise ValueError("Invalid DNA sequence, DNA must be include A, T, C, G only")
        dic = {"G": "C", "C": "G", "A": "T", "T": "A"}
        return "".join(dic[base] for base in seq)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def reverse(seq):
    return seq[::-1] 

def reverse_complement(seq):
    return complement(reverse(seq))

def translation_table(seq):
    try:
        seq = seq.upper()
        if not validate_sequence(seq):
            raise ValueError("Invalid DNA sequence, DNA must be include A, T, C, G only")
        if len(seq) % 3 != 0:
            raise ValueError("Sequence length must be divisible by 3")
        # تحويل إلى أحماض أمينية 
        dic = {
            "TTT": "F", "CTT": "L", "ATT": "I", "GTT": "V",
            "TTC": "F", "CTC": "L", "ATC": "I", "GTC": "V",
            "TTA": "L", "CTA": "L", "ATA": "I", "GTA": "V",
            "TTG": "L", "CTG": "L", "ATG": "M", "GTG": "V",
            "TCT": "S", "CCT": "P", "ACT": "T", "GCT": "A",
            "TCC": "S", "CCC": "P", "ACC": "T", "GCC": "A",
            "TCA": "S", "CCA": "P", "ACA": "T", "GCA": "A",
            "TCG": "S", "CCG": "P", "ACG": "T", "GCG": "A",
            "TAT": "Y", "CAT": "H", "AAT": "N", "GAT": "D",
            "TAC": "Y", "CAC": "H", "AAC": "N", "GAC": "D",
            "TAA": "*", "CAA": "Q", "AAA": "K", "GAA": "E",
            "TAG": "*", "CAG": "Q", "AAG": "K", "GAG": "E",
            "TGT": "C", "CGT": "R", "AGT": "S", "GGT": "G",
            "TGC": "C", "CGC": "R", "AGC": "S", "GGC": "G",
            "TGA": "*", "CGA": "R", "AGA": "R", "GGA": "G",
            "TGG": "W", "CGG": "R", "AGG": "R", "GGG": "G"
        }
        protein_seq = ""
        for i in range(0, len(seq), 3):
            protein_seq += dic[seq[i:i + 3]]
        return protein_seq
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# DNA Sequence Analyzer GUI
class DNASequenceAnalyzer:
    def __init__(self, frame):
        self.frame = frame
        self.result_history = []
        self.background_color = "#222222"
        self.frame.configure(bg=self.background_color)

        self.header_label = tk.Label(self.frame, text="DNA Sequence Analyzer", font=("Arial", 24, "bold"), bg=self.background_color, fg="#00FF00")
        self.header_label.pack(pady=20)

        self.input_frame = tk.Frame(self.frame, bg=self.background_color)
        self.input_frame.pack(padx=20, pady=20)

        tk.Label(self.input_frame, text="DNA Sequence:", font=("Arial", 14), bg=self.background_color, fg="#FFFFFF").pack(side=tk.LEFT)
        self.dna_sequence = tk.Entry(self.input_frame, width=50, font=("Arial", 14), bg="#333333", fg="#FFFFFF")
        self.dna_sequence.pack(side=tk.LEFT)

        # Buttons
        self.button_frame1 = tk.Frame(self.frame, bg=self.background_color)
        self.button_frame1.pack(padx=20, pady=10)
        tk.Button(self.button_frame1, text="Calculate GC Content", command=self.calculate_gc_content, font=("Arial", 12), bg="#0044FF", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame1, text="Calculate Reverse Complement", command=self.calculate_reverse_complement, font=("Arial", 12), bg="#FF4400", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)

        self.button_frame2 = tk.Frame(self.frame, bg=self.background_color)
        self.button_frame2.pack(padx=20, pady=10)
        tk.Button(self.button_frame2, text="Calculate Translation Table", command=self.calculate_translation_table, font=("Arial", 12), bg="#00FF44", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame2, text="Reset", command=self.reset, font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame2, text="Copy Result", command=self.copy_result, font=("Arial", 12), bg="#4444FF", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame2, text="Help/About", command=self.help_about, font=("Arial", 12), bg="#44FF44", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame2, text="Select File", command=self.select_file, font=("Arial", 12), bg="#4444FF", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)

        # Result Frame
        self.result_frame = tk.Frame(self.frame, bg=self.background_color)
        self.result_frame.pack(padx=20, pady=20)
        self.result_label = tk.Label(self.result_frame, text="Result:", font=("Arial", 14), bg=self.background_color, fg="#00FF00")
        self.result_label.pack()
        self.result_text = tk.Text(self.result_frame, height=10, width=60, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.result_text.pack()

        # Result History Frame
        self.history_frame = tk.Frame(self.frame, bg=self.background_color)
        self.history_frame.pack(padx=20, pady=20)
        self.history_label = tk.Label(self.history_frame, text="Result History:", font=("Arial", 14), bg=self.background_color, fg="#00FF00")
        self.history_label.pack()
        self.history_text = tk.Text(self.history_frame, height=10, width=60, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.history_text.pack()
        tk.Button(self.button_frame2, text="Reset History", command=self.reset_History, font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        
        # Animation
        self.animate()
    def animate(self):
        self.header_label.config(fg="#FF0000" if self.header_label.cget("fg") == "#00FF00" else "#00FF00")
        self.frame.after(2000, self.animate)
    def reset(self):
            self.dna_sequence.delete(0, tk.END)
            self.result_text.delete(1.0, tk.END)

    def reset_History(self):
            self.history_text.delete(1.0, tk.END)
            self.result_history = []    
    def copy_result(self):
        result = self.result_text.get("1.0", tk.END)
        pyperclip.copy(result)
        messagebox.showinfo('Copied successfully', result)

    def help_about(self):
        messagebox.showinfo("Help/About", "DNA Sequence Analyzer\nVersion 1.0\nDeveloped by Mohamed Amr")
        
    def calculate_gc_content(self):
        seq = self.dna_sequence.get()
        if validate_sequence(seq):
            gc_content_result = gc_content(seq)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"GC Content: {gc_content_result}")
            self.result_history.append(f"GC Content: {gc_content_result}")
            self.history_text.insert(tk.END, f"GC Content: {gc_content_result}\n")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Invalid DNA sequence, DNA must be include A, T, C, G only")

    def calculate_reverse_complement(self):
        seq = self.dna_sequence.get()
        if validate_sequence(seq):
            reverse_complement_result = reverse_complement(seq)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Reverse Complement: {reverse_complement_result}")
            self.result_history.append(f"Reverse Complement: {reverse_complement_result}")
            self.history_text.insert(tk.END, f"Reverse Complement: {reverse_complement_result}\n")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Invalid DNA sequence, DNA must be include A, T, C, G only")

    def calculate_translation_table(self):
        seq = self.dna_sequence.get()
        if validate_sequence(seq):
            translation_table_result = translation_table(seq)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Translation Table: {translation_table_result}")
            self.result_history.append(f"Translation Table: {translation_table_result}")
            self.history_text.insert(tk.END, f"Translation Table: {translation_table_result}\n")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Invalid DNA sequence, DNA must be include A, T, C, G only")
    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select DNA File", filetypes=[("FASTA Files", "*.fasta")])
        if file_path:
            self.dna_sequence.delete(0, tk.END)
            self.dna_sequence.insert(tk.END, file_path)
            self.read_fasta_file(file_path) 

    def read_fasta_file(self, file_path):
        with open(file_path, 'r') as file:
            seq = ''
            for line in file:
                if not line.startswith('>'):
                    seq += line.strip()
    
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        # Display current file results
        self.display_results(seq)
        
        # Add previous results to history
        # self.history_text.insert(tk.END, self.result_history[-1] + "\n\n")
        
        # Update result history
        if self.result_history:  # Check if list is not empty
            self.history_text.insert(tk.END, self.result_history[-1] + "\n\n")
        else:
            print("History is empty.")
        # Optional: Handle the case when history is empty
    def display_results(self, seq):
        self.result_text.insert(tk.END, f"Sequence:\n\n{seq}\n\n")
        gc_content_result = gc_content(seq)
        self.result_text.insert(tk.END, f"----------------------------------------\n")
        self.result_text.insert(tk.END, f"GC Content: {gc_content_result}\n\n")
        reverse_complement_result = reverse_complement(seq)
        self.result_text.insert(tk.END, f"----------------------------------------\n")
        self.result_text.insert(tk.END, f"Reverse Complement:\n\n{reverse_complement_result}\n\n")
        translation_table_result = translation_table(seq)
        self.result_text.insert(tk.END, f"----------------------------------------\n")
        self.result_text.insert(tk.END, f"Translation Table:\n\n{translation_table_result}\n")
    def calculate_gc_content_from_file(self, seq):
        gc_content_result = gc_content(seq)
        self.result_text.insert(tk.END, f"GC Content: {gc_content_result}\n")

    def calculate_reverse_complement_from_file(self, seq):
        reverse_complement_result = reverse_complement(seq)
        self.result_text.insert(tk.END, f"Reverse Complement: {reverse_complement_result}\n")

    def calculate_translation_table_from_file(self, seq):
        translation_table_result = translation_table(seq)
        self.result_text.insert(tk.END, f"Translation Table: {translation_table_result}\n")              
# Fasta to CSV Converter GUI
# Section 2 


class FastaToCSVConverter:
    def __init__(self, frame):
        
        self.frame = frame
        # self.root.title("FASTA to CSV Converter")
        self.frame.configure(bg="#222222")

        # Input Frame
        input_frame = tk.Frame(self.frame, bg="#222222")
        input_frame.pack(padx=20, pady=20)

        tk.Label(input_frame, text="Select FASTA File:", font=("Arial", 14), bg="#222222", fg="#FFFFFF").pack()
        self.file_path_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.file_path_entry.pack()
        tk.Button(input_frame, text="Browse", command=self.browse_file, font=("Arial", 12), bg="#0044FF", fg="#FFFFFF").pack(pady=(10, 0))

        # Output Frame
        output_frame = tk.Frame(self.frame, bg="#222222")
        output_frame.pack(padx=20, pady=20)

        tk.Label(output_frame, text="Output CSV File:", font=("Arial", 14), bg="#222222", fg="#FFFFFF").pack()
        self.output_path_entry = tk.Entry(output_frame, width=50, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.output_path_entry.pack()

        # Convert Button
        tk.Button(output_frame, text="Convert to CSV", command=self.convert_fasta_to_csv, font=("Arial", 12), bg="#0044FF", fg="#FFFFFF").pack(pady=(10, 0))

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select FASTA File", filetypes=[("FASTA Files", "*.fasta")])
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(tk.END, file_path)

    def convert_fasta_to_csv(self):
        file_path = self.file_path_entry.get()
        output_path = self.output_path_entry.get()
        if not file_path or not output_path:
            messagebox.showerror("Error", "Please select input and output files")
            return

        tb = []
        with open(file_path, 'r') as infile:
            flag = 0
            s = []
            for line in infile:
                if flag == 0:
                    s = line.split("|lcl|")
                    flag = 1
                else:
                    if len(s) > 3 and (s[3] == 'non-hemolytic' or s[3] == 'non-hemolytic\n'):
                        tb.append([line[:-1], 0])
                    elif len(s) > 3:
                        tb.append([line[:-1], 1])
                    flag = 0

        head = ['Sequence', 'y']
        df = pd.DataFrame(tb, columns=head)
        df.to_csv(output_path, index=False)
        messagebox.showinfo("Success", "Conversion completed successfully")


# Main Application
class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Sequence Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#222222")

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Home Tab (DNA Sequence Analyzer)
        self.home_tab = tk.Frame(self.notebook)
        self.notebook.add(self.home_tab, text="Home")
        DNASequenceAnalyzer(self.home_tab)

        # Fasta to CSV Converter Tab
        self.fasta_converter_tab = tk.Frame(self.notebook)
        self.notebook.add(self.fasta_converter_tab, text="Fasta to CSV Converter")
        FastaToCSVConverter(self.fasta_converter_tab)

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()    
