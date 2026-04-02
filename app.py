import streamlit as st
import yt_dlp
import os
import time

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Max Downloader V1.5", page_icon="💎", layout="centered")
st.title("💎 V.15 เครื่องมือดึงวิดีโอ (ฉบับแก้ 403)")
st.info("💡 หมายเหตุ: หากขึ้น Error 403 ให้เว้นระยะสักครู่แล้วกดใหม่นะครับ")

url = st.text_input("👉 วางลิงก์ YouTube/TikTok ตรงนี้ครับ:", placeholder="https://...")

if st.button("🚀 เริ่มดึงข้อมูลวิดีโอ"):
    if url:
        with st.spinner('⏳ กำลังพยายามขุดหาไฟล์... (รอแป๊บนี้นะครับ)'):
            try:
                # ชื่อไฟล์ชั่วคราว
                out_filename = f"video_{int(time.time())}.mp4"
                
                # สูตรลับหลบการบล็อก (User-Agent และเครื่องมือช่วย)
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': out_filename,
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'referer': 'https://www.google.com/',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # แสดงปุ่มดาวน์โหลด
                if os.path.exists(out_filename):
                    with open(out_filename, "rb") as f:
                        st.success("✅ ดึงข้อมูลสำเร็จแล้ว!")
                        st.download_button(
                            label="⬇️ กดบันทึกลงมือถือ",
                            data=f,
                            file_name="max_video.mp4",
                            mime="video/mp4"
                        )
                    os.remove(out_filename)
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {str(e)}")
    else:
        st.warning("⚠️ กรุณาวางลิงก์ก่อนครับพี่แม็ก")
