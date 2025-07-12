import customtkinter

def createDetailField(root, fieldName, content, row, column, rowspan=1):
    # Field name label
    customtkinter.CTkLabel(
        root,
        text=fieldName,
        bg_color='transparent',
        anchor="w"
    ).grid(row=row, column=column, sticky="w", padx=(10, 5), pady=5)
    # Content label (support rowspan)
    contentLabel  = customtkinter.CTkLabel(
        root,
        text=content if content != "" else "---", 
        bg_color='transparent',
        wraplength=200,
        anchor="w",
        justify="left",
        width=200
    )
    contentLabel.grid(row=row, column=column + 1, rowspan=rowspan, sticky="w", padx=(5, 10), pady=5)
    
    return contentLabel