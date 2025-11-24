from virtual_device_v4.device.device_camera import DeviceCamera


def test_missing_camera_uses_placeholder_image():
    camera = DeviceCamera()
    try:
        camera.set_id(9999)  # ID that should not exist on disk
        assert camera.imgSource is not None
        assert camera.imgSource.size == (camera.SOURCE_SIZE, camera.SOURCE_SIZE)
        # Placeholder image starts with a black background.
        assert camera.imgSource.getpixel((0, 0)) == (0, 0, 0)
    finally:
        camera.stop()
