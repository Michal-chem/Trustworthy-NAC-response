import numpy as np
from scipy.stats import norm
import statsmodels.api as sm
import tkinter as tk
from tkinter import ttk, messagebox

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()


class StatisticalCalculator:
    def approximate_R2(self, auc, prevalence, S, N, n=1000000):
        mu = np.sqrt(2) * norm.ppf(auc)
        non_events = np.random.normal(loc=0, scale=1, size=int(prevalence * n))
        events = np.random.normal(loc=mu, scale=1, size=int((1 - prevalence) * n))
        LP = np.concatenate([non_events, events])
        y = np.concatenate([np.zeros(int(prevalence * n)), np.ones(int((1 - prevalence) * n))])
        LP = sm.add_constant(LP)
        model = sm.Logit(y, LP).fit(disp=0)
        sam_size = N / ((S - 1) * np.log(1 - (model.prsquared / S)))
        return sam_size

    def epv_calc(self, epv, prevalence, n):
        return (epv * n) / prevalence

    def calculate_prevalence(self, positive_cases, total_cases):
        return positive_cases / total_cases if total_cases else 0


def show_result(message):
    messagebox.showinfo("Result", message)


def calculate_R2():
    try:
        auc = float(auc_entry.get())
        prevalence = float(prevalence_entry.get())
        S = float(S_entry.get())
        N = float(N_entry.get())

        result = StatisticalCalculator().approximate_R2(auc, prevalence, S, N)
        show_result(f"Calculated Sample Size: {result:.4f}")
    except ValueError as ve:
        messagebox.showerror("Input Error", "Please fill in all fields correctly. Ensure all fields contain valid numeric values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def calculate_prevalence():
    try:
        positive_cases = int(positive_cases_entry.get())
        total_cases = int(total_cases_entry.get())
        prevalence = StatisticalCalculator().calculate_prevalence(positive_cases, total_cases)
        prevalence_entry.delete(0, tk.END)
        prevalence_entry.insert(0, f"{prevalence:.4f}")
        prevalence_epv_entry.delete(0, tk.END)
        prevalence_epv_entry.insert(0, f"{prevalence:.4f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def calculate_epv():
    try:
        epv = float(epv_entry.get())
        prevalence = float(prevalence_epv_entry.get())
        n = float(n_entry_epv.get())
        
        result = StatisticalCalculator().epv_calc(epv, prevalence, n)
        show_result(f"Calculated Sample Size: {result:.4f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please fill in all fields correctly. Ensure all fields contain valid numeric values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
root = tk.Tk()
root.title("Sample Size Assessment")

# Prevalence Calculation Frame
frame_prevalence = ttk.LabelFrame(root, text="Prevalence Calculation")
frame_prevalence.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

positive_cases_label = ttk.Label(frame_prevalence, text="Positive Cases:")
positive_cases_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
positive_cases_entry = ttk.Entry(frame_prevalence)
positive_cases_entry.grid(row=0, column=1, padx=5, pady=5)
ToolTip(positive_cases_entry, "Enter the number of positive cases (e.g. patients with the disease).")

total_cases_label = ttk.Label(frame_prevalence, text="Total Cases:")
total_cases_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
total_cases_entry = ttk.Entry(frame_prevalence)
total_cases_entry.grid(row=1, column=1, padx=5, pady=5)
ToolTip(total_cases_entry, "Enter the total number of cases (e.g. all patients).")

ttk.Button(frame_prevalence, text="Calculate Prevalence", command=calculate_prevalence).grid(row=2, column=0, columnspan=2, pady=10)

# Cox-Snell based sample size calculation Frame
frame_R2 = ttk.LabelFrame(root, text="Calculate Sample Size Based on Cox-Snell residuals")
frame_R2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

auc_label = ttk.Label(frame_R2, text="AUC:")
auc_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
auc_entry = ttk.Entry(frame_R2)
auc_entry.grid(row=0, column=1, padx=5, pady=5)
ToolTip(auc_entry, "Enter the Area Under the Curve (AUC) value (between 0 and 1).")

prevalence_label = ttk.Label(frame_R2, text="Prevalence:")
prevalence_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
prevalence_entry = ttk.Entry(frame_R2)
prevalence_entry.grid(row=1, column=1, padx=5, pady=5)
ToolTip(prevalence_entry, "The prevalence of the condition (positive cases/total cases).")

S_label = ttk.Label(frame_R2, text="Shrinkage Factor:")
S_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
S_entry = ttk.Entry(frame_R2)
S_entry.grid(row=2, column=1, padx=5, pady=5)
ToolTip(S_entry, "Enter the Shrinkage Factor (e.g. 0.9).")

N_label = ttk.Label(frame_R2, text="Number of features:")
N_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
N_entry = ttk.Entry(frame_R2)
N_entry.grid(row=3, column=1, padx=5, pady=5)
ToolTip(N_entry, "Enter the number of features used for training.")

ttk.Button(frame_R2, text="Calculate Sample Size", command=calculate_R2).grid(row=4, column=0, columnspan=2, pady=10)

# EPV Calculation Frame
frame_epv = ttk.LabelFrame(root, text="EPV Calculation")
frame_epv.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

epv_label = ttk.Label(frame_epv, text="EPV:")
epv_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
epv_entry = ttk.Entry(frame_epv)
epv_entry.grid(row=0, column=1, padx=5, pady=5)
ToolTip(epv_entry, "Enter the umber of Events per Variable (EPV).")

prevalence_epv_label = ttk.Label(frame_epv, text="Prevalence:")
prevalence_epv_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
prevalence_epv_entry = ttk.Entry(frame_epv)
prevalence_epv_entry.grid(row=1, column=1, padx=5, pady=5)
ToolTip(prevalence_epv_entry, "Prevalence of the condition (positive cases/total cases).")

n_label_epv = ttk.Label(frame_epv, text="Number of features:")
n_label_epv.grid(row=2, column=0, padx=5, pady=5, sticky="e")
n_entry_epv = ttk.Entry(frame_epv)
n_entry_epv.grid(row=2, column=1, padx=5, pady=5)
ToolTip(n_entry_epv, "Enter the number of features used for training.")

ttk.Button(frame_epv, text="Calculate Sample Size", command=calculate_epv).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
