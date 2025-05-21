from camera import Camera

def main():
    # Configurações
    camera_config = {
        "camera_id": "CAM001",
        "url": "http://192.168.3.7:8080/video",
        "db_uri": "mongodb://localhost:27017/"
    }
    
    # Criar e iniciar câmera
    camera = Camera(**camera_config)
    camera.start_monitoring(capture_interval=5)

if __name__ == "__main__":
    main()