import customtkinter as ctk
import yt_dlp
import os
import threading
from tkinter import messagebox, filedialog
import imageio_ffmpeg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VideoDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("โปรแกรมแปลงวีดีโอ")
        self.geometry("600x480")

        self.label_title = ctk.CTkLabel(self, text="💎 โปรแกรมแปลงวีดีโอ", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=30)

        self.entry_url = ctk.CTkEntry(self, placeholder_text="วางลิงก์ YouTube, TikTok, Facebook...", width=480, height=45)
        self.entry_url.pack(pady=10)

        self.btn_download = ctk.CTkButton(self, text="🚀 เริ่มดาวน์โหลดความชัดสูงสุด", 
                                          width=250, height=55, 
                                          font=("Arial", 18, "bold"),
                                          command=self.start_download_thread)
        self.btn_download.pack(pady=20)

        self.label_status = ctk.CTkLabel(self, text="สถานะ: พร้อมใช้งาน", text_color="gray")
        self.label_status.pack(pady=10)

    def start_download_thread(self):
        url = self.entry_url.get()
        if not url:
            messagebox.showwarning("แจ้งเตือน", "กรุณาวางลิงก์ก่อนครับ")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("Video files", "*.mp4")],
            title="เลือกที่เก็บไฟล์"
        )
        
        if not save_path: return

        self.btn_download.configure(state="disabled", text="⏳ กำลังทำงาน...")
        self.label_status.configure(text="กำลังดึงข้อมูลไฟล์...", text_color="orange")
        
        thread = threading.Thread(target=self.download_video, args=(url, save_path))
        thread.daemon = True
        thread.start()

    def download_video(self, url, save_path):
        try:
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': save_path,
                'merge_output_format': 'mp4',
                'ffmpeg_location': ffmpeg_exe,
                'noplaylist': True,
                'quiet': True,
                
                # --- ส่วนเพิ่มเพื่อแก้ปัญหาไม่มีเสียง (Opus Fix) ---
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4', # บังคับรวมเป็น MP4 ที่มาตรฐานที่สุด
                }, {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'aac', # ใช้ Codec เสียง AAC ที่เปิดได้ทุกเครื่อง
                }],
                # ---------------------------------------------

                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            } AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
                'nocheckcertificate': True,
                # ------------------------------------
            }
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.after(0, lambda: self.finish_download(True))
        except Exception as err:
            # แก้บั๊ก NameError: ส่งค่า err ไปเป็น string แทน
            error_message = str(err)
            self.after(0, lambda: self.finish_download(False, error_message))

    def finish_download(self, success, error_msg=""):
        self.btn_download.configure(state="normal", text="🚀 เริ่มดาวน์โหลดความชัดสูงสุด")
        if success:
            self.label_status.configure(text="✅ ดาวน์โหลดสำเร็จ!", text_color="#00FF00")
            messagebox.showinfo("สำเร็จ", "ดาวน์โหลดวิดีโอเรียบร้อย!")
        else:
            self.label_status.configure(text="❌ เกิดข้อผิดพลาด", text_color="red")
            messagebox.showerror("ผิดพลาด", f"สาเหตุ: {error_msg}")

if __name__ == "__main__":
    app = VideoDownloaderApp()
    app.mainloop()
