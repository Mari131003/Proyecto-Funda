import tkinter as tk
from tkinter import simpledialog, messagebox
import pickle
import os
import random
import threading
import time
from PIL import Image, ImageTk 
import pygame
from pygame import mixer

pygame.mixer.init()
try:    # Cargar sonidos 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SONIDO_GUARDAR = os.path.join(BASE_DIR, "sonido","botonguardar.wav")
    MUSICA_PRINCIPAL = os.path.join(BASE_DIR,"sonido", "musicaprincipal.wav")
    mixer.music.load(MUSICA_PRINCIPAL)  # Música de fondo
    sonido_guardar = mixer.Sound(SONIDO_GUARDAR)  # Sonido al guardar
except Exception as e:
    print(f"Error al cargar sonidos: {e}")
    sonido_guardar = None

ARCHIVO_USUARIOS = "usuarios.pkl"
# === Cargar o crear usuarios ===
def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "rb") as f:
            return pickle.load(f)
    else:
        return {}
def guardar_usuarios(datos):
    with open(ARCHIVO_USUARIOS, "wb") as f:
        pickle.dump(datos, f)

# === Clase principal de la aplicación ===
class JuegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Light Hunt")
        self.centro_ventana(600, 400)
        self.root.configure(bg="#E6951C")
        self.jugadores = cargar_usuarios()
        self.jugador_actual = None
        self.puntaje_actual = 0
        self.juego_activo = False
        try:
            mixer.music.play(-1)  # -1 para loop infinito
            mixer.music.set_volume(0.2)  # Entre 0.0 y 1.0
            sonido_guardar.set_volume(0.7)
        except:
            pass
        self.crear_widgets()
        self.mostrar_menu_principal()

    def centro_ventana(self, ancho, alto):
        screen_ancho = self.root.winfo_screenwidth()
        screen_alto = self.root.winfo_screenheight()
        x = (screen_ancho // 2) - (ancho // 2)
        y = (screen_alto // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def centrar_ventana(self, ventana, ancho, alto):
        screen_ancho = ventana.winfo_screenwidth()
        screen_alto = ventana.winfo_screenheight()
        x = (screen_ancho // 2) - (ancho // 2)
        y = (screen_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        self.frame.configure(bg="#E6951C")

    def limpiar_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self):
        self.limpiar_frame()
        tk.Label(self.frame, text="Seleccione o Cree su perfil",bg="#E6951C", fg="white",font=("Arial", 16,"bold")).pack(pady=10)
        tk.Button(self.frame,text="➕ Nuevo Perfil",bg="#E6951C",fg="white",font=("Arial", 12,"bold"),width=25,command=self.crear_perfil
        ).pack(pady=5)
        tk.Button(self.frame,text="👥 Usuarios Registrados",bg="#E6951C",fg="white",font=("Arial", 12,"bold"),width=25,command=self.abrir_ventana_usuarios
        ).pack(pady=5)
        tk.Button(self.frame,text="🏆 Ver Ranking",bg="#E6951C",fg="white",font=("Arial", 12,"bold"),width=25,command=self.ver_ranking
        ).pack(pady=5)

    def abrir_ventana_usuarios(self):
        VentanaUsuarios(self.root, self.jugadores, self)

    def seleccionar_perfil(self, nombre):
        self.jugador_actual = nombre
        self.iniciar_juego()
        
    def crear_perfil(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("➕ Nuevo Perfil")
        ventana.geometry("600x600")  # Tamaño aumentado
        ventana.transient(self.root)
        ventana.configure(bg="#E6951C")
        ventana.grab_set()
        self.centrar_ventana(ventana, 600, 600) 
        frame_nuevo = tk.Frame(ventana)
        frame_nuevo.pack(fill="both", expand=True, padx=20, pady=20)
        frame_nuevo.configure(bg="#E6951C")
        tk.Label(frame_nuevo, text="Crear nuevo perfil", bg="#E6951C",fg="white",font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(frame_nuevo, text="Ingrese su nombre:", bg="#E6951C",fg="white",font=("Arial", 12,"bold")).pack(anchor="w")
        entry_nombre = tk.Entry(frame_nuevo, font=("Arial", 12), width=30)
        entry_nombre.pack(pady=10, fill="x")
        tk.Label(frame_nuevo, text="Seleccione un avatar:", bg="#E6951C",fg="white",font=("Arial", 12,"bold")).pack(anchor="w", pady=(10, 5))
        avatares = ["avatar1.png", "avatar2.png", "avatar3.png",
                    "avatar4.png", "avatar5.png", "avatar6.png"]
        avatar_seleccionado = tk.StringVar(value=avatares[0])
        frame_avatares = tk.Frame(frame_nuevo)
        frame_avatares.pack(pady=10)
        frame_avatares.configure(bg="#E6951C")
        frame_seleccion = tk.Frame(frame_nuevo)
        frame_seleccion.pack(pady=5)
        frame_seleccion.config(bg="#E6951C")
        lbl_seleccion = tk.Label(frame_seleccion, text="Avatar seleccionado:",fg="white",font=("Arial", 12,"bold"),bg="#E6951C")
        lbl_seleccion.pack(side="left")
        img_seleccionada = None
        lbl_img_seleccionada = tk.Label(frame_seleccion)
        lbl_img_seleccionada.pack(side="left", padx=10)

        def actualizar_seleccion(avatar):
            try:
                ruta = os.path.join(os.path.dirname(__file__), "avatares", avatar)
                img = Image.open(ruta).resize((60, 60))
                img_tk = ImageTk.PhotoImage(img)
                lbl_img_seleccionada.config(image=img_tk)
                lbl_img_seleccionada.image = img_tk
                avatar_seleccionado.set(avatar)
            except Exception as e:
                print(f"Error al cargar avatar: {e}")
        for i, avatar in enumerate(avatares): # Cargar y mostrar los avatares como botones con imágenes
            try:
                ruta_imagen = os.path.join(os.path.dirname(__file__), "avatares", avatar)
                imagen = Image.open(ruta_imagen).resize((60, 60))  
                imagen_tk = ImageTk.PhotoImage(imagen)
                btn = tk.Button(frame_avatares,image=imagen_tk,command=lambda a=avatar: actualizar_seleccion(a)
                )
                btn.image = imagen_tk 
                btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)
            except Exception as e:
                print(f"No se pudo cargar {avatar}: {e}")
                btn = tk.Button(frame_avatares,text="❌",font=("Arial", 20),width=4,height=2,command=lambda a=avatar: actualizar_seleccion(a)
                )
                btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)
        actualizar_seleccion(avatares[0])  # Mostrar el primer avatar como seleccionado por defecto
            
        def guardar():
            nombre = entry_nombre.get().strip()
            avatar = avatar_seleccionado.get()
            if nombre and nombre not in self.jugadores:
                if sonido_guardar:
                    sonido_guardar.play()
                self.jugadores[nombre] = {
                    "puntaje_max": 0,
                    "avatar": avatar
                }
                guardar_usuarios(self.jugadores)
                ventana.destroy()
                self.mostrar_menu_principal()
            elif nombre in self.jugadores:
                messagebox.showerror("Error", "El nombre ya existe.")
            else:
                messagebox.showwarning("Cancelado", "Nombre inválido.")
        tk.Button(frame_nuevo,text="Guardar Perfil",font=("Arial", 14),bg="green",fg="white",command=guardar
        ).pack(pady=20)

    def ver_ranking(self):
        self.limpiar_frame()
        tk.Label(self.frame, text="Ranking de Jugadores",bg="#E6951C", fg="white",font=("Arial", 18,"bold")).pack(pady=10)
        jugadores_ordenados = sorted(
            self.jugadores.items(),
            key=lambda x: x[1]["puntaje_max"],
            reverse=True
        )
        if not jugadores_ordenados:
            tk.Label(self.frame, text="No hay jugadores registrados aún.",bg="#E6951C", fg="gray").pack()
        else:
            for idx, (nombre, info) in enumerate(jugadores_ordenados[:10]):
                tk.Label(
                    self.frame,
                    text=f"{idx + 1}. {nombre} - {info['puntaje_max']}",
                    font=("Arial", 14,"bold"),
                    fg="white",
                    bg="#E6951C"
                ).pack()
        tk.Button(self.frame, text="🔙 Volver",bg="#E6951C",fg="white", font=("Arial", 12,"bold"), command=self.mostrar_menu_principal).pack(pady=10)

    def iniciar_juego(self):
        self.limpiar_frame()
        ruta_avatar = os.path.join("avatares", self.jugadores[self.jugador_actual]["avatar"])
        try:
            imagen = Image.open(ruta_avatar).resize((60, 60))
            imagen_tk = ImageTk.PhotoImage(imagen)
            lbl_avatar = tk.Label(self.frame, image=imagen_tk)
            lbl_avatar.image = imagen_tk
            lbl_avatar.pack(pady=10)
        except Exception as e:
            tk.Label(self.frame, font=("Arial", 30)).pack(pady=10)
            tk.Label(self.frame, text=f"Jugador: {self.jugador_actual}",bg="#E6951C",fg="white", font=("Arial", 14,"bold")).pack(pady=10)
        self.lbl_score = tk.Label(self.frame, text="Score: 0",bg="#E6951C",fg="white", font=("Arial", 16,"bold"))
        self.lbl_score.pack(pady=10)
        self.btn_iniciar = tk.Button(self.frame, text="▶️ Iniciar Partida",bg="#E6951C",fg="white", font=("Arial", 12,"bold"), command=self.comenzar_partida)
        self.btn_iniciar.pack(pady=10)
        tk.Button(self.frame, text="🔚 Salir al Menú",bg="#E6951C",fg="white", font=("Arial", 12,"bold"),command=self.mostrar_menu_principal).pack(pady=5)

    def comenzar_partida(self):
        self.btn_iniciar.config(state=tk.DISABLED)
        self.puntaje_actual = 0
        self.juego_activo = True
        self.actualizar_puntaje()

    def actualizar_puntaje(self):
        if not self.juego_activo:
            return
        self.puntaje_actual += 1
        self.lbl_score.config(text=f"Score: {self.puntaje_actual}")
        if random.random() < 0.05:
            self.finalizar_partida()
        else:
            self.root.after(500, self.actualizar_puntaje)

    def finalizar_partida(self):
        self.juego_activo = False
        self.btn_iniciar.config(state=tk.NORMAL)
        if self.puntaje_actual > self.jugadores[self.jugador_actual]["puntaje_max"]:
            self.jugadores[self.jugador_actual]["puntaje_max"] = self.puntaje_actual
            guardar_usuarios(self.jugadores)
        respuesta = messagebox.askyesno(
            "Fin de la partida",
            f"Tu puntaje fue: {self.puntaje_actual}\n¿Jugar nuevamente con este perfil?"
        )
        if not respuesta:
            self.mostrar_menu_principal()

# === Ventana emergente para mostrar usuarios ===
class VentanaUsuarios:
    def __init__(self, parent, jugadores, app):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("👥 Usuarios Registrados")
        self.ventana.geometry("600x600")
        self.ventana.configure(bg="#E6951C")
        self.app = app  # Referencia a la aplicación principal
        self.jugadores = jugadores.copy()  # Hacemos una copia para no afectar directamente
        self.centro_ventana(600, 400)
        self.frame_contenido = tk.Frame(self.ventana)
        self.frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)
        self.frame_contenido.configure(bg="#E6951C")
        tk.Label(self.frame_contenido, text="Usuarios Registrados",bg="#E6951C",fg="white", font=("Arial", 12,"bold")).pack(pady=10)
        self.lista_frame = tk.Frame(self.frame_contenido) # Definimos lista_frame aquí, como atributo de la clase
        self.lista_frame.pack(fill="both", expand=True)
        self.mostrar_usuarios()
        tk.Button(self.ventana, text="Cerrar",bg="#E6951C",fg="white", font=("Arial", 12,"bold"),width=15, command=self.ventana.destroy).pack(pady=10)

    def mostrar_usuarios(self):
        """Muestra la lista de usuarios con sus avatares."""
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        if not self.jugadores:
            tk.Label(self.lista_frame, text="No hay usuarios registrados.", fg="white").pack(pady=20)
            return
        for nombre, info in self.jugadores.items():
            frame_usuario = tk.Frame(self.lista_frame)
            frame_usuario.pack(fill="x", pady=5)
            avatar = info.get("avatar", "avatar1.png")
            ruta_imagen = os.path.join(os.path.dirname(__file__), "avatares", avatar)
            try:
                imagen = Image.open(ruta_imagen).resize((40, 40))
                imagen_tk = ImageTk.PhotoImage(imagen)
                lbl_avatar = tk.Label(frame_usuario, image=imagen_tk, text="", width=45, height=45)
                lbl_avatar.image = imagen_tk
                lbl_avatar.pack(side="left", padx=5)
            except Exception as e:
                tk.Label(frame_usuario, text="🖼️", width=5).pack(side="left", padx=5)
            tk.Button(frame_usuario,
                text=f"{nombre}\nPuntaje Máximo: {info['puntaje_max']}",width=30,anchor="w",command=lambda n=nombre: self.seleccionar_usuario(n)
            ).pack(side="left", padx=5)
            tk.Button(frame_usuario,text="🗑️",width=3,fg="red",command=lambda n=nombre, f=frame_usuario: self.confirmar_eliminacion(n, f)
            ).pack(side="left", padx=5)

    def centro_ventana(self, ancho, alto):
        screen_ancho = self.ventana.winfo_screenwidth()
        screen_alto = self.ventana.winfo_screenheight()
        x = (screen_ancho // 2) - (ancho // 2)
        y = (screen_alto // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def seleccionar_usuario(self, nombre):
        self.ventana.destroy()
        self.app.seleccionar_perfil(nombre)

    def confirmar_eliminacion(self, nombre, frame_usuario):
        """Muestra botones Sí/No en lugar del botón de eliminar."""
        for widget in frame_usuario.winfo_children():
            widget.destroy()
        tk.Label(frame_usuario, text=f"¿Eliminar '{nombre}'?", width=30, anchor="w").pack(side="left", padx=5)
        tk.Button(frame_usuario,text="✔️",width=3,fg="green",command=lambda: self.eliminar_usuario(nombre)
        ).pack(side="left", padx=2)
        tk.Button(frame_usuario,text="❌",width=3,fg="red",command=self.mostrar_usuarios
        ).pack(side="left", padx=2)
 
    def eliminar_usuario(self, nombre):
        confirmacion = messagebox.askyesno(
            "Eliminar Usuario",
            f"¿Está seguro de eliminar el perfil de '{nombre}'?\nEsta acción no se puede deshacer."
        )
        if confirmacion:
            del self.jugadores[nombre]  # Elimina del diccionario temporal
            guardar_usuarios(self.jugadores)  # Guarda los cambios en el archivo
            # Recarga los usuarios desde el archivo
            self.app.jugadores = cargar_usuarios()  # ⬅️ Actualiza la lista completa en la app principal
            messagebox.showinfo("Usuario Eliminado", f"El perfil de '{nombre}' ha sido eliminado.")
            self.mostrar_usuarios()  # Vuelve a mostrar la lista actualizada

# === Iniciar Aplicación ===
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoApp(root)
    root.mainloop()