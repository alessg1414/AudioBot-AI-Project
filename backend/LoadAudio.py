import whisper
import torch

# Verificar si hay GPU disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")

# archivos
Filename = "C:\\audio\\Grabacion.mp3"
output_File = "C:\\audio\\call.txt"

try:
    print("proces.......")
    
    # MODELO GRANDE
    # Opciones: "tiny", "base", "small", "medium", "large", "large-v2", "large-v3"
    model = whisper.load_model("large-v3")  #MÁS PRECISO
    
    # Parámetros optimizados 
    resultado = model.transcribe(
        Filename,
        language="es",
        verbose=True,
        task="transcribe",
        temperature=0.0,  # Temperatura 0 = máximo determinismo
        best_of=5,        # Número de muestras a considerar
        beam_size=5,      # Tamaño del beam search
        patience=1.0,     # Paciencia en beam search
        compression_ratio_threshold=2.4,
        logprob_threshold=-1.0,
        no_speech_threshold=0.6,
        condition_on_previous_text=True,
        initial_prompt=None,
        word_timestamps=False,  # True si necesitas timestamps por palabra
        fp16=False if device == "cpu" else True
    )
    
    full_transcripcion = resultado["text"]
    
    # Guardar con metadatos
    with open(output_File, "w", encoding="utf-8") as f:
        f.write("=== TRANSCRIPCIÓN WHISPER (MÁXIMA PRECISIÓN) ===\n\n")
        f.write(f"Modelo: large-v3\n")
        f.write(f"Dispositivo: {device}\n")
        f.write(f"Duración: {resultado.get('duration', 0):.1f}s\n")
        f.write(f"Idioma detectado: {resultado.get('language', 'es')}\n\n")
        f.write("=== TEXTO ===\n\n")
        f.write(full_transcripcion)
        
        # También guardar segmentos si quieres
        if "segments" in resultado:
            f.write("\n\n=== SEGMENTOS ===\n\n")
            for seg in resultado["segments"]:
                f.write(f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}\n") 
    
    print("✅ Transcripción completada!")
    print(f"Guardado en: {output_File}")
    
    # Mostrar estadísticas
    print(f"\nEstadísticas:")
    print(f"  - Modelo: large-v3")
    print(f"  - Dispositivo: {device}")
    print(f"  - Duración audio: {resultado.get('duration', 0):.1f}s")
    print(f"  - Texto generado: {len(full_transcripcion)} caracteres")
    
except FileNotFoundError:
    print(f"El archivo {Filename} no se encontró")
except Exception as e:
    print(f"Error: {e}")
