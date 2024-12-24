import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import numpy as np
import bisect
from itertools import permutations
import pandas as pd
class DNAQueryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Query and Sequence Analyzer")
        self.root.configure(bg="#222222")

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#222222")
        input_frame.pack(padx=20, pady=20)

        tk.Label(input_frame, text="DNA Sequence (FASTA format):", font=("Arial", 14), bg="#222222", fg="#FFFFFF").pack()
        self.dna_sequence = tk.Text(input_frame, height=10, width=60, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.dna_sequence.pack()

        tk.Button(input_frame, text="Upload File", command=self.upload_file, font=("Arial", 12), bg="#4444FF", fg="#FFFFFF").pack(pady=(10,0))

        # Tab Control
        tab_control = ttk.Notebook(self.root)
        tab_control.pack(padx=20, pady=10)

        # Query Tab
        query_tab = tk.Frame(tab_control, bg="#222222")
        tab_control.add(query_tab, text="Query")

        button_frame_query = tk.Frame(query_tab, bg="#222222")
        button_frame_query.pack(pady=10)

        tk.Label(query_tab, text="Pattern:", font=("Arial", 12), bg="#222222", fg="#FFFFFF").pack()
        self.pattern = tk.Entry(query_tab, width=20, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.pattern.pack()

        tk.Label(query_tab, text="Subsequence Length:", font=("Arial", 12), bg="#222222", fg="#FFFFFF").pack()
        self.subsequence_length = tk.Entry(query_tab, width=5, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.subsequence_length.pack()

        tk.Button(button_frame_query, text="Query", command=self.query_dna, font=("Arial", 12), bg="#0044FF", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame_query, text="Reset", command=self.reset_query, font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)

        tk.Label(query_tab, text="Offsets:", font=("Arial", 12), bg="#222222", fg="#FFFFFF").pack()
        self.result_text_query = tk.Text(query_tab, height=5, width=60, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.result_text_query.pack()

        # Analyzer Tab
        analyzer_tab = tk.Frame(tab_control, bg="#222222")
        tab_control.add(analyzer_tab, text="Analyzer Badchars")

        tk.Label(analyzer_tab, text="Substring:", font=("Arial", 12), bg="#222222", fg="#FFFFFF").pack()
        self.substring = tk.Entry(analyzer_tab, width=20, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.substring.pack()

        
        button_frame_analyzer = tk.Frame(analyzer_tab, bg="#222222")
        button_frame_analyzer.pack(pady=10)

        tk.Button(button_frame_analyzer, text="Analyze", command=self.analyze, font=("Arial", 12), bg="#0044FF", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame_analyzer, text="Clear", command=self.clear_analyzer, font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame_analyzer, text="Load File", command=self.load_file, font=("Arial", 12), bg="#4444FF", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=10)

        tk.Label(analyzer_tab, text="Results:", font=("Arial", 12), bg="#222222", fg="#FFFFFF").pack()
        self.result_text_analyzer = tk.Text(analyzer_tab, height=10, width=60, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.result_text_analyzer.pack()



        # Construct Suffix Array Tab
        suffix_array_tab = tk.Frame(tab_control, bg="#222222")
        tab_control.add(suffix_array_tab, text="Construct Suffix Array")

        tk.Label(suffix_array_tab, text="DNA Sequence:", font=("Arial", 14), bg="#222222", fg="#FFFFFF").pack()
        self.suffix_array_sequence = tk.Entry(suffix_array_tab, width=50, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.suffix_array_sequence.pack()

        tk.Button(suffix_array_tab, text="Construct Suffix Array", command=self.construct_suffix_array, font=("Arial", 12), bg="#0044FF", fg="#FFFFFF").pack(pady=(10, 0))

        tk.Label(suffix_array_tab, text="Suffix Array:", font=("Arial", 14), bg="#222222", fg="#FFFFFF").pack()
        self.suffix_array_output = tk.Text(suffix_array_tab, height=10, width=50, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.suffix_array_output.pack()

        # Calculate Overlap Tab
        overlap_tab = tk.Frame(tab_control, bg="#222222")
        tab_control.add(overlap_tab, text="Calculate Overlap")

        tk.Label(overlap_tab, text="Enter DNA Reads (comma-separated):", font=("Arial", 14), bg="#222222", fg="#FFFFFF").pack()
        self.overlap_reads_entry = tk.Entry(overlap_tab, width=50, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.overlap_reads_entry.pack()

        tk.Label(overlap_tab, text="Minimum Overlap Length:", font=("Arial", 14), bg="#222222", fg="#FFFFFF").pack()
        self.overlap_min_length_entry = tk.Entry(overlap_tab, width=5, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.overlap_min_length_entry.pack()

        tk.Button(overlap_tab, text="Calculate Overlap", command=self.calculate_overlap, font=("Arial", 12), bg="#0044FF", fg="#FFFFFF").pack(pady=(10, 0))

        tk.Label(overlap_tab, text="Overlap Results:", font=("Arial", 14), bg="#222222", fg="#FFFFFF").pack()
        self.overlap_output_text = tk.Text(overlap_tab, height=10, width=50, font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.overlap_output_text.pack()

       
    def overlap(self, a, b, min_length):
            start = 0
            while True:
                start = a.find(b[:min_length], start)
                if start == -1:
                    return 0
                if b.startswith(a[start:]):
                    return len(a) - start
                start += 1

    def native_overlap(self, reads, k):
        olap = {}
        for a, b in permutations(reads, 2):
            olen = self.overlap(a, b, k)
            if olen > 0:
                olap[(a, b)] = olen
        return olap

    def calculate_overlap(self):
        reads = self.overlap_reads_entry.get().split(',')
        reads = [r.strip() for r in reads]
        k = int(self.overlap_min_length_entry.get())
        result = self.native_overlap(reads, k)
        self.overlap_output_text.delete(1.0, tk.END)
        for key, value in result.items():
            self.overlap_output_text.insert(tk.END, f"{key}: {value}\n")



    def construct_suffix_array(self):
        sequence = self.suffix_array_sequence.get() + '$'
        dec = {'$': 0, 'A': 1, 'C': 2, 'G': 3, 'T': 4}
        table = []
        i = 2**0
        n = 0

        while True:
            l = []
            dec2 = {}
            if i > 1:
                for j in range(len(sequence)):
                    if sequence[j:j+i] not in l:
                        l.append(sequence[j:j+i])
                l.sort()
                for j in range(len(l)):
                    dec2[tuple(l[j])] = j
            row = []
            for j in range(len(sequence)):
                if i == 1:
                    row.append(dec[sequence[j]])
                else:
                    row.append(dec2[tuple(table[n-1][j:j+i])])
            table.append(row)
            flag = 0
            for j in range(len(row)):
                c = row.count(j)
                if c > 1:
                    flag = 1
                    break
            self.suffix_array_output.insert(tk.END, str(row) + "\n")
            if flag == 0:
                break
            n += 1
            i = 2**n
    def analyze(self):
            seq = self.dna_sequence.get("1.0", tk.END).strip()
            sub_seq = self.substring.get()
            match_result = match(seq, sub_seq)
            badchars_result = Badchars(seq, sub_seq)
            self.result_text_analyzer.delete("1.0", tk.END)
            self.result_text_analyzer.insert(tk.END, f"Match Index: {match_result}\n")
            self.result_text_analyzer.insert(tk.END, f"Badchars Index: {badchars_result}\n")


    def clear_analyzer(self):
        self.dna_sequence.delete("1.0", tk.END)
        self.substring.delete(0, tk.END)
        self.result_text_analyzer.delete("1.0", tk.END)


    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select DNA File", filetypes=[("FASTA Files", "*.fasta")])
        if file_path:
            with open(file_path, 'r') as file:
                seq = file.read().splitlines()[1].strip()
                self.dna_sequence.insert(tk.END, seq)


    def validate_dna(self, sequence):
        valid_chars = set("ATCGatcg")
        return set(sequence).issubset(valid_chars)


    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select DNA Sequence File", 
                                                filetypes=[("FASTA Files", "*.fasta"), 
                                                            ("Text Files", "*.txt")])
        
        if file_path:
            with open(file_path, "r") as file:
                lines = file.readlines()
                dna_sequence = "".join([line.strip() for line in lines[1:]])  
                
                if self.validate_dna(dna_sequence):
                    self.dna_sequence.delete("1.0", tk.END)
                    self.dna_sequence.insert("1.0", dna_sequence)
                else:
                    messagebox.showerror("Invalid DNA Sequence", "Please upload a valid DNA sequence file.")


    def query_dna(self): 
        dna_sequence = self.dna_sequence.get("1.0", tk.END).strip()
        pattern = self.pattern.get()
        subsequence_length = int(self.subsequence_length.get())

        index = index_sorted(dna_sequence, subsequence_length)
        offsets = query(dna_sequence, pattern, index)
        result = "Offsets: " + ", ".join(map(str, offsets))
        self.result_text_query.delete("1.0", tk.END)
        self.result_text_query.insert("1.0", result)


    def reset_query(self):
        self.dna_sequence.delete("1.0", tk.END)
        self.pattern.delete(0, tk.END)
        self.subsequence_length.delete(0, tk.END)
        self.result_text_query.delete("1.0", tk.END)


def index_sorted(seq, ln):
        index = []
        for i in range(len(seq) - ln + 1):
            index.append((seq[i:i+ln], i))
        index.sort()
        return index


def query(t , p, index):
        keys = [r[0] for r in index]
        st = bisect.bisect_left(keys, p[:len(keys[0])])
        en = bisect.bisect(keys, p[:len(keys[0])])
        hits = index[st:en]
        l = [h[1] for h in hits]
        offsets = []
        for i in l:
            if t[i:i+len(p)] == p:
                offsets.append(i)
        return offsets


def match(seq, sub_seq):
        x = -1
        for i in range(len(seq) - len(sub_seq) + 1):
            if sub_seq == seq[i:i + len(sub_seq)]:
                x = i
                break
        return x


def Badchars(seq, sub_seq):
    table = np.zeros([4, len(sub_seq)])
    row = ["A", "C", "G", "T"]
    for i in range(4):
        num = -1
        for j in range(len(sub_seq)):
            if row[i] == sub_seq[j]:
                table[i, j] = -1
                num = -1
            else:
                num += 1
                table[i, j] = num
    x = -1
    i = 0
    while (i < len(seq) - len(sub_seq) + 1):
        if sub_seq == seq[i:i + len(sub_seq)]:
            x = i
        else:
            for j in range(len(sub_seq) - 1, -1, -1):
                if seq[i + j] != sub_seq[j]:
                    k = row.index(seq[i + j])
                    i += int(table[k, j])
                    break
        i += 1
    return x

if __name__ == "__main__":
    root = tk.Tk()
    gui = DNAQueryGUI(root)
    root.mainloop()



#Online or offline?
# Naïve algorithm --> online
# Boyer-Moore --> online
# Web search engine --> offline
# Read alignment --> offline




# seq = "banana"
# ln = 3
# [('ana', 1), ('ana', 3), ('ban', 0), ('nan', 2)]
#