# ParaBank – Automatización de pruebas con Python y Playwright

> **Estado: proyecto en proceso.** Esta suite no está terminada. Hay páginas con cobertura parcial, tests por rehacer y varios hallazgos todavía sin cerrar. La sección [Pendientes](#pendientes) lista lo que falta y la sección [Comportamientos observados](#comportamientos-observados-de-la-aplicación) documenta lo que se fue descubriendo, indicando qué está verificado y qué es solo una hipótesis.

Suite de pruebas end-to-end sobre [ParaBank](https://parabank.parasoft.com), una aplicación bancaria de demostración de Parasoft. Es un proyecto de práctica para aprender automatización de pruebas con criterios cercanos a un entorno de trabajo real.

## Tecnologías

- Python
- Playwright (API sincrónica) y pytest (`pytest-playwright`)
- Faker (datos de prueba)
- Patrón **Page Object Model**

## Estructura del proyecto

```
.
├── conftest.py            # fixtures (sesión iniciada)
├── pytest.ini             # base_url, markers y opciones por defecto
├── pages/                 # page objects y utilidades
│   ├── login_page.py
│   ├── register_page.py
│   ├── menu_component.py
│   ├── accounts_overview_page.py
│   ├── account_activity_page.py
│   ├── open_new_account_page.py
│   ├── transfer_funds_page.py
│   ├── bill_pay_page.py
│   ├── find_transactions_page.py
│   ├── transaction_details_page.py
│   ├── request_loan_page.py
│   ├── update_profile_page.py
│   └── utils.py
└── tests/
    ├── helpers.py         # flujos reutilizables entre tests
    └── test_*.py
```

### Decisiones de diseño

- **Las aserciones viven en los tests.** Los page objects devuelven datos o locators sin evaluar, para que el test use `expect()` con reintentos automáticos.
- **Esperas por condición, no por tiempo.** Se usa `expect()` sobre algo concreto. La excepción pendiente es `click_go()` en la página de actividad (ver [Pendientes](#pendientes)).
- **Locators estables.** Se prefiere el atributo `name` frente a ids con puntos o texto de fila, y se evita depender del orden del DOM.
- **`base_url` centralizada** en `pytest.ini`, con barra final y rutas relativas sin barra inicial.
- **Un fallo esperado no se oculta:** los defectos observados se marcan con `xfail(strict=True)` y una razón verificada, de modo que el test avise cuando la aplicación cambie.

## Markers

| Marker | Uso |
|---|---|
| `smoke` | pruebas críticas |
| `regression` | pruebas no críticas |
| `negative` | comportamiento inválido o no permitido |
| `creates_data` | crean datos persistentes en el servidor (cuentas, usuarios, préstamos) |

Por defecto `pytest` **excluye** `creates_data` (`addopts` en `pytest.ini`).

## Instalación

```bash
pip install pytest pytest-playwright faker
playwright install chromium
```

## Configuración de entorno

- La URL base está en `pytest.ini`. Se probó contra una **instancia local** de ParaBank (`http://localhost:8080/parabank/`) y contra el servidor público.
- **Recomendación:** usar la instancia local. El servidor público es compartido, inestable y acumula los datos que dejan las corridas.
- Las credenciales del usuario de prueba no deben estar escritas en el código. Se leen de variables de entorno.

```bash
# PowerShell
$env:PARABANK_USER = "tu_usuario"
$env:PARABANK_PASSWORD = "tu_contraseña"
```

## Ejecución

```bash
pytest                              # suite por defecto (sin creates_data)
pytest tests/test_login_page.py     # un archivo
pytest -m negative                  # solo pruebas negativas
pytest -m "not negative"            # sin pruebas negativas
pytest -o addopts="" -m creates_data  # pruebas que crean datos
pytest --headed                     # con navegador visible
```

## Cobertura actual

| Área | Estado |
|---|---|
| Login | Cubierto (camino feliz). Falta el negativo con credenciales inválidas |
| Registro | **En rehacer**: ver hallazgo sobre caracteres acentuados |
| Abrir cuenta (`creates_data`) | Cubierto |
| Transferencias | Parcial: falta aserción final del resultado |
| Pago de facturas | Parcial: depende del estado del usuario, ver hallazgos |
| Actividad de cuenta | Cubierto, con filtros por mes y tipo |
| Buscar transacciones | Parcial: ID y monto cubiertos; fecha y rango en corrección |
| Solicitar préstamo (`creates_data`) | Cubierto |
| Actualizar perfil | Cubierto, con un caso `xfail` |
| Acceso tras cerrar sesión (`negative`) | En proceso, ver hallazgos |
| Panel de administración | Fuera del alcance por ahora (ver nota más abajo) |

---

## Comportamientos observados de la aplicación

Esta sección documenta casos raros que aparecieron durante el desarrollo. Cada uno indica **dónde se observó** y **qué tan firme es la conclusión**. Una hipótesis no verificada se señala como tal. No se afirma si un comportamiento es intencional.

### 1. El `+` del teléfono se convierte en espacio al guardar el perfil

- **Qué pasa:** al guardar un teléfono como `+34 975 291 671`, tras recargar la página queda ` 34 975 291 671`.
- **Verificado:** de forma manual y con test automatizado. La aserción previa al envío pasa, así que el cambio ocurre al guardar.
- **En la suite:** dos casos parametrizados, con y sin `+`. El caso con `+` es `xfail(raises=AssertionError, strict=True)`.

### 2. Carrera al cargar el formulario de "Update Profile"

- **Qué pasa:** el título aparece antes de que el formulario reciba sus datos guardados. Si el test escribe antes, esos datos pisan lo escrito y el guardado envía los valores viejos.
- **Verificado:** una aserción previa al clic mostraba el valor viejo.
- **Solución:** `is_loaded()` espera que el campo de nombre no esté vacío. Limitación: asume un usuario con perfil poblado, lo cual es válido porque el registro lo exige.

### 3. Caracteres acentuados en el registro provocan `400 Bad Request`

- **Qué pasa:** el servidor devolvió `Character decoding failed` con valores como `Cáceres` o `Águeda`, antes de validar nada.
- **Verificado:** se repitió en varias corridas con distintos acentos.
- **Sin confirmar:** la causa. "Update Profile" sí aceptó acentos, así que podría deberse a cómo cada formulario envía los datos. Falta confirmarlo manualmente y con DevTools (Network).
- **En la suite:** los datos pasaron a ser solo ASCII para que el test pruebe lo que debe. El caso con acentos queda pendiente de un test aparte.

### 4. Pago de facturas: saldo sin cambios con un usuario particular

- **Qué pasa:** con un usuario antiguo, tras un pago exitoso el saldo de la cuenta no cambiaba, con distintos montos ($10 y $500). La respuesta era 200 con mensaje de éxito.
- **Verificado:** el flujo manual con usuarios nuevos sí actualizó el saldo. Ese usuario dejó además de poder iniciar sesión.
- **Conclusión provisoria:** parece un estado de datos corrupto de esa cuenta en el servidor compartido, y no un defecto de la funcionalidad. No se reportó como bug.
- **Pendiente:** volver a comprobarlo en la instancia local, donde el estado es controlado.
- **Dato relacionado:** la aplicación permite pagar o transferir más de lo disponible y deja el saldo negativo.

### 5. Errores intermitentes del servidor público

- **Qué pasa:** aparece "An internal error has occurred" al iniciar sesión o al navegar, también de forma manual. Credenciales que dejan de funcionar con el tiempo.
- **Causa probable (hipótesis):** servidor de demo compartido y saturado, con datos acumulados por muchas corridas.
- **Consecuencia:** `MenuComponent` valida que no se muestre el encabezado "Error!". Así un fallo del entorno no pasa inadvertido. Un fallo de este tipo no indica por sí solo un defecto del código ni de la aplicación.

### 6. Listas desplegables que se llenan de forma asíncrona

- **Qué pasa:** en "Open New Account" y "Transfer Funds" el `<select>` aparece vacío y se llena un instante después. Leer sus opciones de inmediato devuelve una lista vacía.
- **Además:** las `<option>` de un `<select>` cerrado cuentan como *ocultas* para Playwright, así que `to_be_visible()` falla aunque existan.
- **Solución:** esperar con `expect(opciones).not_to_have_count(0)`, que comprueba presencia y no visibilidad. Está centralizado en `wait_for()`.

### 7. Diferencia de un día entre fechas del servidor y las buscadas

- **Qué pasa:** las transacciones se registran con una fecha un día **posterior** a la local, y al buscar por fecha los resultados a veces devuelven el día anterior al ingresado.
- **Sin confirmar:** la causa. La hipótesis es una diferencia de zona horaria entre el servidor y la máquina local. No se pudo comprobar con una marca de tiempo visible.
- **En la suite:** `add_one_day()` compensa el desfase, con un comentario que explica el motivo. Falta verificar a mano qué fecha muestran los resultados al buscar una fecha concreta.

### 8. Filas de transacciones con el mismo contenido

- **Qué pasa:** localizar una fila por fecha, tipo y monto devuelve decenas de coincidencias (`strict mode violation`), porque las operaciones de prueba repiten esos valores.
- **Solución:** se elige la fila por **posición** (`nth()`), y no se reconstruye por contenido.

### 9. La URL base y las rutas relativas

- **Qué pasa:** una ruta que empieza con `/` ignora el path del `base_url`. `https://host/parabank` más `/overview.htm` apunta a `https://host/overview.htm`.
- **Solución:** `base_url` con barra final y rutas sin barra inicial (`overview.htm`).

### 10. Acceso y cierre de sesión

Este es el hallazgo más complejo y **sigue en proceso**.

**Servidor público (observado de forma manual, tras cerrar sesión y volver con "atrás"):**
- *Overview:* aparece un diálogo nativo del navegador pidiendo usuario y contraseña. Al cancelar y hacer clic en algo, la página muestra `Error! Server returned 401: User login required`. El diálogo es del navegador y no de la página, por eso la tecla Escape no lo cierra.
- *Activity:* panel de login a la izquierda y los datos reales de la cuenta a la derecha.
- *Transaction Details:* la página se ve completa. Tras recargar, el panel izquierdo muestra el login pero los datos siguen visibles.

**Instancia local:**
- Las 7 páginas principales rechazan el acceso tras cerrar sesión (la prueba vuelve a pedir la URL y debe mostrar el login). **Verificado.**
- `activity.htm` sin sesión devuelve un error. **Verificado.**
- `transaction.htm?id=<ID existente>` **muestra los datos de la transacción sin sesión**:
  - con un contexto limpio de Playwright (respuesta 200),
  - en una ventana de incógnito,
  - con distintos IDs reales,
  - y con la sesión de otro usuario, sobre transacciones que no le pertenecen.
- La caché del navegador no lo explica (se desactivó y el resultado fue el mismo).
- Un ID inexistente (`id+1`) responde que la transacción no existe.

**Qué no se sabe:** la causa, ni si es un comportamiento previsto de la aplicación de demo. No se probaron IDs ajenos en el servidor público.

**Cómo se probó:** solo en local, con usuarios creados para la prueba.

**En la suite:** test con `xfail(raises=AssertionError, strict=True)` sobre un contexto sin sesión. Se descartó una conclusión anterior (que no había defecto) tras comprobar que una ventana de incógnito inicial no coincidía con las demás pruebas.

---

## Pendientes

- Terminar los tests de búsqueda por fecha y por rango (selección de fechas válidas y aserciones reales).
- Rehacer los tests de registro con datos ASCII y separar el caso con acentos.
- Agregar aserción final al test de transferencias y los tests negativos de login, transferencias y pago de facturas.
- Reemplazar `wait_for_timeout` en `click_go()` por una espera por condición.
- Mover las credenciales a variables de entorno y dejarlas fuera del repositorio.
- Revisión general del código (nombres, duplicación, restos de depuración).
- Agregar `__init__.py` en `pages/` y `tests/`.
- Panel de administración: queda fuera del alcance por ahora. Sus acciones pueden borrar datos y no conviene automatizarlas contra un servidor compartido. Podría retomarse con una instancia local propia.
- Integración continua con GitHub Actions.

## Notas

- Las pruebas que cambian datos o recorren IDs solo se hicieron en una instancia local. No se debe probar contra datos de terceros en el servidor público.
- Proyecto con fines de aprendizaje. Los comportamientos descritos se refieren a una aplicación de demostración.