from camera import Camera
from camerasqlite import camerasqlite


class CameraWorkerList(list[Camera]):
    @classmethod
    def createlist(cls,addrlist:list):
        camlist=[]
        for address in addrlist:
            camlist.append(Camera(address))
        return cls(camlist)




class CameraWorker():
    @staticmethod
    def runall(cameraworkerlist:CameraWorkerList,database:camerasqlite):
        """

        :type CameraWorkerList: object
        :param CameraWorkerList:
        """
        for cameraw in cameraworkerlist:
            cameraw.capture()
            database.store(cameraw.get_jpg(),cameraw.host)

    @staticmethod
    def runallthread(cameraworkerlist: CameraWorkerList):
        """
        :type CameraWorkerList: object
        :param CameraWorkerList:
        """
        database = camerasqlite()
        for cameraw in cameraworkerlist:
            cameraw.capture()
            database.store(cameraw.get_jpg(), cameraw.host)

