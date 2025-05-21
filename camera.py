from datetime import datetime
from pymongo import MongoClient
from json_converter import from_dict
from video_extractor import VideoFrameExtractor
from object_detector import ObjectDetector
import time

class Camera:
    def __init__(self, camera_id: str, url: str, db_uri: str = "mongodb://localhost:27017/"):
        """
        Inicializa uma câmera para monitoramento
        Args:
            camera_id: Identificador único da câmera
            url: URL do stream da câmera
            db_uri: URI de conexão com MongoDB
        """
        self.camera_id = camera_id
        self.url = url
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client.camera_monitoring
        self.collection = self.db.detections
        self.extractor = VideoFrameExtractor(stream_url=url)
        self.detector = ObjectDetector()

    def start_monitoring(self, capture_interval: int = 5):
        """
        Inicia o monitoramento da câmera
        Args:
            capture_interval: Intervalo entre capturas em segundos
        """
        print(f"Iniciando monitoramento da câmera {self.camera_id}")
        try:
            while True:
                frame_path = self.extractor.capture_frame()
                if frame_path:
                    # Processa o frame e obtém detecções
                    _, detections = self.detector.process_image(frame_path)
                    
                    # Prepara documento para MongoDB
                    now = datetime.now()
                    detection_doc = {
                        "camera_id": self.camera_id,
                        "date": now.strftime("%d/%m/%y"),
                        "time": now.strftime("%H:%M"),
                        "detections": from_dict(detections)
                    }
                    
                    # Salva no MongoDB
                    self.collection.insert_one(detection_doc)
                    
                    # Log das detecções
                    print(f"Detecções salvas para câmera {self.camera_id} em {detection_doc['date']} {detection_doc['time']}")
                    
                time.sleep(capture_interval)
                
        except KeyboardInterrupt:
            print(f"\nMonitoramento da câmera {self.camera_id} interrompido")
            self.db_client.close()

    def get_detections(self, date: str = None):
        """
        Recupera detecções da câmera
        Args:
            date: Data no formato dd/mm/yy (opcional)
        Returns:
            Lista de detecções
        """
        query = {"camera_id": self.camera_id}
        if date:
            query["date"] = date
        
        return list(self.collection.find(query, {"_id": 0}))