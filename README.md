<p>
    <a align="center" href="https://github.com/Robo-pioneer" target="_blank">
      <img width="100%" src="https://raw.githubusercontent.com/Robo-pioneer/Armor-Yolov5ver/master/splash.png"></a>
</p>

## **Armor-Yolov5ver**

[简体中文](README.zh-CN.md)

**A program for armor recognition in RoboMaster Youth Challenge (RMYC) based on yolov5**

**Firstly, thanks to Gavin_xiang’s** [**code**](https://gitee.com/Gavin_xiang666/aim-bot2023-abandonment-plan) **and** [**model**](https://bbs.robomaster.com/forum.php?mod=viewthread&tid=22626)**, this program is modified based upon this foundation.**

For the related introduction of yolov5, please refer to [yolov5-README](yolov5-README.md) in the repository.



**Related data (based on Gavin_xiang’s published model)**

| Testing Platform          | Acceleration                                          | Inference Time/ms  | Total Time/ms TPS Average | Remarks                                                      |
| ------------------------- | ----------------------------------------------------- | ------------------ | ------------------------- | ------------------------------------------------------------ |
| CPU:i7-4700HQ GPU:GTX960m | \                                                     | N/A                | 5ms 17 FPS               | [Test by Gavin_xiang’s](https://bbs.robomaster.com/forum.php?mod=viewthread&tid=22626) |
| Jetson Tx2 NX             | Pythorch acceleration (without TensorRT acceleration) | 0.9 ms             | 11ms 8 FPS                | Test result in Robo-pioneer team (with secondary verification turned off) |
| Jetson NANO               | Pythorch acceleration (without TensorRT acceleration) | To be supplemented | To be supplemented        | To be supplemented                                           |
|                           |                                                       |                    |                           |                                                              |

###### 

**Plan：**

• Perfect secondary verification

• Integrate PID (because the Python on EP is too limited and the PID is put on Jetson to ensure program stability.)

• TensorRT acceleration.



#### **Installation (only applicable to Jetson TX2/NANO devices)**

Complete records can refer to [nano 的yolov5环境配置 # 2](https://github.com/Robo-pioneer/RMYC/issues/2).



**Clone this repository and install the environment required by yolov5.**

```bash
$ git clone https://github.com/Robo-pioneer/Armor-Yolov5ver.git
$ cd Armor-Yolov5ver
$ pip3 -r requirements.txt
```



**Installation of PyTorch and Torch Vision**[PyTorch for Jetson](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048)



For Jetson Nano and Jetson Tx2 NX, JetPack 4.6 is only supported. Please download [torch-1.10.0-cp36-cp36m-linux_aarch64.whl](https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl) compatible with Python 3.6 supported software packages with JetPack 4.4 (L4T R32.4.3) / JetPack 4.4.1 (L4T R32.4.4) / JetPack 4.5 (L4T R32.5.0) / JetPack 4.5.1 (L4T R32.5.1) / JetPack 4.6 (L4T R32.6.1).



To use PyTorch Vision, you need to compile it yourself, please first install [NVIDIA JetPack](https://docs.nvidia.com/jetson/jetpack/install-jetpack/index.html) on Jetson.



==Note that Jetpack requires a large storage space, please ensure that there is more than 4GB of free space on your device.==



At the same time, the compilation time of PyTorch Vision is also very long. It is recommended to use the “screen” command to prevent ssh from disconnecting.

```bash
$ wget LINK_OF_PYTHORCH_WHL
$ pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl
$ sudo apt update
$ sudo apt install nvidia-jetpack  # Please check the remaining space of the device before running it.
```



The following command is used to compile PyTorch Vision:

```bash
$ sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
$ git clone --branch release/0.11 https://github.com/pytorch/vision.git
$ cd vision
$ export BUILD_VERSION=0.x.0 # Change the version to 0.11.1
$ python3 setup.py install --user # The compile process is older.
$ cd ../ # attempting to load torchvision from build dir will result in import error
$ pip install 'pillow<7'
```



**Configuration before running**

Modify YOUR_PASSWORD in the [autorun](autorun.sh) script to the device’s password

And also modify the following python code to recognize armor colors:

armor_color = "blue" # Set the color of the armor to recognize



**Run**

```bash
bash autorun.sh
```



Finally, thanks to Gavin_xiang for the basic code and guidance. If you have any questions, please feel free to submit an issue for discussion.
