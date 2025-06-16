# 🖥️ Simulador de Planificador de Procesos

Un simulador visual interactivo para algoritmos de planificación de CPU en sistemas operativos, desarrollado como proyecto académico para la materia de Sistemas Operativos.

![Python](https://img.shields.io/badge/python-v3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![Matplotlib](https://img.shields.io/badge/charts-Matplotlib-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Descripción

Este proyecto implementa un simulador completo que permite visualizar y comparar el funcionamiento de tres algoritmos clásicos de planificación de procesos:

- **FIFO (First In First Out)** - Planificación por orden de llegada
- **SJF (Shortest Job First)** - Planificación por trabajo más corto
- **Round Robin** - Planificación circular con quantum de tiempo

### 🎯 Características Principales

- ✅ Interfaz gráfica intuitiva y fácil de usar
- ✅ Visualización mediante diagramas de Gantt
- ✅ Cálculo automático de métricas de rendimiento
- ✅ Comparación simultánea de algoritmos
- ✅ Ejemplos predefinidos para pruebas rápidas
- ✅ Configuración personalizable de parámetros

## 🖼️ Capturas de Pantalla

### Interfaz Principal
*Interfaz principal mostrando la entrada de datos y lista de procesos*
![image](https://github.com/user-attachments/assets/95226c3e-d346-4028-8a57-7e7788064068)

### Diagrama de Gantt
*Ejemplo de diagrama de Gantt generado por el algoritmo FIFO*
![image](https://github.com/user-attachments/assets/e94980de-264d-425a-85fc-6f79b3aef3c2)

### Comparación de Algoritmos
*Vista de comparación mostrando métricas de los tres algoritmos*
![image](https://github.com/user-attachments/assets/f27058c4-253e-4a40-ae09-915920c9c63f)

## 🚀 Instalación y Uso

### Prerrequisitos

- Python 3.x
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/AdrianEst27/planificador_procesos.git
cd planificador_procesos
```

2. **Instalar dependencias:**
```bash
pip install matplotlib
```

3. **Ejecutar el simulador:**
```bash
python simulador.py
```

### Uso Básico

1. **Agregar Procesos:**
   - Ingresa el nombre del proceso
   - Especifica el tiempo de llegada
   - Define la duración del proceso
   - Haz clic en "Agregar Proceso"

2. **Ejecutar Algoritmos:**
   - Selecciona el algoritmo deseado (FIFO, SJF, Round Robin)
   - Visualiza el diagrama de Gantt generado
   - Revisa las métricas calculadas

3. **Comparar Algoritmos:**
   - Utiliza el botón "Comparar Algoritmos"
   - Analiza las métricas de rendimiento
   - Identifica el algoritmo más eficiente

4. **Funciones Adicionales:**
   - "Cargar Ejemplo": Carga un conjunto predefinido de procesos
   - "Limpiar Datos": Reinicia el simulador
   - Configuración de quantum para Round Robin

## 📊 Métricas Calculadas

El simulador calcula automáticamente las siguientes métricas para cada proceso:

- **Tiempo de Espera**: Tiempo que el proceso permanece en cola
- **Tiempo de Respuesta**: Tiempo desde la llegada hasta la primera ejecución
- **Tiempo de Finalización**: Momento en que el proceso termina
- **Promedios Generales**: Para comparación entre algoritmos

## 🔧 Estructura del Código

```
simulador.py
├── Clase Proceso
│   ├── Atributos del proceso
│   └── Métricas calculadas
├── Clase PlanificadorProcesos
│   ├── Algoritmo FIFO
│   ├── Algoritmo SJF
│   └── Algoritmo Round Robin
└── Clase InterfazSimulador
    ├── Interfaz gráfica
    ├── Manejo de eventos
    └── Visualización de resultados
```

## 📈 Ejemplo de Uso

### Datos de Ejemplo
```
Proceso | Tiempo de Llegada | Duración
P1      | 0                | 8
P2      | 1                | 4
P3      | 2                | 9
P4      | 3                | 5
P5      | 4                | 2
```

### Resultados Esperados
- **FIFO**: Ejecución secuencial, posible efecto convoy
- **SJF**: Optimización del tiempo promedio de espera
- **Round Robin**: Mejor tiempo de respuesta con quantum apropiado

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **Tkinter**: Interfaz gráfica de usuario
- **Matplotlib**: Generación de diagramas de Gantt
- **Programación Orientada a Objetos**: Paradigma de desarrollo

## 📚 Propósito Educativo

Este simulador fue desarrollado como herramienta educativa para:

- Comprender algoritmos de planificación de procesos
- Visualizar conceptos abstractos de sistemas operativos
- Comparar eficiencia entre diferentes estrategias
- Experimentar con parámetros y cargas de trabajo

## 🎓 Información Académica

- **Universidad**: Hipócrates
- **Materia**: Sistemas Operativos
- **Semestre**: LIS6 - Tercer Parcial
- **Estudiante**: Jesús Adrián Salas Estrada
- **Matrícula**: 22010585
- **Docente**: Gladis Guzmán Guerrero

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🔮 Futuras Mejoras

- [ ] Implementación de algoritmos adicionales (Prioridades, Multilevel)
- [ ] Simulación de memoria virtual
- [ ] Exportación de resultados a PDF/Excel
- [ ] Interfaz web responsive
- [ ] Análisis estadístico avanzado
- [ ] Modo de simulación en tiempo real

## 📞 Contacto

Jesús Adrián Salas Estrada - [adrian.estrada99@outlook.com](adrian.estrada99@outlook.com)

Link del Proyecto: [https://github.com/AdrianEst27/planificador_procesos](https://github.com/AdrianEst27/planificador_procesos)

---

## ⭐ Agradecimientos

- Docente Gladis Guzmán Guerrero por la guía y orientación
- Universidad Hipócrates por el marco académico
- Comunidad de desarrolladores Python por las herramientas utilizadas

---

*¿Te resultó útil este simulador? ¡Dale una ⭐ al repositorio y compártelo con otros estudiantes!*
