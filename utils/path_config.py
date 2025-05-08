from pathlib import Path


base_path = Path(__file__).parent.parent / "media" 

class MediaPath:
    @staticmethod
    def getVideoPath(fileName: str):
        return base_path / "video" /fileName
    
    @staticmethod
    def getImagePath(fileName: str):
        return base_path / "images" /fileName
    
    