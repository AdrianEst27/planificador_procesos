import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from collections import defaultdict
import random
import copy

class Proceso:
    def __init__(self, nombre, tiempo_llegada, duracion):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.duracion = duracion
        self.tiempo_restante = duracion
        self.tiempo_inicio = 0
        self.tiempo_finalizacion = 0
        self.tiempo_espera = 0
        self.tiempo_respuesta = -1
    
    def __str__(self):
        return f"Proceso {self.nombre}: Llegada={self.tiempo_llegada}, Duración={self.duracion}"

class PlanificadorProcesos:
    def __init__(self):
        self.procesos = []
        self.quantum = 3
        
    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)
    
    def limpiar_procesos(self):
        self.procesos = []
    
    def fifo(self):
        """Algoritmo First In First Out"""
        procesos = sorted(copy.deepcopy(self.procesos), key=lambda x: x.tiempo_llegada)
        tiempo_actual = 0
        secuencia = []
        
        for proceso in procesos:
            if tiempo_actual < proceso.tiempo_llegada:
                tiempo_actual = proceso.tiempo_llegada
            
            proceso.tiempo_inicio = tiempo_actual
            proceso.tiempo_finalizacion = tiempo_actual + proceso.duracion
            proceso.tiempo_espera = proceso.tiempo_inicio - proceso.tiempo_llegada
            proceso.tiempo_respuesta = proceso.tiempo_espera
            
            secuencia.append({
                'proceso': proceso.nombre,
                'inicio': tiempo_actual,
                'fin': proceso.tiempo_finalizacion
            })
            
            tiempo_actual = proceso.tiempo_finalizacion
        
        return procesos, secuencia
    
    def sjf(self):
        """Algoritmo Shortest Job First"""
        procesos = copy.deepcopy(self.procesos)
        tiempo_actual = 0
        secuencia = []
        completados = []
        pendientes = []
        
        while len(completados) < len(procesos):
            # Agregar procesos que han llegado
            for proceso in procesos:
                if (proceso.tiempo_llegada <= tiempo_actual and 
                    proceso not in completados and 
                    proceso not in pendientes):
                    pendientes.append(proceso)
            
            if not pendientes:
                # Si no hay procesos pendientes, avanzar al siguiente tiempo de llegada
                siguiente_llegada = min([p.tiempo_llegada for p in procesos if p not in completados])
                tiempo_actual = siguiente_llegada
                continue
            
            # Seleccionar el proceso con menor duración
            proceso_actual = min(pendientes, key=lambda x: x.duracion)
            pendientes.remove(proceso_actual)
            
            proceso_actual.tiempo_inicio = tiempo_actual
            proceso_actual.tiempo_finalizacion = tiempo_actual + proceso_actual.duracion
            proceso_actual.tiempo_espera = proceso_actual.tiempo_inicio - proceso_actual.tiempo_llegada
            proceso_actual.tiempo_respuesta = proceso_actual.tiempo_espera
            
            secuencia.append({
                'proceso': proceso_actual.nombre,
                'inicio': tiempo_actual,
                'fin': proceso_actual.tiempo_finalizacion
            })
            
            tiempo_actual = proceso_actual.tiempo_finalizacion
            completados.append(proceso_actual)
        
        return completados, secuencia
    
    def round_robin(self):
        """Algoritmo Round Robin"""
        procesos = copy.deepcopy(self.procesos)
        tiempo_actual = 0
        secuencia = []
        cola = []
        completados = []
        procesos_ordenados = sorted(procesos, key=lambda x: x.tiempo_llegada)
        indice_proceso = 0
        
        while len(completados) < len(procesos):
            # Agregar procesos que han llegado a la cola
            while (indice_proceso < len(procesos_ordenados) and 
                   procesos_ordenados[indice_proceso].tiempo_llegada <= tiempo_actual):
                cola.append(procesos_ordenados[indice_proceso])
                indice_proceso += 1
            
            if not cola:
                # Si no hay procesos en cola, avanzar al siguiente tiempo de llegada
                if indice_proceso < len(procesos_ordenados):
                    tiempo_actual = procesos_ordenados[indice_proceso].tiempo_llegada
                continue
            
            proceso_actual = cola.pop(0)
            
            # Establecer tiempo de respuesta si es la primera vez que se ejecuta
            if proceso_actual.tiempo_respuesta == -1:
                proceso_actual.tiempo_respuesta = tiempo_actual - proceso_actual.tiempo_llegada
            
            # Determinar tiempo de ejecución
            tiempo_ejecucion = min(self.quantum, proceso_actual.tiempo_restante)
            tiempo_inicio_segmento = tiempo_actual
            tiempo_actual += tiempo_ejecucion
            proceso_actual.tiempo_restante -= tiempo_ejecucion
            
            secuencia.append({
                'proceso': proceso_actual.nombre,
                'inicio': tiempo_inicio_segmento,
                'fin': tiempo_actual
            })
            
            # Agregar nuevos procesos que han llegado durante la ejecución
            while (indice_proceso < len(procesos_ordenados) and 
                   procesos_ordenados[indice_proceso].tiempo_llegada <= tiempo_actual):
                cola.append(procesos_ordenados[indice_proceso])
                indice_proceso += 1
            
            if proceso_actual.tiempo_restante > 0:
                # El proceso no ha terminado, volver a la cola
                cola.append(proceso_actual)
            else:
                # El proceso ha terminado
                proceso_actual.tiempo_finalizacion = tiempo_actual
                proceso_actual.tiempo_espera = (proceso_actual.tiempo_finalizacion - 
                                               proceso_actual.tiempo_llegada - 
                                               proceso_actual.duracion)
                completados.append(proceso_actual)
        
        return completados, secuencia

class InterfazSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Planificador de Procesos - Jesús Adrián Salas Estrada - Sistemas Operativos")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.planificador = PlanificadorProcesos()
        self.colores_procesos = {}
        
        self.crear_interfaz()
        self.cargar_ejemplo()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Simulador de Planificador de Procesos", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de entrada de datos
        entrada_frame = ttk.LabelFrame(main_frame, text="Entrada de Procesos", padding="10")
        entrada_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Campos de entrada
        ttk.Label(entrada_frame, text="Nombre del Proceso:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.nombre_entry = ttk.Entry(entrada_frame, width=15)
        self.nombre_entry.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(entrada_frame, text="Tiempo de Llegada:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.llegada_entry = ttk.Entry(entrada_frame, width=15)
        self.llegada_entry.grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(entrada_frame, text="Duración (CPU Burst):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.duracion_entry = ttk.Entry(entrada_frame, width=15)
        self.duracion_entry.grid(row=2, column=1, pady=2, padx=5)
        
        # Quantum para Round Robin
        ttk.Label(entrada_frame, text="Quantum (Round Robin):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.quantum_entry = ttk.Entry(entrada_frame, width=15)
        self.quantum_entry.insert(0, "3")
        self.quantum_entry.grid(row=3, column=1, pady=2, padx=5)
        
        # Botones
        botones_frame = ttk.Frame(entrada_frame)
        botones_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(botones_frame, text="Agregar Proceso", 
                  command=self.agregar_proceso).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Limpiar Todo", 
                  command=self.limpiar_todo).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Cargar Ejemplo", 
                  command=self.cargar_ejemplo).pack(side=tk.LEFT, padx=5)
        
        # Lista de procesos
        lista_frame = ttk.LabelFrame(entrada_frame, text="Procesos Ingresados", padding="5")
        lista_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.lista_procesos = tk.Listbox(lista_frame, height=6)
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.lista_procesos.yview)
        self.lista_procesos.configure(yscrollcommand=scrollbar.set)
        
        self.lista_procesos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de control y resultados
        control_frame = ttk.LabelFrame(main_frame, text="Control y Algoritmos", padding="10")
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones de algoritmos
        algoritmos_frame = ttk.Frame(control_frame)
        algoritmos_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(algoritmos_frame, text="Ejecutar FIFO", 
                  command=lambda: self.ejecutar_algoritmo('FIFO')).pack(side=tk.LEFT, padx=5)
        ttk.Button(algoritmos_frame, text="Ejecutar SJF", 
                  command=lambda: self.ejecutar_algoritmo('SJF')).pack(side=tk.LEFT, padx=5)
        ttk.Button(algoritmos_frame, text="Ejecutar Round Robin", 
                  command=lambda: self.ejecutar_algoritmo('RR')).pack(side=tk.LEFT, padx=5)
        ttk.Button(algoritmos_frame, text="Comparar Todos", 
                  command=self.comparar_algoritmos).pack(side=tk.LEFT, padx=5)
        
        # Área de resultados
        self.resultado_text = scrolledtext.ScrolledText(control_frame, height=15, width=50)
        self.resultado_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame para gráficos
        grafico_frame = ttk.LabelFrame(main_frame, text="Diagrama de Gantt", padding="10")
        grafico_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Canvas para matplotlib
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, grafico_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def agregar_proceso(self):
        try:
            nombre = self.nombre_entry.get().strip()
            llegada = int(self.llegada_entry.get())
            duracion = int(self.duracion_entry.get())
            
            if not nombre:
                messagebox.showerror("Error", "El nombre del proceso es obligatorio")
                return
            
            if llegada < 0 or duracion <= 0:
                messagebox.showerror("Error", "Los tiempos deben ser positivos")
                return
            
            proceso = Proceso(nombre, llegada, duracion)
            self.planificador.agregar_proceso(proceso)
            
            # Asignar color aleatorio al proceso
            if nombre not in self.colores_procesos:
                self.colores_procesos[nombre] = f"#{random.randint(0, 0xFFFFFF):06x}"
            
            self.actualizar_lista_procesos()
            self.limpiar_campos()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.llegada_entry.delete(0, tk.END)
        self.duracion_entry.delete(0, tk.END)
    
    def limpiar_todo(self):
        self.planificador.limpiar_procesos()
        self.colores_procesos.clear()
        self.actualizar_lista_procesos()
        self.resultado_text.delete(1.0, tk.END)
        self.ax.clear()
        self.canvas.draw()
    
    def cargar_ejemplo(self):
        """Cargar procesos de ejemplo para demostración"""
        self.limpiar_todo()
        
        procesos_ejemplo = [
            Proceso("P1", random.randint(0, 4), random.randint(1, 9)),
            Proceso("P2", random.randint(0, 4), random.randint(1, 9)),
            Proceso("P3", random.randint(0, 4), random.randint(1, 9)),
            Proceso("P4", random.randint(0, 4), random.randint(1, 9)),
            Proceso("P5", random.randint(0, 4), random.randint(1, 9))
        ]
        
        for proceso in procesos_ejemplo:
            self.planificador.agregar_proceso(proceso)
            self.colores_procesos[proceso.nombre] = f"#{random.randint(0, 0xFFFFFF):06x}"
        
        self.actualizar_lista_procesos()
    
    def actualizar_lista_procesos(self):
        self.lista_procesos.delete(0, tk.END)
        for proceso in self.planificador.procesos:
            self.lista_procesos.insert(tk.END, 
                f"{proceso.nombre}: Llegada={proceso.tiempo_llegada}, Duración={proceso.duracion}")
    
    def ejecutar_algoritmo(self, algoritmo):
        if not self.planificador.procesos:
            messagebox.showwarning("Advertencia", "No hay procesos para planificar")
            return
        
        try:
            self.planificador.quantum = int(self.quantum_entry.get())
        except ValueError:
            self.planificador.quantum = 3
        
        if algoritmo == 'FIFO':
            procesos, secuencia = self.planificador.fifo()
            titulo = "First In First Out (FIFO)"
        elif algoritmo == 'SJF':
            procesos, secuencia = self.planificador.sjf()
            titulo = "Shortest Job First (SJF)"
        elif algoritmo == 'RR':
            procesos, secuencia = self.planificador.round_robin()
            titulo = "Round Robin"
        
        self.mostrar_resultados(procesos, secuencia, titulo)
        self.dibujar_gantt(secuencia, titulo)
    
    def mostrar_resultados(self, procesos, secuencia, algoritmo):
        self.resultado_text.delete(1.0, tk.END)
        
        resultado = f"=== RESULTADOS DEL ALGORITMO {algoritmo} ===\n\n"
        
        if algoritmo == "Round Robin":
            resultado += f"Quantum utilizado: {self.planificador.quantum}\n\n"
        
        resultado += "SECUENCIA DE EJECUCIÓN:\n"
        for seg in secuencia:
            resultado += f"{seg['proceso']}: {seg['inicio']} -> {seg['fin']}\n"
        
        resultado += "\nMÉTRICAS POR PROCESO:\n"
        resultado += f"{'Proceso':<10} {'Llegada':<8} {'Duración':<9} {'Finalización':<12} {'Espera':<8} {'Respuesta':<10}\n"
        resultado += "-" * 70 + "\n"
        
        tiempo_total_espera = 0
        tiempo_total_respuesta = 0
        
        for proceso in procesos:
            tiempo_total_espera += proceso.tiempo_espera
            tiempo_total_respuesta += proceso.tiempo_respuesta
            resultado += f"{proceso.nombre:<10} {proceso.tiempo_llegada:<8} {proceso.duracion:<9} {proceso.tiempo_finalizacion:<12} {proceso.tiempo_espera:<8} {proceso.tiempo_respuesta:<10}\n"
        
        # Calcular promedios
        n_procesos = len(procesos)
        tiempo_promedio_espera = tiempo_total_espera / n_procesos
        tiempo_promedio_respuesta = tiempo_total_respuesta / n_procesos
        
        resultado += f"\nRESUMEN:\n"
        resultado += f"Tiempo promedio de espera: {tiempo_promedio_espera:.2f}\n"
        resultado += f"Tiempo promedio de respuesta: {tiempo_promedio_respuesta:.2f}\n"
        resultado += f"Tiempo total de finalización: {max(seg['fin'] for seg in secuencia)}\n"
        
        self.resultado_text.insert(tk.END, resultado)
    
    def dibujar_gantt(self, secuencia, titulo):
        self.ax.clear()
        self.ax.set_title(f"Diagrama de Gantt - {titulo}", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel("Procesos")
        
        # Obtener lista única de procesos
        procesos_unicos = list(set(seg['proceso'] for seg in secuencia))
        procesos_unicos.sort()
        
        # Dibujar barras para cada segmento
        for i, seg in enumerate(secuencia):
            proceso = seg['proceso']
            inicio = seg['inicio']
            duracion = seg['fin'] - seg['inicio']
            
            # Encontrar posición Y del proceso
            y_pos = procesos_unicos.index(proceso)
            
            # Obtener color del proceso
            color = self.colores_procesos.get(proceso, '#3498db')
            
            # Dibujar rectángulo
            rect = patches.Rectangle((inicio, y_pos), duracion, 0.8, 
                                   linewidth=1, edgecolor='black', 
                                   facecolor=color, alpha=0.8)
            self.ax.add_patch(rect)
            
            # Agregar texto con el nombre del proceso
            self.ax.text(inicio + duracion/2, y_pos + 0.4, proceso, 
                        ha='center', va='center', fontweight='bold', fontsize=9)
            
            # Agregar tiempo en la parte inferior
            self.ax.text(inicio + duracion/2, y_pos + 0.1, f"{duracion}", 
                        ha='center', va='center', fontsize=8)
        
        # Configurar ejes
        self.ax.set_yticks(range(len(procesos_unicos)))
        self.ax.set_yticklabels(procesos_unicos)
        self.ax.set_xlim(0, max(seg['fin'] for seg in secuencia))
        self.ax.set_ylim(-0.5, len(procesos_unicos) - 0.5)
        
        # Agregar líneas de tiempo
        tiempo_max = max(seg['fin'] for seg in secuencia)
        for t in range(0, tiempo_max + 1):
            self.ax.axvline(x=t, color='gray', linestyle='--', alpha=0.3)
        
        self.ax.grid(True, alpha=0.3)
        plt.tight_layout()
        self.canvas.draw()
    
    def comparar_algoritmos(self):
        if not self.planificador.procesos:
            messagebox.showwarning("Advertencia", "No hay procesos para planificar")
            return
        
        try:
            self.planificador.quantum = int(self.quantum_entry.get())
        except ValueError:
            self.planificador.quantum = 3
        
        # Ejecutar todos los algoritmos
        procesos_fifo, secuencia_fifo = self.planificador.fifo()
        procesos_sjf, secuencia_sjf = self.planificador.sjf()
        procesos_rr, secuencia_rr = self.planificador.round_robin()
        
        # Calcular métricas
        def calcular_metricas(procesos):
            tiempo_espera = sum(p.tiempo_espera for p in procesos) / len(procesos)
            tiempo_respuesta = sum(p.tiempo_respuesta for p in procesos) / len(procesos)
            return tiempo_espera, tiempo_respuesta
        
        espera_fifo, respuesta_fifo = calcular_metricas(procesos_fifo)
        espera_sjf, respuesta_sjf = calcular_metricas(procesos_sjf)
        espera_rr, respuesta_rr = calcular_metricas(procesos_rr)
        
        # Mostrar comparación
        self.resultado_text.delete(1.0, tk.END)
        
        resultado = "=== COMPARACIÓN DE ALGORITMOS ===\n\n"
        resultado += f"{'Algoritmo':<15} {'T. Espera Prom.':<18} {'T. Respuesta Prom.':<20}\n"
        resultado += "-" * 55 + "\n"
        resultado += f"{'FIFO':<15} {espera_fifo:<18.2f} {respuesta_fifo:<20.2f}\n"
        resultado += f"{'SJF':<15} {espera_sjf:<18.2f} {respuesta_sjf:<20.2f}\n"
        resultado += f"{'Round Robin':<15} {espera_rr:<18.2f} {respuesta_rr:<20.2f}\n"
        
        # Determinar el mejor algoritmo
        resultado += "\nANÁLISIS:\n"
        if espera_fifo <= espera_sjf and espera_fifo <= espera_rr:
            resultado += f"• FIFO tiene el menor tiempo de espera promedio ({espera_fifo:.2f})\n"
        elif espera_sjf <= espera_fifo and espera_sjf <= espera_rr:
            resultado += f"• SJF tiene el menor tiempo de espera promedio ({espera_sjf:.2f})\n"
        else:
            resultado += f"• Round Robin tiene el menor tiempo de espera promedio ({espera_rr:.2f})\n"
        
        if respuesta_fifo <= respuesta_sjf and respuesta_fifo <= respuesta_rr:
            resultado += f"• FIFO tiene el menor tiempo de respuesta promedio ({respuesta_fifo:.2f})\n"
        elif respuesta_sjf <= respuesta_fifo and respuesta_sjf <= respuesta_rr:
            resultado += f"• SJF tiene el menor tiempo de respuesta promedio ({respuesta_sjf:.2f})\n"
        else:
            resultado += f"• Round Robin tiene el menor tiempo de respuesta promedio ({respuesta_rr:.2f})\n"
        
        self.resultado_text.insert(tk.END, resultado)
        
        # Mostrar gráfico comparativo (usar el SJF como ejemplo)
        self.dibujar_gantt(secuencia_sjf, "SJF (Comparación)")

def main():
    root = tk.Tk()
    app = InterfazSimulador(root)
    root.mainloop()

if __name__ == "__main__":
    main()