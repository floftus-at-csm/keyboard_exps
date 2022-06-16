
from email.mime import image
import serial
import asyncio
from serial.serialutil import SerialException
from time import sleep

# modified from https://blog.rareschool.com/2021/01/controlling-raspberry-pi-pico-using.html
# based on https://github.com/GSGBen/pico-serial/blob/main/serial_test.py

class SerialSender:
    TERMINATOR_INITIAL = '\n'.encode('UTF8')


    def __init__(self, device='COM3', baud=115200, timeout=1):
        self.serial = serial.Serial(device, baud, timeout=timeout)

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR_INITIAL)
        return line.decode('UTF8').strip()

    def send_line(self, text: str):
        line = '%s\n' % text
        self.serial.write(line.encode('UTF8'))

    
    def send_ending_line(self, text: str):
        line = 'ending_message\n'
        self.serial.write(line.encode('UTF8'))

    def close(self):
        self.serial.close()

def rotate_3d_model(model):
    # run glslviewer headless
    # glslViewer 3D/00_pipeline/00_background.frag 3D/00_pipeline/head.ply -e model_position,x,y,z -e skybox,off -e light_position,x,y,z -e wait,6 -e screenshot, /3D_model_images/current_image.png
    # take screenshot
#     When running the glslViewer is possible to make a stack of command just by adding -e <commands> arguments one after the other. They will be run in that order. For example if you want to wait 6 seconds and make a screenshot you could do something like:

# glslViewer shader.frag -e wait,6 -e screenshot,image.png
    # save to folder
    return path

def load_image_from_path(path):


    return the_image

def create_text_image(image):

    return text_array 



if __name__ == '__main__':

    #previous_media_info = None
    
    while True:
        current_image_path = rotate_3d_model(current_model)
        current_image = load_image_from_path(current_image_path);
        text_image_array = create_text_image(current_image)
        
        
        if text_image_array != previous_image_array and text_image_array != None:
            print(text_image_array)
            previous_image_array = text_image_array
            sleep(1)
            
            # recreate the serial each time to allow handling disconnection
            try:
                # initialise serial
                serial_sender = SerialSender()
                
                # send contents of text_image_array
                val = 0
                for _ in range(60):
                    serial_sender.send_line(text_image_array[val])
                    val = val + 1
                
                # send ending message
                serial_sender.send_ending_line()

                # wait until the message has been processed on the e-paper display
                received_message = "nothing"
                while received_message != "updated":
                    received_message = serial_sender.receive() # this needs to wait for a response
                # close the serial
                serial_sender.close()
            except SerialException:
                pass
        # then loop
