import gmsh
import tkinter as tk
from tkinter import messagebox, ttk
import sys

def gerar_malha():
    try:
        tipo = tipo_var.get()
        gmsh.initialize()
        gmsh.model.add(tipo)

        if tipo == "Paralelepípedo":
            comprimento = float(entry_comprimento.get())
            largura = float(entry_largura.get())
            altura = float(entry_altura.get())
            lc = float(entry_malha.get())

            p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
            p2 = gmsh.model.geo.addPoint(comprimento, 0, 0, lc)
            p3 = gmsh.model.geo.addPoint(comprimento, largura, 0, lc)
            p4 = gmsh.model.geo.addPoint(0, largura, 0, lc)
            p5 = gmsh.model.geo.addPoint(0, 0, altura, lc)
            p6 = gmsh.model.geo.addPoint(comprimento, 0, altura, lc)
            p7 = gmsh.model.geo.addPoint(comprimento, largura, altura, lc)
            p8 = gmsh.model.geo.addPoint(0, largura, altura, lc)

            l1 = gmsh.model.geo.addLine(p1, p2)
            l2 = gmsh.model.geo.addLine(p2, p3)
            l3 = gmsh.model.geo.addLine(p3, p4)
            l4 = gmsh.model.geo.addLine(p4, p1)

            loop_base = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
            surface_base = gmsh.model.geo.addPlaneSurface([loop_base])
            volume = gmsh.model.geo.extrude([(2, surface_base)], 0, 0, altura)[1][1]

        elif tipo == "Esfera":
            raio = float(entry_raio.get())
            volume = gmsh.model.occ.addSphere(0, 0, 0, raio)
            gmsh.model.occ.synchronize()

        elif tipo == "Cilindro":
            raio = float(entry_raio_cilindro.get())
            altura = float(entry_altura_cilindro.get())
            volume = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, altura, raio)
            gmsh.model.occ.synchronize()

        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(3)
        nome_arquivo = f"malha_{tipo.lower()}.msh"
        gmsh.write(nome_arquivo)
        gmsh.finalize()
        messagebox.showinfo("Sucesso", f"Malha de {tipo} gerada com sucesso!")

        gmsh.initialize()
        gmsh.open(nome_arquivo)
        gmsh.fltk.run()
        gmsh.finalize()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar malha: {e}")
        gmsh.finalize()

def atualizar_campos():
    frame_paralelepipedo.pack_forget()
    frame_esfera.pack_forget()
    frame_cilindro.pack_forget()
    
    if tipo_var.get() == "Paralelepípedo":
        frame_paralelepipedo.pack(pady=10)
    elif tipo_var.get() == "Esfera":
        frame_esfera.pack(pady=10)
    elif tipo_var.get() == "Cilindro":
        frame_cilindro.pack(pady=10)

root = tk.Tk()
root.title("Gerador de Malha Gmsh")
root.geometry("400x500")

tk.Label(root, text="Escolha o tipo de malha:").pack()
tipo_var = tk.StringVar(value="Paralelepípedo")
tipo_menu = ttk.Combobox(root, textvariable=tipo_var, values=["Paralelepípedo", "Esfera", "Cilindro"])
tipo_menu.pack()
tipo_menu.bind("<<ComboboxSelected>>", lambda e: atualizar_campos())

frame_paralelepipedo = tk.Frame(root)
tk.Label(frame_paralelepipedo, text="Comprimento:").pack()
entry_comprimento = tk.Entry(frame_paralelepipedo)
entry_comprimento.pack()
entry_comprimento.insert(0, "2.0")

tk.Label(frame_paralelepipedo, text="Largura:").pack()
entry_largura = tk.Entry(frame_paralelepipedo)
entry_largura.pack()
entry_largura.insert(0, "1.0")

tk.Label(frame_paralelepipedo, text="Altura:").pack()
entry_altura = tk.Entry(frame_paralelepipedo)
entry_altura.pack()
entry_altura.insert(0, "1.0")

frame_esfera = tk.Frame(root)
tk.Label(frame_esfera, text="Raio da Esfera:").pack()
entry_raio = tk.Entry(frame_esfera)
entry_raio.pack()
entry_raio.insert(0, "1.0")

frame_cilindro = tk.Frame(root)
tk.Label(frame_cilindro, text="Raio do Cilindro:").pack()
entry_raio_cilindro = tk.Entry(frame_cilindro)
entry_raio_cilindro.pack()
entry_raio_cilindro.insert(0, "1.0")

tk.Label(frame_cilindro, text="Altura do Cilindro:").pack()
entry_altura_cilindro = tk.Entry(frame_cilindro)
entry_altura_cilindro.pack()
entry_altura_cilindro.insert(0, "2.0")

tk.Label(root, text="Tamanho do elemento da malha:").pack()
entry_malha = tk.Entry(root)
entry_malha.pack()
entry_malha.insert(0, "0.2")

btn_gerar = tk.Button(root, text="Gerar Malha", command=gerar_malha)
btn_gerar.pack(pady=10)

frame_paralelepipedo.pack(pady=10)
root.mainloop()
