import streamlit as st
import yt_dlp
import os
import time
import imageio_ffmpeg

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Raw Source Downloader (Max Quality)", page_icon="💎", layout="centered")
st.title("💎 V.15 เครื่องมือเปลี่ยนลิ้งเป็นวีดีโอฟรี (ชัดที่สุดในโลก)")
st.info("💡 หมายเหตุ: ความชัดขึ้นอยู่กับต้นฉบับ 100% ถ้าต้นฉบับชัด 4K เราก็ได้ 4K ครับ (แต่ถ้าต้นฉบับไม่ชัด เราก็ทำอะไรไม่ได้ครับ)")

# ฟังก์ชันโหลดคลิป (โหมดดูดไฟล์ดิบ)
def download_raw_source(url):
    timestamp = int(time.time())
    # ตั้งชื่อไฟล์รอไว้ก่อน (เดี๋ยวตัวโหลดจะเติมนามสกุลให้เอง)
    output_template = f"raw_video_{timestamp}.%(ext)s"
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    ydl_opts = {
        # สูตรลับ V.15: ขอไฟล์ Video ที่ Bitrate สูงที่สุด + Audio ที่ Bitrate สูงที่สุด
        # ไม่สนความละเอียด ขอแค่ "ดีที่สุด" (best)
        'format': 'bestvideo+bestaudio/best',
        
        'outtmpl': output_template,
        'noplaylist': True,
        
        # บังคับรวมร่างเป็น MKV หรือ MP4 เพื่อคุณภาพสูงสุด (MKV รองรับคุณภาพสูงกว่าในบางครั้ง)
        'merge_output_format': 'mp4',
        
        'ffmpeg_location': ffmpeg_exe,
        
        # ปิดการแปลงไฟล์ที่ไม่จำเป็น เพื่อรักษาคุณภาพไฟล์ดิบไว้
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        
        # TikTok: ขอแบบไม่มีลายน้ำ (No Watermark) ซึ่งมักจะชัดกว่า
        'extractor_args': {'tiktok': {'adapt_html5_video_player': False}},
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
        # เช็คไฟล์ผลลัพธ์ (เผื่อโดนเปลี่ยนนามสกุล)
        base, ext = os.path.splitext(filename)
        final_filename = filename
        
        # บางทีมันเซฟเป็น .mkv หรือ .webm เราต้องหาให้เจอ
        possible_exts = ['.mp4', '.mkv', '.webm']
        if not os.path.exists(final_filename):
             for try_ext in possible_exts:
                 if os.path.exists(base + try_ext):
                     final_filename = base + try_ext
                     break
        
        # ส่งค่ากลับ: ชื่อไฟล์, ความชัด, และ Bitrate (ถ้ามี)
        resolution = info.get('resolution', 'Unknown')
        if resolution == 'Unknown': # ลองหาจาก height
             h = info.get('height')
             if h: resolution = f"{h}p"
             
        return final_filename, resolution

# --- หน้าเว็บ ---
url = st.text_input("👉 วางลิงก์ YouTube/TikTok (ขอคลิปชัดๆ):", placeholder="https://...")

if st.button("🚀 ดูดไฟล์ต้นฉบับ (Raw Download)"):
    if url:
        st.write("⏳ กำลังขุดหาไฟล์ที่ชัดที่สุดจาก Server... (รอแป๊บนะครับ)")
        
        try:
            file_path, resolution = download_raw_source(url)
            
            if os.path.exists(file_path):
                st.success(f"✅ ได้ไฟล์มาแล้ว! ความละเอียด: {resolution}")
                st.caption("⚠️ ถ้าดูในเว็บแล้วภาพแตก ไม่ต้องตกใจนะครับ! ให้กดปุ่ม Save แล้วไปเปิดในเครื่อง จะชัดแจ๋วครับ")
                
                # โชว์คลิป (Browser อาจจะลดคุณภาพตอนพรีวิว)
                st.video(file_path)
                
                # ปุ่มโหลดไฟล์จริง
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"💾 กดตรงนี้เพื่อบันทึกไฟล์ ({os.path.basename(file_path)})",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
            else:
                st.error("❌ หาไฟล์ไม่เจอ ลองใหม่อีกครั้งครับ")
                
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("⚠️ กรุณาวางลิงก์ก่อนครับ")