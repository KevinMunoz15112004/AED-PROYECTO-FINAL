import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from datetime import datetime
import random

def validar_telefono(telefono):
    return telefono.isdigit() and len(telefono) == 10

def validar_texto(texto):
    texto = texto.strip()
    return all(char.isalpha() or char.isspace() for char in texto) and texto != ""

def validar_producto(producto):
    partes = producto.split(",")
    if len(partes) != 3:
        return False
    nombre = partes[0].strip()
    cantidad = partes[1].strip()
    valor_unitario = partes[2].strip()
    if not (nombre and cantidad and valor_unitario):
        return False
    if not cantidad.isdigit() or int(cantidad) <= 0:
        return False
    try:
        float(valor_unitario)
    except ValueError:
        return False
    return True

def validar_cedula(cedula):
    return cedula.isdigit() and len(cedula) == 10

def validar_campos():
    if not (empresa_var.get() and fecha_var.get() and proveedor_var.get() and
            direccion_proveedor_var.get() and telefono_proveedor_var.get() and
            cedula_proveedor_var.get() and cliente_var.get() and
            direccion_cliente_var.get() and telefono_cliente_var.get() and
            cedula_cliente_var.get() and forma_pago_var.get()):
        messagebox.showwarning("Campos Obligatorios", "Todos los campos deben ser llenados.")
        return False

    if not validar_telefono(telefono_proveedor_var.get()):
        messagebox.showwarning("Número de Teléfono", "El teléfono del proveedor debe ser un número de 10 dígitos.")
        return False
    
    if not validar_telefono(telefono_cliente_var.get()):
        messagebox.showwarning("Número de Teléfono", "El teléfono del cliente debe ser un número de 10 dígitos.")
        return False

    if not validar_texto(proveedor_var.get()):
        messagebox.showwarning("Nombre del Proveedor", "El nombre del proveedor solo debe contener texto.")
        return False

    if not validar_texto(cliente_var.get()):
        messagebox.showwarning("Nombre del Cliente", "El nombre del cliente solo debe contener texto.")
        return False

    if not validar_cedula(cedula_proveedor_var.get()):
        messagebox.showwarning("Número de Cédula del Proveedor", "La cédula del proveedor debe ser un número de 10 dígitos.")
        return False
    
    if not validar_cedula(cedula_cliente_var.get()):
        messagebox.showwarning("Número de Cédula del Cliente", "La cédula del cliente debe ser un número de 10 dígitos.")
        return False

    productos = productos_text.get("1.0", tk.END).strip().split("\n")
    for producto in productos:
        if not validar_producto(producto):
            messagebox.showwarning("Formato de Productos", "Cada producto debe seguir el formato: Producto, Cantidad (mayor a 0), Valor Unitario.")
            return False

    return True

def limpiar_campos():
    empresa_var.set("")
    fecha_var.set(datetime.now().strftime("%Y-%m-%d"))
    proveedor_var.set("")
    direccion_proveedor_var.set("")
    telefono_proveedor_var.set("")
    cedula_proveedor_var.set("")
    cliente_var.set("")
    direccion_cliente_var.set("")
    telefono_cliente_var.set("")
    cedula_cliente_var.set("")
    forma_pago_var.set("")
    productos_text.delete("1.0", tk.END)

def generar_factura():
    if not validar_campos():
        return

    datos_factura = {
        "numero_factura": f"{random.randint(1, 9999):04d}",
        "empresa": empresa_var.get(),
        "fecha": fecha_var.get(),
        "proveedor": proveedor_var.get(),
        "direccion_proveedor": direccion_proveedor_var.get(),
        "telefono_proveedor": telefono_proveedor_var.get(),
        "cedula_proveedor": cedula_proveedor_var.get(),
        "cliente": cliente_var.get(),
        "direccion_cliente": direccion_cliente_var.get(),
        "telefono_cliente": telefono_cliente_var.get(),
        "cedula_cliente": cedula_cliente_var.get(),
        "productos": [],
        "forma_pago": forma_pago_var.get()
    }

    productos = productos_text.get("1.0", tk.END).strip().split("\n")
    total_sin_iva = 0

    for producto in productos:
        try:
            nombre, cantidad, valor_unitario = producto.split(",")
            cantidad = int(cantidad.strip())
            valor_unitario = float(valor_unitario.strip())
            valor_total = cantidad * valor_unitario
            total_sin_iva += valor_total
            datos_factura["productos"].append({
                "nombre": nombre.strip(),
                "cantidad": cantidad,
                "valor_unitario": valor_unitario,
                "valor_total": valor_total
            })
        except ValueError:
            continue

    iva = total_sin_iva * 0.15
    total_con_iva = total_sin_iva + iva

    if datos_factura["forma_pago"] == "Tarjeta":
        total_con_iva *= 1.18

    datos_factura["subtotal"] = total_sin_iva
    datos_factura["iva"] = iva
    datos_factura["total_con_iva"] = total_con_iva

    # Guardar en archivo .txt
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if archivo:
        with open(archivo, "w") as file:
            file.write(f"Numero de Factura: {datos_factura['numero_factura']}\n")
            file.write(f"{'-'*70}\n")
            file.write(f"Nombre de la Empresa: {datos_factura['empresa']}\n")
            file.write(f"Fecha: {datos_factura['fecha']}\n")
            file.write(f"{'-'*70}\n")
            file.write(f"Datos del Proveedor:\n")
            file.write(f"Nombre: {datos_factura['proveedor']}\n")
            file.write(f"Dirección: {datos_factura['direccion_proveedor']}\n")
            file.write(f"Teléfono: {datos_factura['telefono_proveedor']}\n")
            file.write(f"Cédula: {datos_factura['cedula_proveedor']}\n")
            file.write(f"{'-'*70}\n")
            file.write(f"Datos del Cliente:\n")
            file.write(f"Nombre: {datos_factura['cliente']}\n")
            file.write(f"Dirección: {datos_factura['direccion_cliente']}\n")
            file.write(f"Teléfono: {datos_factura['telefono_cliente']}\n")
            file.write(f"Cédula: {datos_factura['cedula_cliente']}\n")
            file.write(f"{'-'*70}\n")
            file.write(f"Productos:\n")
            file.write(f"{'Producto':<25} {'Cantidad':<10} {'Valor Unitario':>15} {'Valor Total':>15}\n")
            file.write(f"{'-'*70}\n")
            for prod in datos_factura["productos"]:
                file.write(f"{prod['nombre']:<25} {prod['cantidad']:<10} {prod['valor_unitario']:>15.2f} {prod['valor_total']:>15.2f}\n")
            file.write(f"{'-'*70}\n")
            file.write(f"Subtotal: {datos_factura['subtotal']:.2f}\n")
            file.write(f"IVA (15%): {datos_factura['iva']:.2f}\n")
            file.write(f"Total con IVA: {datos_factura['total_con_iva']:.2f}\n")
            file.write(f"Forma de Pago: {datos_factura['forma_pago']}\n")
        messagebox.showinfo("Factura Generada", "La factura se ha guardado correctamente.")
        limpiar_campos()

def cargar_factura():
    archivo = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if archivo:
        with open(archivo, "r") as file:
            factura_texto = file.read()
        mostrar_factura(factura_texto)

def mostrar_factura(factura_texto):
    ventana_factura = tk.Toplevel(root)
    ventana_factura.title("Factura Cargada")
    texto = tk.Text(ventana_factura, wrap=tk.WORD, width=80, height=20)
    texto.insert(tk.END, factura_texto)
    texto.pack()

def crear_botones(root, generador_callback, cargador_callback):
    ttk.Button(root, text="Generar Factura", command=generador_callback).grid(row=12, column=0, pady=10)
    ttk.Button(root, text="Cargar Factura", command=cargador_callback).grid(row=12, column=1, pady=10)

def crear_formulario(root):
    global empresa_var, fecha_var, proveedor_var, direccion_proveedor_var, telefono_proveedor_var, cedula_proveedor_var
    global cliente_var, direccion_cliente_var, telefono_cliente_var, cedula_cliente_var, forma_pago_var, productos_text
    
    # Empresa
    ttk.Label(root, text="Nombre de la Empresa:").grid(row=0, column=0, sticky="w")
    empresa_var = tk.StringVar()
    ttk.Entry(root, textvariable=empresa_var).grid(row=0, column=1)

    # Fecha
    ttk.Label(root, text="Fecha:").grid(row=1, column=0, sticky="w")
    fecha_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    ttk.Entry(root, textvariable=fecha_var).grid(row=1, column=1)

    # Datos del Proveedor
    ttk.Label(root, text="Nombre del Proveedor:").grid(row=2, column=0, sticky="w")
    proveedor_var = tk.StringVar()
    ttk.Entry(root, textvariable=proveedor_var).grid(row=2, column=1)

    # Dirección del Proveedor
    ttk.Label(root, text="Dirección del Proveedor:").grid(row=3, column=0, sticky="w")
    direccion_proveedor_var = tk.StringVar()
    ttk.Entry(root, textvariable=direccion_proveedor_var).grid(row=3, column=1)

    # Teléfono del Proveedor
    ttk.Label(root, text="Teléfono del Proveedor:").grid(row=4, column=0, sticky="w")
    telefono_proveedor_var = tk.StringVar()
    ttk.Entry(root, textvariable=telefono_proveedor_var).grid(row=4, column=1)

    # Cédula del Proveedor
    ttk.Label(root, text="Cédula del Proveedor:").grid(row=5, column=0, sticky="w")
    cedula_proveedor_var = tk.StringVar()
    ttk.Entry(root, textvariable=cedula_proveedor_var).grid(row=5, column=1)

    # Datos del Cliente
    ttk.Label(root, text="Nombre del Cliente:").grid(row=6, column=0, sticky="w")
    cliente_var = tk.StringVar()
    ttk.Entry(root, textvariable=cliente_var).grid(row=6, column=1)

    # Dirección del Cliente
    ttk.Label(root, text="Dirección del Cliente:").grid(row=7, column=0, sticky="w")
    direccion_cliente_var = tk.StringVar()
    ttk.Entry(root, textvariable=direccion_cliente_var).grid(row=7, column=1)

    # Teléfono del Cliente
    ttk.Label(root, text="Teléfono del Cliente:").grid(row=8, column=0, sticky="w")
    telefono_cliente_var = tk.StringVar()
    ttk.Entry(root, textvariable=telefono_cliente_var).grid(row=8, column=1)

    # Cédula del Cliente
    ttk.Label(root, text="Cédula del Cliente:").grid(row=9, column=0, sticky="w")
    cedula_cliente_var = tk.StringVar()
    ttk.Entry(root, textvariable=cedula_cliente_var).grid(row=9, column=1)

    # Productos
    ttk.Label(root, text="Productos (Formato: Producto, Cantidad, Valor Unitario):").grid(row=10, column=0, sticky="w")
    productos_text = tk.Text(root, height=5, width=40)
    productos_text.grid(row=10, column=1)

    # Forma de Pago
    ttk.Label(root, text="Forma de Pago:").grid(row=11, column=0, sticky="w")
    forma_pago_var = tk.StringVar()
    ttk.Radiobutton(root, text="Efectivo", variable=forma_pago_var, value="Efectivo").grid(row=11, column=1, sticky="w")
    ttk.Radiobutton(root, text="Tarjeta", variable=forma_pago_var, value="Tarjeta").grid(row=11, column=1, sticky="e")

def main():
    global root
    root = tk.Tk()
    root.title("Generador de Factura")

    crear_formulario(root)
    crear_botones(root, generar_factura, cargar_factura)

    root.mainloop()

main()
