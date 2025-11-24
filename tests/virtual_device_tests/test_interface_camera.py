import pytest

from virtual_device_v4.device.interface_camera import InterfaceCamera


class StubCamera(InterfaceCamera):
    """Subclass that defers to InterfaceCamera to surface NotImplemented errors."""

    def set_id(self, id_):
        return super().set_id(id_)

    def get_id(self):
        return super().get_id()

    def get_view(self):
        return super().get_view()

    def pan_right(self):
        return super().pan_right()

    def pan_left(self):
        return super().pan_left()

    def zoom_in(self):
        return super().zoom_in()

    def zoom_out(self):
        return super().zoom_out()


@pytest.fixture
def stub_camera():
    # Although InterfaceCamera is abstract, overriding each method allows instantiation.
    return StubCamera()


@pytest.mark.parametrize(
    "method_name",
    [
        "set_id",
        "get_id",
        "get_view",
        "pan_right",
        "pan_left",
        "zoom_in",
        "zoom_out",
    ],
)
def test_interface_camera_methods_raise_not_implemented(stub_camera, method_name):
    method = getattr(stub_camera, method_name)
    with pytest.raises(NotImplementedError):
        # Some methods expect a parameter; provide a dummy value when needed.
        if method_name in {"set_id"}:
            method(1)
        else:
            method()
