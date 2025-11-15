"""
Configuración de variantes del producto
Sistema de gestión de tareas con diferentes niveles de funcionalidad
"""

# Variante A: Sistema básico
PRODUCT_A = {
    'name': 'TaskManager Basic',
    'ENABLE_TASK_COMPLETION': False,
    'ENABLE_TASK_IMPORTANCE': False,
    'ENABLE_COMPLETED_TASKS_VIEW': False,
    'SHOW_TASK_DATES': False,
}

# Variante B: Sistema completo
PRODUCT_B = {
    'name': 'TaskManager Pro',
    'ENABLE_TASK_COMPLETION': True,
    'ENABLE_TASK_IMPORTANCE': True,
    'ENABLE_COMPLETED_TASKS_VIEW': True,
    'SHOW_TASK_DATES': True,
}

# Configuración activa (cambiar entre 'A' o 'B')
ACTIVE_PRODUCT = 'A'  # Cambiar a 'A' para producto básico

# Obtener configuración activa
def get_active_config():
    if ACTIVE_PRODUCT == 'A':
        return PRODUCT_A
    elif ACTIVE_PRODUCT == 'B':
        return PRODUCT_B
    else:
        return PRODUCT_B  # Por defecto producto completo