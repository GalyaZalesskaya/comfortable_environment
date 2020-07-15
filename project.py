from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import cv2
import numpy as np
import logging as log
from time import time
from openvino.inference_engine import IECore

def comfort_level(sidewalk_ratio, terrain_ratio, vegetation_ratio, fence_ratio, truck_ratio, traffic_light_ratio, traffic_sign_ratio, person_ratio, car_ratio, bicycle_ratio):
    sum_comf=8*sidewalk_ratio+10*terrain_ratio+10*vegetation_ratio-10*fence_ratio-10*truck_ratio
    print(sum_comf)
    if sum_comf<2:
        print("bad ")
    elif sum_comf<=5:
        print("ok")
    elif sum_comf<=10:
        print("good")
    else:
        print ("perfectly")

def class_size(road,sidewalk,building,wall,fence,pole,traffic_light,traffic_sign,vegetation,terrain,sky,
                   person,rider,car,truck,
                   bus,train,motorcycle,bicycle,ego_vehicle,cl21):
    sum_cl=road+sidewalk+building+wall+fence+pole+traffic_light+traffic_sign+vegetation+terrain+sky+person+rider+car+truck+bus+train+motorcycle+bicycle+ego_vehicle+cl21
    print("Sum_cl",sum_cl)
    road_ratio=road/sum_cl
    sidewalk_ratio=sidewalk/sum_cl
    building_ratio=building/sum_cl
    wall_ratio=wall/sum_cl
    fence_ratio=fence/sum_cl
    pole_ratio=pole/sum_cl
    traffic_light_ratio=traffic_light/sum_cl
    traffic_sign_ratio=traffic_sign/sum_cl
    vegetation_ratio=vegetation/sum_cl
    terrain_ratio=terrain/sum_cl
    sky_ratio=sky/sum_cl
    person_ratio=person/sum_cl
    rider_ratio=rider/sum_cl
    car_ratio=car/sum_cl
    truck_ratio=truck/sum_cl
    bus_ratio=bus/sum_cl
    train_ratio=train/sum_cl
    motorcycle_ratio=motorcycle/sum_cl
    bicycle_ratio=bicycle/sum_cl
    ego_vehicle_ratio=ego_vehicle/sum_cl
    cl21_ratio=cl21/sum_cl
    print("road=",road_ratio," sidewalk=", sidewalk_ratio," building=", building_ratio,"wall=", wall_ratio,
          "fence=", fence_ratio," pole=", pole_ratio," traffic_light=", traffic_light_ratio,"traffic_sign=",
          traffic_sign_ratio," vegetation=", vegetation_ratio," terrain_ratio=", terrain_ratio,
          " sky=", sky_ratio," person=", person_ratio," rider=", rider_ratio," car=", car_ratio," truck=",
          truck_ratio," bus=", bus_ratio," train=", train_ratio," motorcycle=", motorcycle_ratio," bicycle=",
          bicycle_ratio," ego_vehicle=", ego_vehicle_ratio," cl21=", cl21_ratio)
    #print(road_ratio+sidewalk_ratio+building_ratio+wall_ratio+fence_ratio+pole_ratio+traffic_light_ratio+traffic_sign_ratio+vegetation_ratio+terrain_ratio+sky_ratio+person_ratio+rider_ratio+car_ratio+truck_ratio+bus_ratio+train_ratio+motorcycle_ratio+bicycle_ratio+ego_vehicle_ratio+cl21_ratio)
    comfort_level(sidewalk_ratio, terrain_ratio, vegetation_ratio, fence_ratio, truck_ratio, traffic_light_ratio,
                  traffic_sign_ratio, person_ratio, car_ratio, bicycle_ratio)


classes_color_map = {
    'road': (150, 150, 150),  # road (и вода тут) cl1
    'sidewalk': (58, 55, 169),  # sidewalk(бордюр,брусчатка) cl2
    'building': (211, 51, 17),  # building (и мосты тут) cl3
    'wall': (157, 80, 44),  # wall(ограждения, шлагбаум)cl4
    'fence': (23, 95, 189),  # fence(большой забор,ограждения мостов)cl5
    'pole': (210, 133, 34),  # pole(столбы,фонари)cl6
    'traffic light': (76, 226, 202),  # traffic light cl7
    'traffic sign': (101, 138, 127),  # traffic sign (очень плохо) cl8
    'vegetation': (223, 91, 182),  # vegetation(только деревья, без травы) cl9
    'terrain': (80, 128, 113),  # terrain(трава,снег)cl10
    'sky': (235, 155, 55),  # sky cl11
    'person': (44, 151, 243),  # person cl12
    'rider': (159, 80, 170),  # rider?? cl13
    'car': (239, 208, 44),  # car cl14
    'truck': (128, 50, 51),  # truck cl15
    'bus': (82, 141, 193),  # bus cl16
    'train': (9, 107, 10),  # train cl17
    'motorcycle': (223, 90, 142),  # motorcycle cl18
    'bicycle': (50, 248, 83),  # bicycle cl19
    'ego-vehicle': (178, 101, 130),  # ego-vehicle??? cl20
    'cl21': (71, 30, 204),  # ????? cl21
}


def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument("-m", "--model", help="Required. Path to an .xml file with a trained model",
                      required=True, type=str)
    args.add_argument("-i", "--input", help="Required. Path to a folder with images or path to an image files",
                      required=True, type=str, nargs="+")
    args.add_argument("-l", "--cpu_extension",
                      help="Optional. Required for CPU custom layers. "
                           "Absolute MKLDNN (CPU)-targeted custom layers. Absolute path to a shared library with the "
                           "kernels implementations", type=str, default=None)
    args.add_argument("-d", "--device",
                      help="Optional. Specify the target device to infer on; CPU, GPU, FPGA, HDDL or MYRIAD is "
                           "acceptable. Sample will look for a suitable plugin for device specified. Default value is CPU",
                      default="CPU", type=str)
    args.add_argument("-nt", "--number_top", help="Optional. Number of top results", default=10, type=int)
    return parser


model = "semantic-segmentation-adas-0001.xml"
input=["Image_9_0.png","Image_9_120.png","Image_9_240.png"]
cpu_extension = None
device = 'CPU'
number_top = 10


def main():
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)

    log.info("Creating Inference Engine")
    ie = IECore()
    if cpu_extension and 'CPU' in device:
        ie.add_extension(cpu_extension, "CPU")
    # Read IR
    log.info("Loading network")
    net = ie.read_network(model, os.path.splitext(model)[0] + ".bin")

    if "CPU" in device:
        supported_layers = ie.query_network(net, "CPU")
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if len(not_supported_layers) != 0:
            log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(device, ', '.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      "or --cpu_extension command line argument")
            sys.exit(1)
    assert len(net.inputs.keys()) == 1, "Sample supports only single input topologies"
    assert len(net.outputs) == 1, "Sample supports only single output topologies"

    log.info("Preparing input blobs")
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    net.batch_size = len(input)

    # NB: This is required to load the image as uint8 np.array
    #     Without this step the input blob is loaded in FP32 precision,
    #     this requires additional operation and more memory.
    net.inputs[input_blob].precision = "U8"

    # Read and pre-process input images
    n, c, h, w = net.inputs[input_blob].shape
    images = np.ndarray(shape=(n, c, h, w))
    for i in range(n):
        image = cv2.imread(input[i])
        assert image.dtype == np.uint8
        if image.shape[:-1] != (h, w):
            log.warning("Image {} is resized from {} to {}".format(input[i], image.shape[:-1], (h, w)))
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        images[i] = image
    log.info("Batch size is {}".format(n))

    # Loading model to the plugin
    log.info("Loading model to the plugin")
    exec_net = ie.load_network(network=net, device_name=device)

    # Start sync inference
    log.info("Starting inference")
    res = exec_net.infer(inputs={input_blob: images})

    # Processing output blob
    log.info("Processing output blob")
    res = res[out_blob]
    if len(res.shape) == 3:
        res = np.expand_dims(res, axis=1)
    if len(res.shape) == 4:
        _, _, out_h, out_w = res.shape
    else:
        raise Exception("Unexpected output blob shape {}. Only 4D and 3D output blobs are supported".format(res.shape))
    road = 0
    sidewalk = 0
    building = 0
    wall = 0
    fence = 0
    pole = 0
    traffic_light = 0
    traffic_sign = 0
    vegetation = 0
    terrain = 0
    sky = 0
    person = 0
    rider = 0
    car = 0
    truck = 0
    bus = 0
    train = 0
    motorcycle = 0
    bicycle = 0
    ego_vehicle = 0
    cl21 = 0
    for batch, data in enumerate(res):
        classes_map = np.zeros(shape=(out_h, out_w, 3), dtype=np.int)
        for i in range(out_h):
            for j in range(out_w):
                if len(data[:, i, j]) == 1:
                    pixel_class = int(data[:, i, j])
                else:
                    pixel_class = np.argmax(data[:, i, j])
                classes_map[i, j, :] = classes_color_map[list(classes_color_map.keys())[min(pixel_class, 20)]]
                if min(pixel_class, 20) == 0:
                    road += 1
                elif min(pixel_class, 20) == 1:
                    sidewalk += 1
                elif min(pixel_class, 20) == 2:
                    building += 1
                elif min(pixel_class, 20) == 3:
                    wall += 1
                elif min(pixel_class, 20) == 4:
                    fence += 1
                elif min(pixel_class, 20) == 5:
                    pole += 1
                elif min(pixel_class, 20) == 6:
                    traffic_light += 1
                elif min(pixel_class, 20) == 7:
                    traffic_sign += 1
                elif min(pixel_class, 20) == 8:
                    vegetation += 1
                elif min(pixel_class, 20) == 9:
                    terrain += 1
                elif min(pixel_class, 20) == 10:
                    sky += 1
                elif min(pixel_class, 20) == 11:
                    person += 1
                elif min(pixel_class, 20) == 12:
                    rider += 1
                elif min(pixel_class, 20) == 13:
                    car += 1
                elif min(pixel_class, 20) == 14:
                    truck += 1
                elif min(pixel_class, 20) == 15:
                    bus += 1
                elif min(pixel_class, 20) == 16:
                    train += 1
                elif min(pixel_class, 20) == 17:
                    motorcycle += 1
                elif min(pixel_class, 20) == 18:
                    bicycle += 1
                elif min(pixel_class, 20) == 19:
                    ego_vehicle += 1
                else:
                    cl21 += 1
        out_img = os.path.join(os.path.dirname('__file__'), "out_{}.bmp".format(batch))
        cv2.imwrite(out_img, classes_map)
        log.info("Result image was saved to {}".format(out_img))
    class_size(road, sidewalk, building, wall, fence, pole, traffic_light, traffic_sign, vegetation, terrain, sky,
               person, rider, car, truck, bus, train, motorcycle, bicycle, ego_vehicle, cl21)

    log.info(
        "This demo is an API example, for any performance measurements please use the dedicated benchmark_app tool "
        "from the openVINO toolkit\n")


if __name__ == '__main__':
    sys.exit(main() or 0)