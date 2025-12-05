import customtkinter as ctk
import pandas as pd
import csv
from tkinter import filedialog
from Constant.appConstant import DB_PATH, COLOR
from Components.popupModal import renderPopUpModal
from services.reportGenerateServices import generateAppointmentPdf


class ViewAppointmentView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        # ---- STATE ----
        self.selection_mode = False        # export mode enabled?
        self.selected_cards = {}           # {appointment_id: True/False}
        self.group_card_map = {}           # {date: [checkbox widgets]}

        # --- Title ---
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(20, 10), padx=20)

        ctk.CTkLabel(
            title_frame,
            text="Appointment Details",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(side="left")

        # --- Export button ---
        self.export_btn = ctk.CTkButton(
            title_frame,
            text="Export",
            command=self.toggle_selection_mode,
            width=130
        )
        self.export_btn.pack(side="right")

        # Extra buttons (hidden initially)
        self.export_pdf_btn = ctk.CTkButton(
            title_frame, text="Export as PDF", command=self.export_pdf, width=150,
            fg_color=COLOR["PURPLE"], hover_color=COLOR["HOVER"],
        )
        self.copy_btn = ctk.CTkButton(
            title_frame, text="Copy", command=self.copy_selection, width=130,
            fg_color=COLOR["GREEN"], hover_color=COLOR["HOVER"],        # slightly lighter green on hover
        )
        self.cancel_btn = ctk.CTkButton(
            title_frame, text="Cancel", command=self.toggle_selection_mode, width=130
        )

        # --- Scroll area ---
        self.scroll_area = ctk.CTkFrame(self, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_and_display_data()


    # -------------------------------------------------------------
    # SELECTION MODE TOGGLE
    # -------------------------------------------------------------
    def toggle_selection_mode(self):
        """Enters or exits selection mode (checkbox mode)."""
        self.selection_mode = not self.selection_mode
        self.selected_cards.clear()

        # Update button layout
        if self.selection_mode:
            self.export_btn.pack_forget()
            self.cancel_btn.pack(side="right")
            self.copy_btn.pack(side="right", padx=5)
            self.export_pdf_btn.pack(side="right", padx=5)
        else:
            self.cancel_btn.pack_forget()
            self.copy_btn.pack_forget()
            self.export_pdf_btn.pack_forget()
            self.export_btn.pack(side="right")

        # Reload UI with checkboxes
        self.load_and_display_data()


    # -------------------------------------------------------------
    # LOAD & DISPLAY DATA
    # -------------------------------------------------------------
    def load_and_display_data(self):
        """Load appointment data and rebuild UI."""
        try:
            # --- Load CSVs ---
            treatment2_df = pd.read_csv(DB_PATH["TREATMENT2"])
            treatment_df = self.load_treatment_data(DB_PATH["TREATMENT"])
            condition_df = pd.read_csv(DB_PATH["CONDITION"])
            customer_df = pd.read_csv(DB_PATH["MAIN"])

            for df in [treatment2_df, treatment_df, condition_df, customer_df]:
                df.columns = df.columns.str.strip()

            customer_df["CustomerID"] = (
                customer_df["Timestamp"].astype(str).str.replace(r"[^\d]", "", regex=True)
            )

            for df in [treatment2_df, treatment_df, condition_df, customer_df]:
                for col in df.columns:
                    if "Id" in col or "ID" in col:
                        df[col] = df[col].astype(str)

            # --- Merge data ---
            merged = pd.merge(
                treatment2_df,
                treatment_df[["treatmentId", "treatmentDescription", "conditionId"]],
                on="treatmentId",
                how="left",
            )
            
            merged = merged.rename(columns={
                "conditionId_x": "conditionId",
                "conditionId_y": "conditionId_treat",
            })

            merged = pd.merge(
                merged,
                condition_df[["customerId", "conditionId", "conditionDescription"]],
                on="conditionId",
                how="left",
            )

            merged = pd.merge(
                merged,
                customer_df,
                left_on="customerId",
                right_on="CustomerID",
                how="left",
            )

            display_df = merged[[
                "Old Customer ID", "customerId", "Name名", "HP No.手机号",
                "conditionDescription", "treatmentDescription", "appointmentDate"
            ]].rename(columns={
                "Name名": "Name",
                "HP No.手机号": "Contact Number",
                "conditionDescription": "Condition",
                "treatmentDescription": "Treatment",
                "appointmentDate": "Appointment",
            })

            display_df["Appointment"] = pd.to_datetime(display_df["Appointment"], errors="coerce")
            display_df["Date"] = display_df["Appointment"].dt.date
            display_df["Time"] = display_df["Appointment"].dt.strftime("%I:%M %p")
            display_df = display_df.sort_values(by="Appointment", ascending=False)

            grouped = display_df.sort_values("Date", ascending=False).groupby("Date")

            # --- Reset UI ---
            for w in self.scroll_area.winfo_children():
                w.destroy()

            self.expanded_sections = {}
            self.group_card_map.clear()

            # -------------------------------------------------------------
            # BUILD UI PER DATE GROUP
            # -------------------------------------------------------------
            for date, group in grouped:
                day_frame = ctk.CTkFrame(self.scroll_area)
                day_frame.pack(fill="x", pady=(5, 2))

                # ---------------- HEADER ----------------
                header = ctk.CTkFrame(day_frame, fg_color="#2F2F2F", height=40)
                header.pack(fill="x")

                arrow_label = ctk.CTkLabel(header, text="▶", width=20, font=ctk.CTkFont(size=16))
                arrow_label.pack(side="left", padx=(10, 5))

                date_label = ctk.CTkLabel(
                    header,
                    text=f"{date}   ({len(group)} appointments)",
                    font=ctk.CTkFont(size=16, weight="bold"),
                )
                date_label.pack(side="left", pady=5)

                # ---- SELECT ALL (only in selection mode) ----
                if self.selection_mode:
                    select_all_btn = ctk.CTkButton(
                        header,
                        text="Select All",
                        width=90,
                        height=28,
                        command=lambda d=date: self.select_all_in_group(d),
                    )
                    select_all_btn.pack(side="right", padx=10)
                else:
                    select_all_btn = None

                # EXPANDABLE FRAME
                content_frame = ctk.CTkFrame(day_frame, fg_color="transparent")
                content_frame.pack(fill="x", padx=20)
                content_frame.pack_forget()

                self.expanded_sections[date] = (arrow_label, content_frame)

                header.bind("<Button-1>", lambda e, d=date: self.toggle_section(d))
                arrow_label.bind("<Button-1>", lambda e, d=date: self.toggle_section(d))
                date_label.bind("<Button-1>", lambda e, d=date: self.toggle_section(d))

                # Track checkboxes for Select All
                self.group_card_map[date] = []

                # ---------------- CARDS ----------------
                for _, row in group.iterrows():
                    card = ctk.CTkFrame(content_frame, fg_color="#1E1E1E", corner_radius=10)
                    card.pack(fill="x", pady=5, padx=5)

                    inner = ctk.CTkFrame(card, fg_color="transparent")
                    inner.pack(fill="x", padx=10, pady=8)

                    row1 = ctk.CTkFrame(inner, fg_color="transparent")
                    row1.pack(fill="x")

                    # Checkbox (selection mode only)
                    checkbox = None
                    if self.selection_mode:
                        checkbox = ctk.CTkCheckBox(
                            row1,
                            text="", width=20,
                            command=lambda d=date: self.update_select_all_state(d)
                        )
                        checkbox.pack(side="left", padx=(0, 10))
                        self.group_card_map[date].append(checkbox)

                        # Store appointment info in checkbox
                        checkbox._appointment_info = {
                            "date": str(row["Date"]),
                            "time": row["Time"],
                            "customer_id": row["Old Customer ID"],
                            "name": row["Name"],
                            "contact": row["Contact Number"],
                            "condition": row["Condition"],
                            "treatment": row["Treatment"]
                        }

                    # Time + Name + Contact (always displayed)
                    ctk.CTkLabel(
                        row1,
                        text=f"{row['Time']}  |  {row['Name']}  |  {row['Contact Number']}",
                        font=ctk.CTkFont(size=15, weight="bold"),
                        anchor="w"
                    ).pack(side="left", padx=5)

                    # Details
                    ctk.CTkLabel(
                        inner,
                        text=f"Condition: {row['Condition']}\nTreatment: {row['Treatment']}",
                        justify="left",
                        anchor="w",
                    ).pack(fill="x", pady=(5, 0))

        except Exception as e:
            print("❌ Error loading appointments:", e)

    # -------------------------------------------------------------
    # EXPAND/COLLAPSE GROUPS
    # -------------------------------------------------------------
    def toggle_section(self, date):
        arrow, frame = self.expanded_sections[date]

        if frame.winfo_ismapped():
            frame.pack_forget()
            arrow.configure(text="▶")
        else:
            frame.pack(fill="x", padx=20, pady=5)
            arrow.configure(text="▼")

    # -------------------------------------------------------------
    # SELECTION HELPERS
    # -------------------------------------------------------------
    def select_all_in_group(self, date):
        """Toggle select-all / unselect-all based on current state."""
        checkboxes = self.group_card_map[date]

        # Check if ALL are selected
        all_selected = all(cb.get() == 1 for cb in checkboxes)

        # Toggle
        if all_selected:
            for cb in checkboxes:
                cb.deselect()
        else:
            for cb in checkboxes:
                cb.select()

        # Update button label
        self.update_select_all_state(date)


    def update_select_all_state(self, date):
        """Update Select All button text according to checkbox state."""

        # 1. Retrieve header frame for this date
        arrow, content_frame = self.expanded_sections[date]
        parent_frame = content_frame.master   # day_frame
        header = parent_frame.winfo_children()[0]

        # 2. Find the Select All button inside header
        for w in header.winfo_children():
            if isinstance(w, ctk.CTkButton) and w.cget("text") in ("Select All", "Unselect All"):
                select_all_btn = w
                break
        else:
            return  # no button (not in selection mode)

        checkboxes = self.group_card_map[date]
        all_selected = all(cb.get() == 1 for cb in checkboxes)

        select_all_btn.configure(text="Unselect All" if all_selected else "Select All")


    def export_pdf(self):
        selected = self.collect_selected_appointments()

        if not selected:
            renderPopUpModal(
                self.parent,
                "No appointments selected.",
                "Export PDF",
                "Error"
            )
            return

        # Group by date
        grouped = {}
        for item in selected:
            grouped.setdefault(item["date"], []).append(item)

        default_name = "AppointmentDetails.pdf"

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=default_name,
            title="Save Appointment PDF"
        )

        if not save_path:
            return  # User canceled save dialog

        # Generate PDF
        try:
            final_path = generateAppointmentPdf(grouped, save_path)

            # SUCCESS POPUP
            renderPopUpModal(
                self.parent,
                f"PDF successfully saved.\n\nLocation:\n{final_path}",
                "Export PDF",
                "Success"
            )

        except Exception as e:
            print("PDF ERROR:", e)

            # ERROR POPUP
            renderPopUpModal(
                self.parent,
                "Error saving report file.\nPlease try again.",
                "Export PDF",
                "Error"
            )



    def copy_selection(self):
        """Copy selected appointments to clipboard in formatted text."""
        selected = self.collect_selected_appointments()

        if not selected:
            self.clipboard_clear()
            self.clipboard_append("No appointments selected.")
            return

        # Group by date
        grouped = {}
        for item in selected:
            grouped.setdefault(item["date"], []).append(item)

        output_lines = []

        for date_str, items in sorted(grouped.items(), reverse=True):
            # Convert date string back to datetime to get weekday
            from datetime import datetime
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = date_obj.strftime("%A")  # Monday, Tuesday, etc.
            except:
                day_name = ""

            # Add day + date header
            output_lines.append(f"*{day_name} {date_str}*")
            output_lines.append("=" * 16)

            # Add each appointment
            for appt in items:
                output_lines.append(
                    f"{appt['time']} ({appt['customer_id']})\n"
                    f"*{appt['name']} {appt['contact']}*\n"
                    f"_{appt['condition']}_\n"
                    f"_{appt['treatment']}_\n"
                )
                # # Add a blank line between appointments
                # output_lines.append("")

        result = "\n".join(output_lines)

        self.clipboard_clear()
        self.clipboard_append(result)


    # -------------------------------------------------------------
    # SAFE TREATMENT LOADER
    # -------------------------------------------------------------
    def load_treatment_data(self, path):
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
                    rows.append(clean_row)

            df = pd.DataFrame(rows)
            df['treatmentDate'] = pd.to_datetime(df['treatmentDate'], errors='coerce')
            return df

        except Exception as e:
            print("⚠️ Error loading treatmentDb.csv safely:", e)
            return pd.DataFrame(columns=expected_cols)
        
        
    def collect_selected_appointments(self):
        """Return a list of dicts containing selected appointment info."""
        selected = []

        for date, checkboxes in self.group_card_map.items():
            for cb in checkboxes:
                if cb.get() == 1:
                    appt_info = getattr(cb, "_appointment_info", None)
                    if appt_info:
                        selected.append(appt_info)

        return selected