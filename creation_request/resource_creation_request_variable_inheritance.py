from models.device_model import DeviceModel

model = None


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


'''
NOTE:
- adding this in api_server.py
    # setting models type
    creation_request.resource_creation_request.setModel("device")
    creation_request.resource_creation_request.modifyIResourceCreationRequest()
    
- adding this in POST of resources_methods.py and in PUT of resource_methods.py
    # (after this row) resource_creation_request = IResourceCreationRequest(**json_data)
    creation_request.resource_creation_request.modifyIResourceCreationRequest()
'''
