from ultralytics import YOLO
import cv2
import numpy as np
from typing import Union, Tuple, List

class ObjectDetector:
    def __init__(self, model_path: str = "yolo12x.pt", confidence: float = 0.45):
        
        self.model = YOLO(model_path)
        self.confidence = confidence

    def process_image(self, image: Union[str, np.ndarray]) -> Tuple[np.ndarray, List]:
        """
        Processa uma imagem e retorna a imagem anotada e os resultados
        Args:
            image: Pode ser um caminho de arquivo ou array numpy
        Returns:
            Tuple contendo a imagem anotada e lista de detecções
        """
        # Carrega a imagem se for um caminho de arquivo
        if isinstance(image, str):
            image = cv2.imread(image)
        
        # Faz a detecção
        results = self.model(image, conf=self.confidence)
        
        # Obtém a imagem anotada
        annotated_image = results[0].plot()
        
        # Extrai informações das detecções
        detections = []
        for r in results[0].boxes.data:
            x1, y1, x2, y2, conf, cls = r
            detection = {
                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                'confiança':float(conf),
                'classe': int(cls),
                'encontrado': results[0].names[int(cls)]
            }
            detections.append(detection)
        
        return annotated_image, detections

    def display_image(self, image: np.ndarray, window_name: str = "Detecção", wait_key: bool = True):
        """
        Exibe a imagem em uma janela
        Args:
            image: Imagem a ser exibida
            window_name: Nome da janela
            wait_key: Se deve aguardar tecla para fechar
        """
        cv2.imshow(window_name, image)
        if wait_key:
            cv2.waitKey(0)
        cv2.destroyAllWindows()