import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Max Downloader", page_icon="💎")
st.title("💎 V.16 เครื่องมือดึงวิดีโอ (Anti-Block)")

url = st.text_input("👉 วางลิงก์ตรงนี้ครับ:")

if st.button("🚀 เริ่มดาวน์โหลด"):
    if url:
        with st.spinner('⏳ กำลังดึงข้อมูล... (ขั้นตอนนี้อาจใช้เวลา 1-2 นาทีนะครับ)'):
            try:
                # สูตรแก้ 403: บังคับใช้รูปแบบที่ YouTube ไม่ค่อยบล็อก
                ydl_opts = {
                    'format': 'best[ext=mp4]/best', # เน้น MP4 ที่รวมร่างมาแล้ว
                    'outtmpl': 'video_final.mp4',
                    'nocheckcertificate': True,
                    'quiet': True,
                    'no_warnings': True,
                    'add_header': [
                        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language: en-US,en;q=0.5',
                    ]
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                with open("video_final.mp4", "rb") as f:
                    st.success("✅ ดึงข้อมูลสำเร็จ!")
                    st.download_button(
                        label="⬇️ บันทึกลงเครื่อง",
                        data=f,
                        file_name="max_video.mp4",
                        mime="video/mp4"
                    )
                os.remove("video_final.mp4")
            except Exception as e:
                st.error(f"❌ ระบบ YouTube บล็อก IP ของเซิร์ฟเวอร์ (403)\nแนะนำให้ลองลิงก์อื่น หรือเว้นระยะสักครู่ครับ")
    else:
        st.warning("⚠️ กรุณาวางลิงก์ก่อนครับ")
