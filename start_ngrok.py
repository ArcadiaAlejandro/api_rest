from pyngrok import ngrok
import subprocess

# Configurar ngrok para exponer el puerto 5000
# Reemplaza 'TU_AUTHTOKEN_VALIDO' con tu token de autenticación real
ngrok.set_auth_token("2iwTIozKmHRHEOW2PT3HxwaGVRL_5oJcwK7E7QqPU8WuJQ7D8")
public_url = ngrok.connect(5000, bind_tls=True)
print(f"Public URL: {public_url}")

# Ejecutar el servidor Flask
subprocess.run(["python", "app.py"])
