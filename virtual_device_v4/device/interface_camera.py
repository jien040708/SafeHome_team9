from abc import ABC, abstractmethod


class InterfaceCamera(ABC):
    """Abstract interface for camera devices."""
    
    @abstractmethod
    def set_id(self, id_):
        """Set the camera ID and load associated image."""
        raise NotImplementedError("set_id must be implemented by subclasses")

    @abstractmethod
    def get_id(self):
        """Get the camera ID."""
        raise NotImplementedError("get_id must be implemented by subclasses")

    @abstractmethod
    def get_view(self):
        """Get the current camera view as an image (PIL Image in Python)."""
        raise NotImplementedError("get_view must be implemented by subclasses")

    @abstractmethod
    def pan_right(self):
        """Pan camera to the right. Returns True if successful."""
        raise NotImplementedError("pan_right must be implemented by subclasses")

    @abstractmethod
    def pan_left(self):
        """Pan camera to the left. Returns True if successful."""
        raise NotImplementedError("pan_left must be implemented by subclasses")

    @abstractmethod
    def zoom_in(self):
        """Zoom in. Returns True if successful."""
        raise NotImplementedError("zoom_in must be implemented by subclasses")

    @abstractmethod
    def zoom_out(self):
        """Zoom out. Returns True if successful."""
        raise NotImplementedError("zoom_out must be implemented by subclasses")
