import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import pandas as pd
import os

# --- OFFICIAL USER REGISTRY ---
USER_DB = {
    "admin": {"role": "Admin"},
    "coord1": {"role": "Regional Coordinator"},
    "sup1": {"role": "Supervisor"},
    "enum1": {"role": "Enumerator"},
    "analyst1": {"role": "Data Analyst"}
}

class KenyaCensusFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("KNBS - National Census Portal v12.5")
        self.root.geometry("1300x850")
        self.root.configure(bg="#0F0F0F")
        
        # Internal Database
        self.records = [
            {"ID": 1, "Name": "James Kamau", "County": "Nairobi", "Type": "S1-Grid", "Status": "Verified"},
            {"ID": 2, "Name": "Sarah Cherono", "County": "Nakuru", "Type": "S1-Grid", "Status": "Verified"}
        ]
        
        self.show_login_screen()

    # --- 1. CENTERED LOGIN SCREEN ---
    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.login_frame = tk.Frame(self.root, bg="#1A1A1A", padx=45, pady=45, highlightbackground="#0DBD8B", highlightthickness=1)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.login_frame, text="KNBS ACCESS PORTAL", fg="#0DBD8B", bg="#1A1A1A", font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(self.login_frame, text="Username:", fg="white", bg="#1A1A1A").pack(anchor="w", pady=(20, 0))
        self.u_ent = tk.Entry(self.login_frame, font=("Arial", 12), width=30, bg="#2A2A2A", fg="white", insertbackground="white")
        self.u_ent.pack(pady=5)
        self.u_ent.insert(0, "admin")

        tk.Label(self.login_frame, text="Password:", fg="white", bg="#1A1A1A").pack(anchor="w", pady=(10, 0))
        self.p_ent = tk.Entry(self.login_frame, show="*", font=("Arial", 12), width=30, bg="#2A2A2A", fg="white")
        self.p_ent.pack(pady=5)

        tk.Button(self.login_frame, text="SECURE LOGIN", bg="#0DBD8B", fg="black", font=("Arial", 10, "bold"), 
                  width=25, pady=12, command=self.authenticate, cursor="hand2").pack(pady=20)

    def authenticate(self):
        u = self.u_ent.get().lower().strip()
        if u in USER_DB:
            self.user_role = USER_DB[u]["role"]
            self.build_main_ui()
        else:
            messagebox.showerror("Access Denied", "Invalid Credentials")

    # --- 2. MAIN INTERFACE & NAVIGATION ---
    def build_main_ui(self):
        for widget in self.root.winfo_children(): widget.destroy()

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg="#1A1A1A", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="KNBS MENU", fg="#0DBD8B", bg="#1A1A1A", font=("Arial", 14, "bold"), pady=20).pack()

        # Nav Links
        self.nav_btn("📊 Dashboard", self.show_dashboard)
        if self.user_role in ["Admin", "Enumerator"]:
            self.nav_btn("📝 Data Entry (Form S1)", self.show_entry)
        if self.user_role in ["Admin", "Supervisor"]:
            self.nav_btn("📋 Supervisor Review", self.show_review)
        if self.user_role in ["Admin", "Data Analyst"]:
            self.nav_btn("📈 Demographics", self.show_demographics)
        if self.user_role == "Admin":
            self.nav_btn("🛡️ System Admin", self.show_admin)

        # LOGOUT (Appears after System Admin)
        tk.Button(self.sidebar, text="🚪 LOGOUT", fg="#FF4444", bg="#1A1A1A", bd=0, padx=20, pady=15, 
                  anchor="w", font=("Arial", 10, "bold"), command=self.show_login_screen, cursor="hand2").pack(fill="x")

        # Main Content Container
        self.main = tk.Frame(self.root, bg="#0F0F0F", padx=30, pady=30)
        self.main.pack(side="right", expand=True, fill="both")
        self.show_dashboard()

    def nav_btn(self, text, cmd):
        tk.Button(self.sidebar, text=text, fg="white", bg="#1A1A1A", bd=0, padx=20, pady=12, 
                  anchor="w", command=cmd, cursor="hand2").pack(fill="x")

    # --- 3. DATA ENTRY (FORM S1 GRID LAYOUT) ---
    def show_entry(self):
        self.clear_main()
        
        # Header Section
        header = tk.Frame(self.main, bg="#0F0F0F")
        header.pack(fill="x")
        tk.Label(header, text="REPUBLIC OF KENYA - 2024 CENSUS", fg="white", bg="#0F0F0F", font=("Arial", 10, "bold")).pack()
        tk.Label(header, text="MAIN QUESTIONNAIRE: INDIVIDUAL PARTICULARS", fg="#0DBD8B", bg="#0F0F0F", font=("Arial", 14, "bold")).pack(pady=5)
        
        # The Grid Frame
        grid_frame = tk.Frame(self.main, bg="#000", highlightbackground="#0DBD8B", highlightthickness=1)
        grid_frame.pack(fill="both", expand=True, pady=10)

        # Form Headers (Column Names)
        headers = [("Line", 5), ("A1: Full Name", 25), ("A2: Relationship", 15), ("A3: Sex", 10), ("A4: Age", 8), ("A5: Status", 12)]
        for i, (text, width) in enumerate(headers):
            tk.Label(grid_frame, text=text, bg="#0DBD8B", fg="black", font=("Arial", 9, "bold"), width=width, relief="solid").grid(row=0, column=i, sticky="nsew")

        self.grid_rows = []
        for r in range(1, 11): # 10-row sheet
            row_data = {}
            tk.Label(grid_frame, text=str(r), bg="#222", fg="white", relief="ridge").grid(row=r, column=0, sticky="nsew")
            
            row_data['n'] = tk.Entry(grid_frame, font=("Arial", 10)); row_data['n'].grid(row=r, column=1, sticky="nsew")
            row_data['r'] = ttk.Combobox(grid_frame, values=["Head", "Spouse", "Child", "Parent", "Other"], width=12); row_data['r'].grid(row=r, column=2, sticky="nsew")
            row_data['s'] = ttk.Combobox(grid_frame, values=["Male", "Female", "Intersex"], width=8); row_data['s'].grid(row=r, column=3, sticky="nsew")
            row_data['a'] = tk.Entry(grid_frame, width=5); row_data['a'].grid(row=r, column=4, sticky="nsew")
            row_data['st'] = tk.Entry(grid_frame, width=10); row_data['st'].grid(row=r, column=5, sticky="nsew"); row_data['st'].insert(0, "Pending")
            
            self.grid_rows.append(row_data)

        # Control Buttons
        btn_area = tk.Frame(self.main, bg="#0F0F0F")
        btn_area.pack(fill="x", pady=20)

        def save_batch():
            count = 0
            for row in self.grid_rows:
                if row['n'].get().strip():
                    self.records.append({
                        "ID": len(self.records)+1, "Name": row['n'].get(), 
                        "County": "Field Entry", "Type": "Form S1", "Status": "Pending"
                    })
                    count += 1
            if count > 0:
                messagebox.showinfo("Sync", f"{count} members added to database."); self.show_dashboard()
            else:
                messagebox.showwarning("Empty", "No data entered in rows.")

        tk.Button(btn_area, text="VALIDATE & SYNC HOUSEHOLD", bg="#0DBD8B", fg="black", font=("Arial", 10, "bold"), padx=20, pady=12, command=save_batch).pack(side="right")

    # --- 4. SYSTEM MODULES ---
    def show_dashboard(self):
        self.clear_main()
        tk.Label(self.main, text=f"System Overview: {self.user_role}", fg="white", bg="#0F0F0F", font=("Arial", 22, "bold")).pack(anchor="w")
        card = tk.Frame(self.main, bg="#1A73E8", width=250, height=120)
        card.pack(pady=20, anchor="w"); card.pack_propagate(False)
        tk.Label(card, text="TOTAL RECORDS", bg="#1A73E8", fg="white").pack(pady=15)
        tk.Label(card, text=str(len(self.records)), bg="#1A73E8", fg="white", font=("Arial", 24, "bold")).pack()

    def show_demographics(self):
        self.clear_main()
        tk.Button(self.main, text="DOWNLOAD FULL EXCEL REPORT", bg="#0DBD8B", font=("Arial", 10, "bold"), pady=15, command=self.export_excel).pack(pady=50)

    def show_review(self):
        self.clear_main()
        t = ttk.Treeview(self.main, columns=("ID", "Name", "Type", "Status"), show="headings")
        for c in ("ID", "Name", "Type", "Status"): t.heading(c, text=c)
        for r in self.records: t.insert("", "end", values=(r["ID"], r["Name"], r["Type"], r["Status"]))
        t.pack(fill="both", expand=True)

    def show_admin(self):
        self.clear_main()
        tk.Label(self.main, text="System Administration", fg="#FF4444", bg="#0F0F0F", font=("Arial", 20)).pack()
        tk.Button(self.main, text="EXPORT MASTER DATABASE", bg="#333", fg="white", pady=15, width=30, command=self.export_excel).pack(pady=20)

    def export_excel(self):
        try:
            df = pd.DataFrame(self.records)
            fname = "Census_Final_Records.xlsx"
            df.to_excel(fname, index=False)
            os.startfile(fname) if os.name == 'nt' else os.system(f'open "{fname}"')
        except Exception as e: messagebox.showerror("Error", str(e))

    def clear_main(self):
        for w in self.main.winfo_children(): w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(); style.theme_use("clam")
    app = KenyaCensusFinal(root)
    root.mainloop()