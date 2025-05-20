# Generador de Datos Sintéticos de Terremotos

## 1. Introducción

Este proyecto genera un conjunto de datos sintéticos que imitan eventos sísmicos reales, usando técnicas estadísticas como *Kernel Density Estimation* (KDE). Su objetivo es producir datos que representen de manera verosímil características como ubicación geográfica, magnitud, profundidad, impacto humano y económico de terremotos. Está diseñado para ser usado en prácticas de análisis de datos, visualización y entrenamiento de modelos de aprendizaje automático.

Los datos generados siguen patrones similares a los observados en registros reales y permiten una evaluación comparativa a través de visualizaciones y estadísticas.

## 2. Origen de los Datos Reales

Los datos reales utilizados como base para el entrenamiento del modelo KDE fueron obtenidos del **United States Geological Survey (USGS)** mediante su API pública de eventos sísmicos. El archivo resultante (`earthquake_data.csv`) contiene eventos desde 1975 con información como latitud, longitud, profundidad, magnitud y tipo de magnitud.

## 3. Descripción del Código y Funcionamiento

El proyecto está estructurado en módulos y scripts independientes para facilitar su uso, pruebas y mantenimiento.

### 3.1. Librerías Utilizadas

- `pandas`: Manipulación y análisis de datos.
- `numpy`: Cálculos matemáticos y generación de ruido.
- `matplotlib` y `seaborn`: Visualización de distribuciones y comparaciones.
- `scipy.stats`: Implementación de KDE.
- `sklearn.preprocessing`: Normalización y codificación de variables.
- `geopandas` y `shapely`: Manipulación de datos geoespaciales.
- `pytest` y `coverage`: Pruebas automáticas y análisis de cobertura.

### 3.2. Componentes Clave del Proyecto

- `coordgen/generator.py`: Genera eventos sintéticos usando KDE y reglas de validación.
- `coordgen/config.py`: Define parámetros globales como `ROW_COUNT` y `RANDOM_SEED`.
- `scripts/fetch_earthquake_data.py`: Descarga datos reales desde la API del USGS.
- `scripts/train_and_generate_kde.py`: Entrena modelos KDE para lat/lon, profundidad y magnitud.
- `tests/test_generator.py`: Pruebas unitarias para asegurar la coherencia de los datos generados.
- `visualizations/`: Scripts que generan gráficos comparativos entre datos reales y sintéticos.

### 3.3. Datos Generados

Cada fila en el archivo `synthetic_earthquakes.csv` representa un evento sísmico con las siguientes variables:

* `latitude`: Latitud del epicentro del sismo.
* `longitude`: Longitud del epicentro del sismo.
* `depth`: Profundidad del evento en kilómetros.
* `mag`: Magnitud del sismo (escala Richter).
* `event_id`: Identificador único del evento sísmico.
* `date`: Fecha del evento en formato ISO (YYYY-MM-DD).
* `tectonic_plate`: Nombre de la placa tectónica asociada al evento.
* `alert_level`: Nivel de alerta emitido (ej. verde, amarillo, rojo).
* `intensity_level`: Nivel de intensidad percibida (escala modificada de Mercalli o equivalente).
* `estimated_cost`: Costo económico estimado del evento (en dólares).
* `casualties`: Número estimado de muertes.
* `injuries`: Número estimado de personas heridas.
* `displaced`: Número estimado de personas desplazadas.
* `region`: Región geográfica o administrativa donde ocurrió el evento.

La generación aplica una combinación de:
- Muestreo KDE para coordenadas y magnitud.
- Reglas condicionales para intensidad y costos.
- Clasificación geográfica por regiones y placas.
- Aleatoriedad controlada por semilla fija (`RANDOM_SEED`).

## 4. Visualización y Exportación

Los scripts en `visualizations/` permiten comparar distribuciones de variables clave entre los datos reales y los sintéticos. En particular:

- `generate_plots.py`: Genera visualizaciones individuales de distribuciones como magnitud, profundidad, impacto, etc.
- `compare_distributions.py`: Compara directamente las distribuciones de variables clave entre los datos reales (`earthquake_data.csv`) y los generados (`synthetic_earthquakes.csv`), tanto gráficamente como mediante estadísticas agregadas.

Se generan gráficos como:

- Histogramas y KDE plots de magnitud, profundidad e impactos.
- Mapas geográficos de distribución de eventos.
- Gráficos de dispersión (ej. magnitud vs intensidad, magnitud vs costo).
- Comparaciones lado a lado entre datos reales y sintéticos.

Todos los gráficos se exportan automáticamente en `visualizations/plots/`.


## 5. Pruebas y Validación

### 5.1. Pruebas Unitarias

Las pruebas se ejecutan con `pytest`, asegurando:

- Que los datos generados tengan la forma y rango esperados.
- Que las columnas clave no contengan valores nulos.
- Que las regiones asignadas correspondan a coordenadas válidas.

### 5.2. Cobertura

El análisis de cobertura se realiza con:

```bash
./run_tests.sh
````

El resultado se puede consultar en `htmlcov/index.html`.

### 5.3. Validación de Realismo

- `compare_distributions.py` permite validar visualmente y estadísticamente la similitud entre los datos reales y los generados.
- Se asegura consistencia interna entre variables (ej. magnitud e intensidad).
- Se usa KDE entrenado sobre datos reales para simular coordenadas y magnitudes plausibles.
- La semilla fija (`RANDOM_SEED`) garantiza reproducibilidad.

## 6. Limitaciones

* Los datos generados son **pseudoaleatorios** y no deben usarse como predicción real de actividad sísmica.
* Las interacciones complejas entre variables (ej. relación entre geología regional y magnitud) son simplificadas.
* Las placas tectónicas se asignan según mapas estáticos y no por dinámica de placas.

## 7. Instrucciones de Uso

### Instalación

```bash
git clone https://github.com/tuusuario/data-generation.git
cd data-generation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Generación de Datos

```bash
python -m coordgen.generator
```

### Visualización

```bash
python visualizations/generate_plots.py
```

### Pruebas

```bash
python -m pytest
# o con cobertura
./run_tests.sh
```

## 8. Conclusión

Este generador proporciona datos sintéticos de terremotos que siguen patrones reales observados. Es útil para entrenamiento de modelos, pruebas de pipelines analíticos y propósitos educativos. No reemplaza datos reales ni modelos geofísicos, pero representa una base sólida para análisis reproducible y exploración de datos sísmicos.

## Licencia

Este proyecto está bajo la Licencia MIT.

