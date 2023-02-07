from models.device_model import DeviceModel


class IResourceCreationRequest:
    pass


def setModel(v):
    global model
    model = v


def modifyIResourceCreationRequest():
    global IResourceCreationRequest

    if model == "device":
        IResourceCreationRequest = type('IResourceCreationRequest', (DeviceModel,),
                                        dict(IResourceCreationRequest.__dict__))
