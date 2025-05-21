from video_extractor import VideoFrameExtractor

def main():
    # Configurações
    stream_url = "http://192.168.3.7:8080/video"
    output_dir = "frames"
    
    extractor = VideoFrameExtractor(
        stream_url=stream_url,
        output_dir=output_dir,
        capture_interval=5
    )
    extractor.start_capture()

if __name__ == "__main__":
    main()