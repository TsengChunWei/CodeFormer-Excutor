from tkinter.ttk import Combobox, Style
from tkinter.ttk import Button as ttkButton
from tkinter.ttk import Entry as ttkEntry
from tkinter.ttk import Label as ttkLabel
from tkinter import filedialog, Frame, Label, StringVar
from CodeFomerExcute import One, Multiple, One_video, One_inpaint, Multiple_inpaint, One_colorize, Multiple_colorize

class RepairPage:
    def __init__(self, parent) -> None:
        self.origin_folder = ""
        self.repair_folder = "" 
        self.repair_img = "" 
        self.Font = "Helvetica"
        
        self.page = Frame(parent)

        style = Style()
        style.configure("TLabel", font=(self.Font, 12))
        style.configure("TEntry", font=(self.Font, 12))
        style.configure("Brw.TButton", font=(self.Font, 12))
        style.configure("run.TButton",
                        font=(self.Font, 16, "bold"),
                        background="#4CAF50",
                        padding=12,
                        borderwidth=2,
                        relief="raised")

        self.frame_select = Frame(self.page)
        label_select = Label(self.frame_select, text="資料夾選擇", background="#b4b4f0", font=(self.Font, 16))
        label_select.grid(row=0, column=0, pady=(30, 10), columnspan=3)
        self.SelectFolders()
        self.frame_select.grid(row=0, column=1, padx=(15, 25))

        self.frame_img_select = Frame(self.page)
        img_label_select = Label(self.frame_img_select, text="圖片選擇", background="#b4b4f0", font=(self.Font, 16))
        img_label_select.grid(row=0, column=0, pady=(30, 10), columnspan=3)
        self.create_folder_browser(True, self.frame_img_select, 1, "修復單張圖片：", self.set_repair_img_path)
        self.frame_img_select.grid(row=1, column=1, padx=(15, 25))

        self.frame_parameter = Frame(self.page)
        label_parameter = Label(self.frame_parameter, text="參數設定", background="#f0b4b4" , font=(self.Font, 16))
        label_parameter.grid(row=0, column=0, pady=(30, 10))
        self.set_weight()
        self.set_bg()
        self.set_face()
        self.set_scale()
        self.frame_parameter.grid(row=0, column=0, padx=(25, 15), rowspan=2)

        self.frame_excuting1 = Frame(self.page)
        self.excuting_btn1()
        self.frame_excuting1.grid(row=0, column=2, padx=20)

        self.frame_excuting2 = Frame(self.page)
        self.excuting_btn2()
        self.frame_excuting2.grid(row=1, column=2, padx=20)

        self.page.columnconfigure(0, weight=1)
        self.page.columnconfigure(1, weight=3)
        self.page.columnconfigure(2, weight=1)


    def create_folder_browser(self, IMG, currFrame, row, label_text, set_path_callback):
        folder_label = ttkLabel(currFrame, text=label_text, font=(self.Font, 14))
        folder_label.grid(row=row, column=0, padx=0, pady=0)

        folder_var = StringVar()
        folder_var.trace("w", lambda *args: self.on_entry_change(folder_var, display_label, set_path_callback))

        folder_entry = ttkEntry(currFrame, textvariable=folder_var, width=40, font=(self.Font, 12))
        folder_entry.grid(row=row, column=1, padx=0, pady=0)

        if IMG:
            browse_button = ttkButton(currFrame, text="瀏覽..", width=6, command=lambda: self.browse_img(folder_var), style='Brw.TButton')
        else:
            browse_button = ttkButton(currFrame, text="瀏覽..", width=6, command=lambda: self.browse_folder(folder_var), style='Brw.TButton')
        browse_button.grid(row=row, column=2, padx=0, pady=0)

        display_label = ttkLabel(currFrame, text="選擇的路徑將顯示在這裡")
        display_label.grid(row=row+1, column=0, columnspan=3, padx=0, pady=(0, 18))

    def browse_img(self, img_var):
        img_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if img_selected:
            img_var.set(img_selected)

    def browse_folder(self, folder_var):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            folder_var.set(folder_selected)

    def on_entry_change(self, folder_var, display_label, set_path_callback):
        folder_path = folder_var.get()
        max_length = 50  # 設定最大顯示長度
        if len(folder_path) > max_length:
            display_text = folder_path[:max_length] + "..."
        else:
            display_text = folder_path
        display_label.config(text=f"路徑: {display_text}")
        set_path_callback(folder_path)

    def set_origin_path(self, path):
        self.origin_folder = path

    def set_repair_path(self, path):
        self.repair_folder = path

    def set_repair_img_path(self, path):
        self.repair_img = path

    def SelectFolders(self):
        self.origin_folder = ""
        self.repair_folder = ""

        self.create_folder_browser(False, self.frame_select, 1, "修復圖片資料夾：", self.set_origin_path)
        self.create_folder_browser(False, self.frame_select, 3, "完成圖片資料夾：", self.set_repair_path)

    def set_weight(self):
        weight_frame = Frame(self.frame_parameter)
        weight_frame.grid(row=1, column=0, pady=3, sticky="w")

        weight_label = Label(weight_frame, text="權重：", width=10, font=(self.Font, 14), anchor='w')
        weight_label.grid(row=0, column=0, sticky='w')

        self.weight_entry = ttkEntry(weight_frame, width=5, justify='center', font=(self.Font, 14))
        self.weight_entry.insert(0, "0.7")  # 預設值
        self.weight_entry.grid(row=0, column=1)

    def set_bg(self):
        bg_frame = Frame(self.frame_parameter)
        bg_frame.grid(row=2, column=0, pady=3, sticky="w")

        bg_label = Label(bg_frame, text="背景：", width=10, font=(self.Font, 14), anchor='w')
        bg_label.grid(row=0, column=0, sticky='w')

        self.bg_entry = StringVar(value='True')  # 預設值為字符串

        # 使用 ttk.Combobox 創建下拉選單
        bg_combobox = Combobox(bg_frame, textvariable=self.bg_entry, values=['修', '不修'], font=(self.Font, 12), width=4, justify='center')
        bg_combobox.grid(row=0, column=1)
        bg_combobox.set('修')

    def set_face(self):
        face_frame = Frame(self.frame_parameter)
        face_frame.grid(row=3, column=0, pady=3, sticky="w")

        face_label = Label(face_frame, text="臉部：", width=10, font=(self.Font, 14), anchor='w')
        face_label.grid(row=0, column=0, sticky='w')

        self.face_entry = StringVar(value='True')  # 預設值為字符串

        # 使用 ttk.Combobox 創建下拉選單
        face_combobox = Combobox(face_frame, textvariable=self.face_entry, values=['修', '不修'], font=(self.Font, 12), width=4, justify='center')
        face_combobox.grid(row=0, column=1)
        face_combobox.set('修')

    def set_scale(self):
        scale_frame = Frame(self.frame_parameter)
        scale_frame.grid(row=4, column=0, pady=3, sticky="w")

        scale_label = Label(scale_frame, text="放大倍數：", width=10, font=(self.Font, 14), anchor='w')
        scale_label.grid(row=0, column=0, sticky='w')

        self.scale_entry = ttkEntry(scale_frame, width=5, justify='center', font=(self.Font, 14))
        self.scale_entry.insert(0, "2")  # 預設值
        self.scale_entry.grid(row=0, column=1)

    def excuting_btn1(self):
        main_btn = ttkButton(self.frame_excuting1, text="執行", width=8, command=self.execute_main1, style='run.TButton')
        main_btn.grid()

    def execute_main1(self):
        _weight_p_ = float(self.weight_entry.get())
        _bg_p_ = self.bg_entry.get() == '修'
        _face_p_ = self.face_entry.get() == '修'
        _scale_p_ = int(self.scale_entry.get())
        Multiple(self.origin_folder, self.repair_folder, _weight_p_, _bg_p_, _face_p_, _scale_p_)

    def excuting_btn2(self):
        main_btn = ttkButton(self.frame_excuting2, text="單張執行", width=8, command=self.execute_main2, style='run.TButton')
        main_btn.grid()

    def execute_main2(self):
        _weight_p_ = float(self.weight_entry.get())
        _bg_p_ = self.bg_entry.get() == '修'
        _face_p_ = self.face_entry.get() == '修'
        _scale_p_ = int(self.scale_entry.get())
        One(self.repair_img, _weight_p_, _bg_p_, _face_p_, _scale_p_)

class VideoRepairPage:
    def __init__(self, parent) -> None:
        self.origin_folder = ""
        self.repair_folder = "" 
        self.repair_img = "" 
        self.Font = "Helvetica"
        
        self.page = Frame(parent)

        style = Style()
        style.configure("TLabel", font=(self.Font, 12))
        style.configure("TEntry", font=(self.Font, 12))
        style.configure("Brw.TButton", font=(self.Font, 12))
        style.configure("run.TButton",
                        font=(self.Font, 16, "bold"),
                        background="#4CAF50",
                        padding=12,
                        borderwidth=2,
                        relief="raised")

        self.frame_vid_select = Frame(self.page)
        vid_label_select = Label(self.frame_vid_select, text="影片選擇", background="#b4b4f0", font=(self.Font, 16))
        vid_label_select.grid(row=0, column=0, pady=(30, 10), columnspan=3)
        self.create_folder_browser(self.frame_vid_select, 1, "修復單支影片：", self.set_repair_img_path)
        self.frame_vid_select.grid(row=1, column=1, padx=(15, 25))

        self.frame_parameter = Frame(self.page)
        label_parameter = Label(self.frame_parameter, text="參數設定", background="#f0b4b4" , font=(self.Font, 16))
        label_parameter.grid(row=0, column=0, pady=(30, 10))
        self.set_weight()
        self.set_bg()
        self.set_face()
        self.set_scale()
        self.frame_parameter.grid(row=0, column=0, padx=(25, 15), rowspan=2)

        self.frame_excuting2 = Frame(self.page)
        self.excuting_btn2()
        self.frame_excuting2.grid(row=1, column=2, padx=20)

        self.page.columnconfigure(0, weight=1)
        self.page.columnconfigure(1, weight=3)
        self.page.columnconfigure(2, weight=1)


    def create_folder_browser(self, currFrame, row, label_text, set_path_callback):
        folder_label = ttkLabel(currFrame, text=label_text, font=(self.Font, 14))
        folder_label.grid(row=row, column=0, padx=0, pady=0)

        folder_var = StringVar()
        folder_var.trace("w", lambda *args: self.on_entry_change(folder_var, display_label, set_path_callback))

        folder_entry = ttkEntry(currFrame, textvariable=folder_var, width=40, font=(self.Font, 12))
        folder_entry.grid(row=row, column=1, padx=0, pady=0)

        browse_button = ttkButton(currFrame, text="瀏覽..", width=6, command=lambda: self.browse_img(folder_var), style='Brw.TButton')

        browse_button.grid(row=row, column=2, padx=0, pady=0)

        display_label = ttkLabel(currFrame, text="選擇的路徑將顯示在這裡")
        display_label.grid(row=row+1, column=0, columnspan=3, padx=0, pady=(0, 18))

    def browse_img(self, img_var):
        img_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.mp4;*.MOV;*.avi")])
        if img_selected:
            img_var.set(img_selected)

    def on_entry_change(self, folder_var, display_label, set_path_callback):
        folder_path = folder_var.get()
        max_length = 50  # 設定最大顯示長度
        if len(folder_path) > max_length:
            display_text = folder_path[:max_length] + "..."
        else:
            display_text = folder_path
        display_label.config(text=f"路徑: {display_text}")
        set_path_callback(folder_path)

    def set_origin_path(self, path):
        self.origin_folder = path

    def set_repair_path(self, path):
        self.repair_folder = path

    def set_repair_img_path(self, path):
        self.repair_img = path

    def set_weight(self):
        weight_frame = Frame(self.frame_parameter)
        weight_frame.grid(row=1, column=0, pady=3, sticky="w")

        weight_label = Label(weight_frame, text="權重：", width=10, font=(self.Font, 14), anchor='w')
        weight_label.grid(row=0, column=0, sticky='w')

        self.weight_entry = ttkEntry(weight_frame, width=5, justify='center', font=(self.Font, 14))
        self.weight_entry.insert(0, "0.7")  # 預設值
        self.weight_entry.grid(row=0, column=1)

    def set_bg(self):
        bg_frame = Frame(self.frame_parameter)
        bg_frame.grid(row=2, column=0, pady=3, sticky="w")

        bg_label = Label(bg_frame, text="背景：", width=10, font=(self.Font, 14), anchor='w')
        bg_label.grid(row=0, column=0, sticky='w')

        self.bg_entry = StringVar(value='True')  # 預設值為字符串

        # 使用 ttk.Combobox 創建下拉選單
        bg_combobox = Combobox(bg_frame, textvariable=self.bg_entry, values=['修', '不修'], font=(self.Font, 12), width=4, justify='center')
        bg_combobox.grid(row=0, column=1)
        bg_combobox.set('修')

    def set_face(self):
        face_frame = Frame(self.frame_parameter)
        face_frame.grid(row=3, column=0, pady=3, sticky="w")

        face_label = Label(face_frame, text="臉部：", width=10, font=(self.Font, 14), anchor='w')
        face_label.grid(row=0, column=0, sticky='w')

        self.face_entry = StringVar(value='True')  # 預設值為字符串

        # 使用 ttk.Combobox 創建下拉選單
        face_combobox = Combobox(face_frame, textvariable=self.face_entry, values=['修', '不修'], font=(self.Font, 12), width=4, justify='center')
        face_combobox.grid(row=0, column=1)
        face_combobox.set('修')

    def set_scale(self):
        scale_frame = Frame(self.frame_parameter)
        scale_frame.grid(row=4, column=0, pady=3, sticky="w")

        scale_label = Label(scale_frame, text="放大倍數：", width=10, font=(self.Font, 14), anchor='w')
        scale_label.grid(row=0, column=0, sticky='w')

        self.scale_entry = ttkEntry(scale_frame, width=5, justify='center', font=(self.Font, 14))
        self.scale_entry.insert(0, "2")  # 預設值
        self.scale_entry.grid(row=0, column=1)


    def excuting_btn2(self):
        main_btn = ttkButton(self.frame_excuting2, text="單支執行", width=8, command=self.execute_main2, style='run.TButton')
        main_btn.grid()

    def execute_main2(self):
        _weight_p_ = float(self.weight_entry.get())
        _bg_p_ = self.bg_entry.get() == '修'
        _face_p_ = self.face_entry.get() == '修'
        _scale_p_ = int(self.scale_entry.get())
        One_video(self.repair_img, _weight_p_, _bg_p_, _face_p_, _scale_p_)


class InpaintPage:
    def __init__(self, parent) -> None:
        self.origin_folder = ""
        self.repair_folder = "" 
        self.repair_img = "" 
        self.Font = "Helvetica"
        
        self.page = Frame(parent)

        style = Style()
        style.configure("TLabel", font=(self.Font, 12))
        style.configure("TEntry", font=(self.Font, 12))
        style.configure("Brw.TButton", font=(self.Font, 12))
        style.configure("run.TButton",
                        font=(self.Font, 16, "bold"),
                        background="#4CAF50",
                        padding=12,
                        borderwidth=2,
                        relief="raised")

        self.frame_select = Frame(self.page)
        label_select = Label(self.frame_select, text="資料夾選擇", background="#b4b4f0", font=(self.Font, 16))
        label_select.grid(row=0, column=0, pady=(30, 10), columnspan=3)
        self.SelectFolders()
        self.frame_select.grid(row=0, column=1, padx=(15, 25))

        self.frame_img_select = Frame(self.page)
        img_label_select = Label(self.frame_img_select, text="圖片選擇", background="#b4b4f0", font=(self.Font, 16))
        img_label_select.grid(row=0, column=0, pady=(30, 10), columnspan=3)
        self.create_folder_browser(True, self.frame_img_select, 1, "填補單張圖片：", self.set_repair_img_path)
        self.frame_img_select.grid(row=1, column=1, padx=(15, 25))

        self.frame_parameter = Frame(self.page)
        label_parameter = Label(self.frame_parameter, text="無參數", background="#f0b4b4" , font=(self.Font, 16))
        label_parameter.grid(row=0, column=0, pady=(30, 10))
        _label_ = Label(self.frame_parameter, width=14, font=(self.Font, 16))
        _label_.grid(row=1, column=0, pady=(30, 10))
        self.frame_parameter.grid(row=0, column=0, padx=(25, 15), rowspan=2)

        self.frame_excuting1 = Frame(self.page)
        self.excuting_btn1()
        self.frame_excuting1.grid(row=0, column=2, padx=20)

        self.frame_excuting2 = Frame(self.page)
        self.excuting_btn2()
        self.frame_excuting2.grid(row=1, column=2, padx=20)

        self.page.columnconfigure(0, weight=1)
        self.page.columnconfigure(1, weight=3)
        self.page.columnconfigure(2, weight=1)


    def create_folder_browser(self, IMG, currFrame, row, label_text, set_path_callback):
        folder_label = ttkLabel(currFrame, text=label_text, font=(self.Font, 14))
        folder_label.grid(row=row, column=0, padx=0, pady=0)

        folder_var = StringVar()
        folder_var.trace("w", lambda *args: self.on_entry_change(folder_var, display_label, set_path_callback))

        folder_entry = ttkEntry(currFrame, textvariable=folder_var, width=40, font=(self.Font, 12))
        folder_entry.grid(row=row, column=1, padx=0, pady=0)

        if IMG:
            browse_button = ttkButton(currFrame, text="瀏覽..", width=6, command=lambda: self.browse_img(folder_var), style='Brw.TButton')
        else:
            browse_button = ttkButton(currFrame, text="瀏覽..", width=6, command=lambda: self.browse_folder(folder_var), style='Brw.TButton')
        browse_button.grid(row=row, column=2, padx=0, pady=0)

        display_label = ttkLabel(currFrame, text="選擇的路徑將顯示在這裡")
        display_label.grid(row=row+1, column=0, columnspan=3, padx=0, pady=(0, 18))

    def browse_img(self, img_var):
        img_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.mp4;*.MOV")])
        if img_selected:
            img_var.set(img_selected)

    def browse_folder(self, folder_var):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            folder_var.set(folder_selected)

    def on_entry_change(self, folder_var, display_label, set_path_callback):
        folder_path = folder_var.get()
        max_length = 50  # 設定最大顯示長度
        if len(folder_path) > max_length:
            display_text = folder_path[:max_length] + "..."
        else:
            display_text = folder_path
        display_label.config(text=f"路徑: {display_text}")
        set_path_callback(folder_path)

    def set_origin_path(self, path):
        self.origin_folder = path

    def set_repair_path(self, path):
        self.repair_folder = path

    def set_repair_img_path(self, path):
        self.repair_img = path

    def SelectFolders(self):
        self.origin_folder = ""
        self.repair_folder = ""

        self.create_folder_browser(False, self.frame_select, 1, "填補圖片資料夾：", self.set_origin_path)
        self.create_folder_browser(False, self.frame_select, 3, "完成圖片資料夾：", self.set_repair_path)


    def excuting_btn1(self):
        main_btn = ttkButton(self.frame_excuting1, text="執行", width=8, command=self.execute_main1, style='run.TButton')
        main_btn.grid()

    def execute_main1(self):
        Multiple_inpaint(self.origin_folder, self.repair_folder)

    def excuting_btn2(self):
        main_btn = ttkButton(self.frame_excuting2, text="單張執行", width=8, command=self.execute_main2, style='run.TButton')
        main_btn.grid()

    def execute_main2(self):
        One_inpaint(self.repair_img)

class ColorizePage:
    def __init__(self, parent) -> None:
        self.origin_folder = ""
        self.repair_folder = "" 
        self.repair_img = "" 
        self.Font = "Helvetica"
        
        self.page = Frame(parent)

        style = Style()
        style.configure("TLabel", font=(self.Font, 12))
        style.configure("TEntry", font=(self.Font, 12))
        style.configure("Brw.TButton", font=(self.Font, 12))
        style.configure("run.TButton",
                        font=(self.Font, 16, "bold"),
                        background="#4CAF50",
                        padding=12,
                        borderwidth=2,
                        relief="raised")

        self.frame_select = Frame(self.page)
        label_select = Label(self.frame_select, text="資料夾選擇", background="#b4b4f0", font=(self.Font, 16))
        label_select.grid(row=0, column=0, pady=(30, 10), columnspan=3)
        self.SelectFolders()
        self.frame_select.grid(row=0, column=1, padx=(15, 25))

        self.frame_img_select = Frame(self.page)
        img_label_select = Label(self.frame_img_select, text="圖片選擇", background="#b4b4f0", font=(self.Font, 16))
        img_label_select.grid(row=0, column=0, pady=(30, 10), columnspan=3)
        self.create_folder_browser(True, self.frame_img_select, 1, "上色單張圖片：", self.set_repair_img_path)
        self.frame_img_select.grid(row=1, column=1, padx=(15, 25))

        self.frame_parameter = Frame(self.page)
        label_parameter = Label(self.frame_parameter, text="無參數", background="#f0b4b4" , font=(self.Font, 16))
        label_parameter.grid(row=0, column=0, pady=(30, 10))
        _label_ = Label(self.frame_parameter, width=14, font=(self.Font, 16))
        _label_.grid(row=1, column=0, pady=(30, 10))
        self.frame_parameter.grid(row=0, column=0, padx=(25, 15), rowspan=2)

        self.frame_excuting1 = Frame(self.page)
        self.excuting_btn1()
        self.frame_excuting1.grid(row=0, column=2, padx=20)

        self.frame_excuting2 = Frame(self.page)
        self.excuting_btn2()
        self.frame_excuting2.grid(row=1, column=2, padx=20)

        self.page.columnconfigure(0, weight=1)
        self.page.columnconfigure(1, weight=3)
        self.page.columnconfigure(2, weight=1)


    def create_folder_browser(self, IMG, currFrame, row, label_text, set_path_callback):
        folder_label = ttkLabel(currFrame, text=label_text, font=(self.Font, 14))
        folder_label.grid(row=row, column=0, padx=0, pady=0)

        folder_var = StringVar()
        folder_var.trace("w", lambda *args: self.on_entry_change(folder_var, display_label, set_path_callback))

        folder_entry = ttkEntry(currFrame, textvariable=folder_var, width=40, font=(self.Font, 12))
        folder_entry.grid(row=row, column=1, padx=0, pady=0)

        if IMG:
            browse_button = ttkButton(currFrame, text="瀏覽..", width=6, command=lambda: self.browse_img(folder_var), style='Brw.TButton')
        else:
            browse_button = ttkButton(currFrame, text="瀏覽..", width=6, command=lambda: self.browse_folder(folder_var), style='Brw.TButton')
        browse_button.grid(row=row, column=2, padx=0, pady=0)

        display_label = ttkLabel(currFrame, text="選擇的路徑將顯示在這裡")
        display_label.grid(row=row+1, column=0, columnspan=3, padx=0, pady=(0, 18))

    def browse_img(self, img_var):
        img_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if img_selected:
            img_var.set(img_selected)

    def browse_folder(self, folder_var):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            folder_var.set(folder_selected)

    def on_entry_change(self, folder_var, display_label, set_path_callback):
        folder_path = folder_var.get()
        max_length = 50  # 設定最大顯示長度
        if len(folder_path) > max_length:
            display_text = folder_path[:max_length] + "..."
        else:
            display_text = folder_path
        display_label.config(text=f"路徑: {display_text}")
        set_path_callback(folder_path)

    def set_origin_path(self, path):
        self.origin_folder = path

    def set_repair_path(self, path):
        self.repair_folder = path

    def set_repair_img_path(self, path):
        self.repair_img = path

    def SelectFolders(self):
        self.origin_folder = ""
        self.repair_folder = ""

        self.create_folder_browser(False, self.frame_select, 1, "上色圖片資料夾：", self.set_origin_path)
        self.create_folder_browser(False, self.frame_select, 3, "完成圖片資料夾：", self.set_repair_path)


    def excuting_btn1(self):
        main_btn = ttkButton(self.frame_excuting1, text="執行", width=8, command=self.execute_main1, style='run.TButton')
        main_btn.grid()

    def execute_main1(self):
        Multiple_colorize(self.origin_folder, self.repair_folder)

    def excuting_btn2(self):
        main_btn = ttkButton(self.frame_excuting2, text="單張執行", width=8, command=self.execute_main2, style='run.TButton')
        main_btn.grid()

    def execute_main2(self):
        One_colorize(self.repair_img)
