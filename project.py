#!/usr/bin/env python
from __future__ import print_function
import sys
import os
#from argparse import ArgumentParser, SUPPRESS
import cv2
import numpy as np
import logging as log
from time import time
from openvino.inference_engine import IECore
import glob
def class_size(cl1,cl2,cl3,cl4,cl5,cl6,cl7,cl8,cl9,cl10,cl11,cl12,cl13,cl14,cl15,cl16,cl17,cl18,cl19,cl20,cl21):
    sum_cl=cl1+cl2+cl3+cl4+cl5+cl6+cl7+cl8+cl9+cl10+cl11+cl12+cl13+cl14+cl15+cl16+cl17+cl18+cl9+cl20+cl21
    cl1_ratio=cl1/sum_cl
    cl2_ratio=cl2/sum_cl
    cl3_ratio=cl3/sum_cl
    cl4_ratio=cl5/sum_cl
    cl5_ratio=cl5/sum_cl
    cl6_ratio=cl6/sum_cl
    cl7_ratio=cl7/sum_cl
    cl8_ratio=cl8/sum_cl
    cl9_ratio=cl9/sum_cl
    cl10_ratio=cl10/sum_cl
    cl11_ratio=cl11/sum_cl
    cl12_ratio=cl12/sum_cl
    cl13_ratio=cl13/sum_cl
    cl14_ratio=cl14/sum_cl
    cl15_ratio=cl15/sum_cl
    cl16_ratio=cl16/sum_cl
    cl17_ratio=cl17/sum_cl
    cl18_ratio=cl18/sum_cl
    cl19_ratio=cl19/sum_cl
    cl20_ratio=cl20/sum_cl
    cl21_ratio=cl21/sum_cl
    sum_cl_ratio=cl1_ratio+cl2_ratio+cl3_ratio+cl4_ratio+cl5_ratio+cl6_ratio+cl7_ratio+cl8_ratio+cl9_ratio+cl10_ratio+cl11_ratio+cl12_ratio+cl13_ratio+cl14_ratio+cl15_ratio+cl16_ratio+cl17_ratio+cl18_ratio+cl19_ratio+cl20_ratio+cl21_ratio
    print("Resalt raiting:"
          "\n road          ",cl1_ratio,
          "\n sidewalk      ", cl2_ratio,
          "\n building      ", cl3_ratio,
          "\n wall          ", cl4_ratio,
          "\n fence         ", cl5_ratio,
          "\n pole          ", cl6_ratio,
          "\n traffic light ", cl7_ratio,
          "\n traffic sign  ", cl8_ratio,
          "\n vegetation    ", cl9_ratio,
          "\n terrain       ", cl10_ratio,
          "\n sky           ", cl11_ratio,
          "\n person        ", cl12_ratio,
          "\n rider         ", cl13_ratio,
          "\n car           ", cl14_ratio,
          "\n truck         ", cl15_ratio,
          "\n bus           ", cl16_ratio,
          "\n train         ", cl17_ratio,
          "\n motorcycle    ", cl18_ratio,
          "\n bicycle       ", cl19_ratio,
          "\n ego-vehicle?? ", cl20_ratio,
          "\n ?????         ", cl21_ratio)
    print(sum_cl_ratio)
    print(sum_cl)

classes_color_map = [
    (150, 150, 150),# road (и вода тут) cl1
    (58, 55, 169),#sidewalk(бордюр,брусчатка) cl2
    (211, 51, 17),#building (и мосты тут) cl3
    (157, 80, 44),# wall(ограждения, шлагбаум)cl4
    (23, 95, 189),#fence(большой забор,ограждения мостов)cl5
    (210, 133, 34),#pole(столбы,фонари)cl6
    (76, 226, 202),#traffic light cl7
    (101, 138, 127),#traffic sign (очень плохо) cl8
    (223, 91, 182),#vegetation(только деревья, без травы) cl9
    (80, 128, 113),#terrain(трава,снег)cl10
    (235, 155, 55),#sky cl11
    (44, 151, 243),#person cl12
    (159, 80, 170),#rider?? cl13
    (239, 208, 44),#car cl14
    (128, 50, 51),#truck cl15
    (82, 141, 193),#bus cl16
    (9, 107, 10),#train cl17
    (223, 90, 142),#motorcycle cl18
    (50, 248, 83),#bicycle cl19
    (178, 101, 130),#ego-vehicle??? cl20
    (71, 30, 204),#????? cl21
]
#N = len(classes_color_map)

"""
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
"""

model = 'semantic-segmentation-adas-0001.xml'
cpu_extension=None
device='CPU'
number_top=10

folders = glob.glob('pictures')
input = []
for folder in folders:
       for f in glob.glob(folder+'/*.bmp'):
           input.append(f)

print(input)

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
        
    #classes=np.zeros(N)
    for batch, data in enumerate(res):
        cl1=0
        cl2=0
        cl3=0
        cl4=0
        cl5=0
        cl6=0
        cl7=0
        cl8=0
        cl9=0
        cl10=0
        cl11=0
        cl12=0
        cl13=0
        cl14=0
        cl15=0
        cl16=0
        cl17=0
        cl18=0
        cl19=0
        cl20=0
        cl21=0
        classes_map = np.zeros(shape=(out_h, out_w, 3), dtype=np.int)
        for i in range(out_h):
            for j in range(out_w):
                if len(data[:, i, j]) == 1:
                    pixel_class = int(data[:, i, j])
                else:
                    pixel_class = np.argmax(data[:, i, j])
                classes_map[i, j, :] = classes_color_map[min(pixel_class, 20)] 
                if min(pixel_class, 20)==0:
                    cl1+=1
                elif min(pixel_class, 20)==1:
                    cl2+=1
                elif min(pixel_class, 20)==2:
                    cl3+=1
                elif min(pixel_class, 20)==3:
                    cl4+=1
                elif min(pixel_class, 20)==4:
                    cl5+=1
                elif min(pixel_class, 20)==5:
                    cl6+=1
                elif min(pixel_class, 20)==6:
                    cl7+=1
                elif min(pixel_class, 20)==7:
                    cl8+=1
                elif min(pixel_class, 20)==8:
                    cl9+=1
                elif min(pixel_class, 20)==9:
                    cl10+=1
                elif min(pixel_class, 20)==10:
                    cl11+=1
                elif min(pixel_class, 20)==11:
                    cl12+=1
                elif min(pixel_class, 20)==12:
                    cl13+=1
                elif min(pixel_class, 20)==13:
                    cl14+=1
                elif min(pixel_class, 20)==14:
                    cl15+=1
                elif min(pixel_class, 20)==15:
                    cl16+=1
                elif min(pixel_class, 20)==16:
                    cl17+=1
                elif min(pixel_class, 20)==17:
                    cl18+=1
                elif min(pixel_class, 20)==18:
                    cl19+=1
                elif min(pixel_class, 20)==19:
                    cl20+=1
                else:
                    cl21+=1
        class_size(cl1,cl2,cl3,cl4,cl5,cl6,cl7,cl8,cl9,cl10,cl11,cl12,cl13,cl14,cl15,cl16,cl17,cl18,cl19,cl20,cl21)
        out_img = os.path.join(os.path.dirname('__file__'), "out_{}.bmp".format(batch))
        cv2.imwrite(out_img, classes_map)
        log.info("Result image was saved to {}".format(out_img))
    log.info("This demo is an API example, for any performance measurements please use the dedicated benchmark_app tool "
             "from the openVINO toolkit\n")

if __name__ == '__main__':
    sys.exit(main() or 0)