from tkinter import Tk, BOTH, YES
from tkinter.ttk import Notebook, Style
from GUI import ColorizePage, InpaintPage, RepairPage, VideoRepairPage

class CombinedApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("CodeFormer修圖器")
        self.root.geometry("1080x400+150+150")
        self.root.minsize(1080, 400)
        self.init_ui()

    def init_ui(self):
        style = Style()
        style.configure("TNotebook.Tab", 
                        font=("Helvetica", 12),
                        borderwidth=2)

        self.notebook = Notebook(self.root, style="TNotebook")
        self.notebook.pack(fill=BOTH, expand=YES)

        repair_page = RepairPage(self.notebook)
        self.notebook.add(repair_page.page, text=" 修復 ")

        vid_repair_page = VideoRepairPage(self.notebook)
        self.notebook.add(vid_repair_page.page, text=" 影片修復 ")

        inpaint_page = InpaintPage(self.notebook)
        self.notebook.add(inpaint_page.page, text=" 填補 ")

        colorize_page = ColorizePage(self.notebook)
        self.notebook.add(colorize_page.page, text=" 上色 ")

    def run(self):
        self.root.mainloop()

app = CombinedApp()
app.run()
