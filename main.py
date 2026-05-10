import flet as ft
import time
import threading

def main(page: ft.Page):
    # Konfigurasi Halaman Utama
    page.title = "Terapi Fokus SanFK"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#010307"
    page.padding = 25
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Variabel State
    is_playing = threading.Event()
    seconds = 0

    # UI Components
    timer_text = ft.Text("00:00", size=50, weight="bold", color="#00d2ff")
    status_text = ft.Text("Siap Memulai Terapi", size=14, color="#00d2ff", opacity=0.8)
    pb = ft.ProgressBar(value=0, width=400, color="#00d2ff", bgcolor="#1e2533")

    # Input Fields (Default sesuai permintaanmu)
    f1 = ft.TextField(label="Freq L (Hz)", value="3117.26", border_color="#00d2ff", expand=1)
    f2 = ft.TextField(label="Freq R (Hz)", value="3157.94", border_color="#00d2ff", expand=1)
    a1 = ft.TextField(label="Amp 1", value="0.5", border_color="#00d2ff", expand=1)
    a2 = ft.TextField(label="Amp 2", value="0.5", border_color="#00d2ff", expand=1)

    # Indikator Mode
    alpha_chip = ft.Chip(label=ft.Text("ALPHA"), leading=ft.Icon(ft.icons.WAVES), disabled=True)
    gamma_chip = ft.Chip(label=ft.Text("GAMMA"), leading=ft.Icon(ft.icons.BOLT), disabled=True)
    theta_chip = ft.Chip(label=ft.Text("THETA"), leading=ft.Icon(ft.icons.BEDTIME), disabled=True)

    def timer_task():
        nonlocal seconds
        while True:
            if is_playing.is_set():
                seconds += 1
                mins, secs = divmod(seconds, 60)
                timer_text.value = f"{mins:02d}:{secs:02d}"
                pb.value = seconds / 1800 # 30 Menit

                # Logika Mode Otomatis
                alpha_chip.disabled = not (0 <= seconds < 300)
                gamma_chip.disabled = not (300 <= seconds < 1500)
                theta_chip.disabled = not (1500 <= seconds <= 1800)

                if seconds >= 1800:
                    stop_clicked(None)
                
                page.update()
                time.sleep(1)
            else:
                time.sleep(0.5)

    def play_clicked(e):
        is_playing.set()
        play_btn.visible = False
        pause_btn.visible = True
        status_text.value = "Terapi Sedang Berjalan..."
        page.update()

    def pause_clicked(e):
        is_playing.clear()
        play_btn.visible = True
        pause_btn.visible = False
        status_text.value = "Terapi Dipause"
        page.update()

    def stop_clicked(e):
        nonlocal seconds
        is_playing.clear()
        seconds = 0
        timer_text.value = "00:00"
        pb.value = 0
        play_btn.visible = True
        pause_btn.visible = False
        status_text.value = "Terapi Berhenti"
        page.update()

    play_btn = ft.ElevatedButton("MULAI PLAY", icon=ft.icons.PLAY_ARROW, on_click=play_clicked, bgcolor="#00d2ff", color="black", width=200)
    pause_btn = ft.ElevatedButton("PAUSE", icon=ft.icons.PAUSE, on_click=pause_clicked, bgcolor="#ff3e3e", color="white", width=200, visible=False)
    stop_btn = ft.TextButton("STOP", icon=ft.icons.STOP, on_click=stop_clicked, icon_color="#ff3e3e")

    # Tambahkan ke Page
    page.add(
        ft.Column(
            [
                ft.Text("TERAPI FOKUS SanFK", size=26, weight="bold", color="#00d2ff"),
                ft.Row([alpha_chip, gamma_chip, theta_chip], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=10, color="transparent"),
                pb,
                timer_text,
                status_text,
                ft.Row([f1, f2]),
                ft.Row([a1, a2]),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Aturan Pengguna:", weight="bold", size=14),
                        ft.Text("• Headset Stereo Wajib", size=12),
                        ft.Text("• Volume Nyaman (Max Level 20)", size=12),
                        ft.Text("• Fokus pada satu titik diam", size=12),
                    ]),
                    padding=15, bgcolor="#0a0f1d", border_radius=15, border=ft.border.all(1, "#1e2533")
                ),
                ft.Column([play_btn, pause_btn, stop_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    # Jalankan Background Timer
    threading.Thread(target=timer_task, daemon=True).start()

ft.app(target=main)