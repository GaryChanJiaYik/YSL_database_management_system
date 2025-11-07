import customtkinter as ctk
import pandas as pd
import csv
import json
from datetime import datetime
from Components.datePickerModal import DatePickerModal
from Constant.appConstant import DB_PATH

class ViewSalesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.csv_path = DB_PATH["TREATMENT"]
        
        # --- Title ---
        ctk.CTkLabel(
            self,
            text="Sales Details",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # --- Date Range Frame ---
        date_frame = ctk.CTkFrame(self)
        date_frame.pack(pady=10)
        
        self.from_date_value = ctk.StringVar(value="")
        self.to_date_value = ctk.StringVar(value="")
        
        # FROM
        ctk.CTkLabel(date_frame, text="From:").grid(row=0, column=0, padx=(10,5))
        from_entry = ctk.CTkEntry(date_frame, textvariable=self.from_date_value, width=120)
        from_entry.grid(row=0, column=1)
        from_entry.bind("<Button-1>", lambda e: self.openDatePicker(self.from_date_value))
        
        # Spacer
        ctk.CTkLabel(date_frame, text=" ").grid(row=0, column=2, padx=10)
        
        # TO
        ctk.CTkLabel(date_frame, text="To:").grid(row=0, column=3, padx=(10,5))
        to_entry = ctk.CTkEntry(date_frame, textvariable=self.to_date_value, width=120)
        to_entry.grid(row=0, column=4)
        to_entry.bind("<Button-1>", lambda e: self.openDatePicker(self.to_date_value))
        
        # --- View Button ---
        ctk.CTkButton(self, text="View Sales", command=self.filter_sales_by_date).pack(pady=(20,10))
        
        # --- Warning Label ---
        self.desc_warning_label = ctk.CTkLabel(
            self,
            text="Invalid date range",
            text_color="red",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.desc_warning_label.pack()
        self.desc_warning_label.pack_forget()
        
        # --- Receipt Frame ---
        self.receipt_frame = ctk.CTkFrame(self)
        self.receipt_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.receipt_frame.pack_forget()  # Hide initially
        
        # --- Load CSV once during init ---
        self.load_data()
    
    
    # --- Robust CSV loader with treatmentCost parsing ---
    def load_data(self):
        rows = []
        try:
            with open(self.csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, quotechar='"')
                for row in reader:
                    expected_cols = [
                        'conditionId','treatmentId','treatmentDescription',
                        'treatmentPainLevel','treatmentTenseLevel','treatmentSoreLevel',
                        'treatmentNumbLevel','treatmentDate','treatmentCost',
                        'version','amendmentDate'
                    ]
                    clean_row = {col: row.get(col, '') for col in expected_cols}

                    # --- Parse treatmentCost ---
                    cost_raw = str(clean_row.get('treatmentCost','')).strip()
                    if cost_raw.startswith('{') and cost_raw.endswith('}'):
                        try:
                            clean_row['treatmentCostParsed'] = json.loads(cost_raw.replace('""','"'))
                        except:
                            clean_row['treatmentCostParsed'] = {"Cash": 0.0}
                    else:
                        try:
                            clean_row['treatmentCostParsed'] = {"Cash": float(cost_raw)}
                        except:
                            clean_row['treatmentCostParsed'] = {"Cash": 0.0}

                    rows.append(clean_row)

            self.df = pd.DataFrame(rows)
            # Ensure treatmentDate is datetime
            self.df['treatmentDate'] = pd.to_datetime(self.df['treatmentDate'], errors='coerce')

        except Exception as e:
            print(f"Error loading CSV: {e}")
            self.df = pd.DataFrame()

    
    # --- Open date picker modal ---
    def openDatePicker(self, date_var):
        DatePickerModal.open_date_picker(
            parent=self,
            current_date_str=date_var.get() or "",
            on_selected=lambda date_str: date_var.set(date_str)
        )
    
    
    # --- Filter sales by date range ---
    def filter_sales_by_date(self):
        from_date_str = self.from_date_value.get().strip()
        to_date_str = self.to_date_value.get().strip()
        self.desc_warning_label.pack_forget()
        self.receipt_frame.pack_forget()  # Hide receipt initially

        # Validation
        if not from_date_str or not to_date_str:
            self.show_warning("Please select both From and To dates.")
            return
        try:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
        except ValueError:
            self.show_warning("Invalid date format. Use YYYY-MM-DD.")
            return
        if from_date > to_date:
            self.show_warning("'From' date cannot be later than 'To' date.")
            return

        # Filter
        try:
            self.df['treatmentDate'] = pd.to_datetime(self.df['treatmentDate'], errors='coerce').dt.date
            df_filtered = self.df[
                (self.df['treatmentDate'] >= from_date.date()) &
                (self.df['treatmentDate'] <= to_date.date())
            ]
        except Exception as e:
            self.show_warning(f"Error filtering data: {e}")
            return

        if df_filtered.empty:
            self.show_warning("No sales found for selected date range.")
        else:
            self.display_sales(df_filtered)
            self.receipt_frame.pack(fill="both", expand=True, padx=20, pady=10)  # Show results


    
    # --- Warning message ---
    def show_warning(self, message):
        self.desc_warning_label.configure(text=message)
        self.desc_warning_label.pack(pady=(0,10))
    
    
    # --- Format treatmentCost for display ---
    def format_treatment_cost(self, cost):
        if not cost or cost.lower() == "nan":
            return "0.00"
        cost = str(cost).strip()
        if cost.startswith('{') and cost.endswith('}'):
            try:
                d = json.loads(cost.replace('""','"'))
                parts = [f"{float(v):.2f} ({k})" for k,v in d.items()]
                return ", ".join(parts)
            except:
                return "0.00"
        else:
            try:
                return f"{float(cost):.2f} (Cash)"
            except:
                return "0.00"
    
    # --- Display sales receipt ---
    def display_sales(self, df_filtered):
        # Clear previous
        for widget in self.receipt_frame.winfo_children():
            widget.destroy()
        
        total_price = 0.0
        
        for _, row in df_filtered.iterrows():
            desc = row.get('treatmentDescription','')
            price_str = self.format_treatment_cost(row.get('treatmentCost','0'))
            
            # Calculate numeric total
            try:
                cost_val = row.get('treatmentCost','0')
                if cost_val.startswith('{'):
                    d = json.loads(cost_val.replace('""','"'))
                    row_total = sum(d.values())
                else:
                    row_total = float(cost_val)
            except:
                row_total = 0
            total_price += row_total
            
            row_frame = ctk.CTkFrame(self.receipt_frame)
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row_frame, text=desc, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=price_str, anchor="e").pack(side="right", padx=10)
        
        # Total row
        total_frame = ctk.CTkFrame(self.receipt_frame)
        total_frame.pack(fill="x", pady=(10,0))
        ctk.CTkLabel(total_frame, text="Total:", anchor="w", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10)
        ctk.CTkLabel(total_frame, text=f"RM {total_price:.2f}", anchor="e", font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", padx=10)
