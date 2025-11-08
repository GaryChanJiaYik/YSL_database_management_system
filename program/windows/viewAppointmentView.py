import customtkinter as ctk
import pandas as pd
import csv, json
from Constant.appConstant import DB_PATH, WINDOW_CUSTOMER_DETAIL


class ViewAppointmentView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Title ---
        ctk.CTkLabel(
            self,
            text="Appointment Details",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(20, 10))

        # --- Scrollable Table ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=400)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Load and display data
        self.load_and_display_data()
    

    # ✅ Custom safe loader for treatmentDb.csv
    def load_treatment_data(self, path):
        """Safely load malformed treatmentDb.csv"""
        rows = []
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, quotechar='"')
                expected_cols = [
                    'conditionId', 'treatmentId', 'treatmentDescription',
                    'treatmentPainLevel', 'treatmentTenseLevel', 'treatmentSoreLevel',
                    'treatmentNumbLevel', 'treatmentDate', 'treatmentCost',
                    'version', 'amendmentDate'
                ]

                for row in reader:
                    clean_row = {col: row.get(col, '') for col in expected_cols}

                    # --- Parse treatmentCost safely ---
                    cost_raw = str(clean_row.get('treatmentCost', '')).strip()
                    if cost_raw.startswith('{') and cost_raw.endswith('}'):
                        try:
                            clean_row['treatmentCostParsed'] = json.loads(cost_raw.replace('""', '"'))
                        except Exception:
                            clean_row['treatmentCostParsed'] = {"Cash": 0.0}
                    else:
                        try:
                            clean_row['treatmentCostParsed'] = {"Cash": float(cost_raw)}
                        except Exception:
                            clean_row['treatmentCostParsed'] = {"Cash": 0.0}

                    rows.append(clean_row)

            df = pd.DataFrame(rows)
            df['treatmentDate'] = pd.to_datetime(df['treatmentDate'], errors='coerce')
            return df

        except Exception as e:
            print(f"⚠️ Error loading treatmentDb.csv safely: {e}")
            return pd.DataFrame(columns=[
                'conditionId', 'treatmentId', 'treatmentDescription',
                'treatmentPainLevel', 'treatmentTenseLevel', 'treatmentSoreLevel',
                'treatmentNumbLevel', 'treatmentDate', 'treatmentCost',
                'version', 'amendmentDate'
            ])


    def load_and_display_data(self):
        """Load all CSVs and display combined appointments with fixed width, wrapped text, and clickable rows."""
        try:
            # --- Load CSVs ---
            treatment2_df = pd.read_csv(DB_PATH["TREATMENT2"])
            treatment_df = self.load_treatment_data(DB_PATH["TREATMENT"])
            condition_df = pd.read_csv(DB_PATH["CONDITION"])
            customer_df = pd.read_csv(DB_PATH["MAIN"])

            # Clean up column names
            for df in [treatment2_df, treatment_df, condition_df, customer_df]:
                df.columns = df.columns.str.strip()

            # --- Generate CustomerID from Timestamp ---
            customer_df["CustomerID"] = (
                customer_df["Timestamp"]
                .astype(str)
                .str.replace(r"[^\d]", "", regex=True)
            )

            # --- Ensure all IDs are strings ---
            for df in [treatment_df, treatment2_df, condition_df, customer_df]:
                for col in [c for c in df.columns if "Id" in c or "ID" in c]:
                    df[col] = df[col].astype(str)

            # --- Merge DataFrames ---
            merged = pd.merge(
                treatment2_df,
                treatment_df[["treatmentId", "treatmentDescription"]],
                how="left",
                on="treatmentId",
            )
            merged = pd.merge(merged, condition_df, how="left", on="conditionId")
            merged = pd.merge(
                merged,
                customer_df,
                how="left",
                left_on="customerId",
                right_on="CustomerID",
            )

            # --- Prepare display data ---
            display_df = merged[
                ["customerId", "IC身份证", "Name名", "HP No.手机号", "treatmentDescription", "appointmentDate"]
            ].rename(
                columns={
                    "IC身份证": "IC",
                    "Name名": "Name",
                    "HP No.手机号": "Contact Number",
                    "treatmentDescription": "Treatment Description",
                    "appointmentDate": "Appointment Date",
                }
            )

            # --- Clear scroll frame ---
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()

            col_widths = [160, 180, 160, 250, 180]

            # --- Header Row ---
            header_frame = ctk.CTkFrame(self.scroll_frame)
            header_frame.pack(fill="x", padx=5, pady=2)

            for i, col_name in enumerate(display_df.columns[1:]):  # Skip customerId
                ctk.CTkLabel(
                    header_frame,
                    text=col_name,
                    font=ctk.CTkFont(size=15, weight="bold"),
                    width=col_widths[i],
                    anchor="center",
                    wraplength=col_widths[i]
                ).grid(row=0, column=i, padx=5, pady=5, sticky="ew")

            # --- Track selection ---
            self.selected_row = None

            # --- Data Rows (Clickable) ---
            for i, (_, row) in enumerate(display_df.iterrows()):
                customer_id = row["customerId"]
                bg_color = "#1E1E1E" if i % 2 == 0 else "#242424"

                row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color)
                row_frame.pack(fill="x", padx=5, pady=1)

                # Make the entire row clickable
                row_frame.bind("<Button-1>", lambda e, cid=customer_id, r=i: self.on_row_click(cid, r))

                for j, val in enumerate(row.values[1:]):  # Skip customerId
                    lbl = ctk.CTkLabel(
                        row_frame,
                        text=str(val) if pd.notna(val) else "",
                        width=col_widths[j],
                        anchor="center",
                        wraplength=col_widths[j],
                        justify="center"
                    )
                    lbl.grid(row=0, column=j, padx=5, pady=5, sticky="ew")

                    # Make each label clickable too
                    lbl.bind("<Button-1>", lambda e, cid=customer_id, r=i: self.on_row_click(cid, r))

        except Exception as e:
            print("❌ Error loading appointment data:", e)


    # --- New function for click handling ---
    def on_row_click(self, customer_id, row_index):
        """Handle row click: highlight + navigate to customer detail."""
        print(f"✅ Clicked customer: {customer_id}")

        # Highlight row
        for i, frame in enumerate(self.scroll_frame.winfo_children()[1:]):  # Skip header
            color = "#1E1E1E" if i % 2 == 0 else "#242424"
            frame.configure(fg_color=color)
        clicked_row = self.scroll_frame.winfo_children()[row_index + 1]
        clicked_row.configure(fg_color="#2D6CDF")

        # Example redirect:
        self.controller.setCustomerID(customer_id)
        self.controller.switch_frame(WINDOW_CUSTOMER_DETAIL)




