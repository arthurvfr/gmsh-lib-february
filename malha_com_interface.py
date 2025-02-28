import gmsh
import tkinter as tk
from tkinter import messagebox
import sys

def gerar_malha():
    try:
        comprimento = float(entry_comprimento.get())
        largura = float(entry_largura.get())
        altura = float(entry_altura.get())
        lc = float(entry_malha.get())

        gmsh.initialize()
        gmsh.model.add("paralelepipedo")

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
        l5 = gmsh.model.geo.addLine(p5, p6)
        l6 = gmsh.model.geo.addLine(p6, p7)
        l7 = gmsh.model.geo.addLine(p7, p8)
        l8 = gmsh.model.geo.addLine(p8, p5)
        l9 = gmsh.model.geo.addLine(p1, p5)
        l10 = gmsh.model.geo.addLine(p2, p6)
        l11 = gmsh.model.geo.addLine(p3, p7)
        l12 = gmsh.model.geo.addLine(p4, p8)

        loop_base = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
        surface_base = gmsh.model.geo.addPlaneSurface([loop_base])

        volume = gmsh.model.geo.extrude([(2, surface_base)], 0, 0, altura)[1][1]

        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(3)
        gmsh.write("malha_interface.msh")

        gmsh.finalize()

        messagebox.showinfo("Sucesso", "Malha gerada com sucesso!")

        gmsh.initialize()
        gmsh.open("malha_interface.msh")
        gmsh.fltk.run()
        gmsh.finalize()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar malha: {e}")
        gmsh.finalize()

root = tk.Tk()
root.title("Gerador de Malha Gmsh")
root.geometry("350x300")

tk.Label(root, text="Comprimento:").pack()
entry_comprimento = tk.Entry(root)
entry_comprimento.pack()
entry_comprimento.insert(0, "2.0")

tk.Label(root, text="Largura:").pack()
entry_largura = tk.Entry(root)
entry_largura.pack()
entry_largura.insert(0, "1.0")

tk.Label(root, text="Altura:").pack()
entry_altura = tk.Entry(root)
entry_altura.pack()
entry_altura.insert(0, "1.0")

tk.Label(root, text="Tamanho do elemento da malha:").pack()
entry_malha = tk.Entry(root)
entry_malha.pack()
entry_malha.insert(0, "0.2")

btn_gerar = tk.Button(root, text="Gerar Malha", command=gerar_malha)
btn_gerar.pack(pady=10)

root.mainloop()
