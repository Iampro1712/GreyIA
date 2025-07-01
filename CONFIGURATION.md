# GreyIA - Configuración de Variables de Entorno

## 📋 Resumen de Cambios

Este proyecto ha sido actualizado para mejorar la seguridad moviendo información sensible de archivos JSON a variables de entorno. Los cambios principales incluyen:

### ✅ Cambios Realizados

1. **Requirements.txt actualizado**: Se removieron las versiones específicas de las librerías para permitir instalaciones más flexibles
2. **Variables de entorno**: Información sensible movida a archivo `.env`
3. **Archivos JSON actualizados**: Solo contienen configuraciones no sensibles
4. **Sistema híbrido**: Combina configuración JSON con variables de entorno
5. **SDK actualizada**: Migración de `google-generativeai` a `google-genai` (nueva SDK oficial de Google)

## 🔧 Configuración Inicial

### 1. Copiar archivo de ejemplo
```bash
cp .env.example .env
```

### 2. Configurar variables de entorno
Edita el archivo `.env` con tus valores reales:

```env
# Telegram Bot Configuration
TELEGRAM_API_ID=tu_api_id_aqui
TELEGRAM_API_HASH=tu_api_hash_aqui
TELEGRAM_BOT_TOKEN=tu_bot_token_aqui

# Database Configuration
DB_HOST=tu_host_de_base_de_datos
DB_PORT=tu_puerto_de_base_de_datos
DB_USER=tu_usuario_de_base_de_datos
DB_PASSWORD=tu_contraseña_de_base_de_datos
DB_DATABASE=tu_nombre_de_base_de_datos

# LLM Configuration (Google Generative AI)
API_KEY=tu_api_key_de_google_ai
```

### 3. Obtener las credenciales necesarias

#### Telegram Bot
1. **API ID y API Hash**: Obtén estos valores en https://my.telegram.org/apps
2. **Bot Token**: Crea un bot con @BotFather en Telegram

#### Base de Datos MySQL
- Configura tu base de datos MySQL y obtén las credenciales de conexión

#### Google Generative AI
- Obtén tu API key en https://makersuite.google.com/app/apikey

## 📁 Estructura de Archivos Modificados

### Archivos de Configuración
- `src/config/config.json` - Solo configuraciones no sensibles del bot
- `src/config/db.json` - Solo configuraciones no sensibles de la BD
- `src/config/llmConfig.json` - Solo configuraciones no sensibles del LLM

### Sistema de Carga
- `src/moduls/utils/utils.py` - Función `load_json()` actualizada para combinar JSON + variables de entorno

## 🔒 Seguridad

### Variables Sensibles Protegidas
- ✅ API ID y Hash de Telegram
- ✅ Token del bot de Telegram  
- ✅ Credenciales de base de datos
- ✅ API Key de Google Generative AI

### Archivos Protegidos
- `.env` está incluido en `.gitignore`
- `.env.example` es seguro para el repositorio (sin valores reales)

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requierements.txt
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus valores reales
```

### 3. Ejecutar el bot
```bash
cd src
python main.py
```

## 🔄 Migración de SDK de Google

### Nueva SDK: `google-genai`
El proyecto ha sido actualizado para usar la nueva SDK oficial de Google `google-genai` en lugar de `google-generativeai`.

**Beneficios de la nueva SDK:**
- ✅ Acceso a modelos más recientes (Gemini 2.5)
- ✅ Mejor rendimiento y estabilidad
- ✅ Soporte oficial a largo plazo
- ✅ Nuevas funcionalidades como generación de imágenes y video

**Cambios en el código:**
- `import google.generativeai as genai` → `from google import genai`
- `genai.configure()` → `client = genai.Client()`
- `model.generate_content_async()` → `client.models.generate_content()`

## ⚠️ Notas Importantes

1. **Nunca subas el archivo `.env` al repositorio**
2. **Usa `.env.example` como plantilla para nuevas instalaciones**
3. **Las variables de entorno tienen prioridad sobre los valores JSON**
4. **Mantén actualizadas las credenciales según sea necesario**
5. **La nueva SDK requiere una API key válida de Google AI Studio**

## 🔄 Migración desde Versión Anterior

Si tienes una instalación anterior:

1. Copia tus valores sensibles de los archivos JSON antiguos
2. Crea el archivo `.env` con estos valores
3. Los archivos JSON actualizados mantendrán las configuraciones no sensibles
4. El sistema funcionará automáticamente con la nueva configuración

## 📞 Soporte

Si tienes problemas con la configuración, verifica:
- Que el archivo `.env` existe y tiene los valores correctos
- Que las credenciales son válidas
- Que todas las dependencias están instaladas correctamente
