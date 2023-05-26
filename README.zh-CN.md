<p>
    <a align="center" href="https://github.com/Robo-pioneer" target="_blank">
      <img width="100%" src="https://raw.githubusercontent.com/Robo-pioneer/Armor-Yolov5ver/master/splash.png"></a>
</p>

# Armor-Yolov5ver

#### 基于 yolov5 的 RoboMaster青少年对抗赛（RMYC）装甲板识别程序

##### 首先感谢 Gavin_xiang 的[代码](https://gitee.com/Gavin_xiang666/aim-bot2023-abandonment-plan)与[模型](https://bbs.robomaster.com/forum.php?mod=viewthread&tid=22626)，本程序是基于此基础上修改而来的

对于yolov5的相关介绍可以参考仓库中的 [yolov5-README](yolov5-README.md) 

###### 相关数据(基于Gavin_xiang公布的模型)

| 测试平台                   | 加速                               | 推理用时/ms | 单词运行总用时/ms TPS 平均 | 备注                                                         |
| -------------------------- | ---------------------------------- | ----------- | -------------------------- | ------------------------------------------------------------ |
| cpu:i7-4700HQ 显卡:GTX960m | \                                  | N/A         | 0.05 17 FPS                | [基于Gavin_xiang的测试](https://bbs.robomaster.com/forum.php?mod=viewthread&tid=22626) |
| Jetson Tx2 NX              | Pythorch加速（未使用TensorRT加速） | 0.9 ms      | 0.11 8 FPS                 | Robo-pioneer 组内测试结果（关闭二次验证）                    |
| Jetson NANO                | Pythorch加速（未使用TensorRT加速） | 待补充      | 待补充                     | 待补充                                                       |
|                            |                                    |             |                            |                                                              |

###### 计划：

- 完善二次验证
- 将PID加入（原因是EP上的Python受限太多将PID放在Jetson上运行保证程序稳定）
- TensorRT加速



#### 安装（仅适用于Jetson TX2/NANO 设备）

全记录可参考 [nano 的yolov5环境配置 # 2](https://github.com/Robo-pioneer/RMYC/issues/2)

**克隆本仓库并安装yolov5 所需环境**

```bash
$ git clone https://github.com/Robo-pioneer/Armor-Yolov5ver.git
$ cd Armor-Yolov5ver
$ pip3 -r requirements.txt
```



**安装 PyTorch 和 Torch Vision**
[PyTorch for Jetson](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048)

对于 Jetson Nano和Jetson Tx2 NX，仅支持 JetPack 4.6。请下载与 JetPack 4.4 (L4T R32.4.3) / JetPack 4.4.1 (L4T R32.4.4) / JetPack 4.5 (L4T R32.5.0) / JetPack 4.5.1 (L4T R32.5.1) / JetPack 4.6 (L4T R32.6.1) 兼容的 Python 3.6 支持的软件包 [torch-1.10.0-cp36-cp36m-linux_aarch64.whl](https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl)。

要使用 PyTorch Vision，您需要自行编译它，请先在 Jetson 上安装 [NVIDIA JetPack](https://docs.nvidia.com/jetson/jetpack/install-jetpack/index.html)。

==请注意 jetpack需要的储存空间占用较大 请保证您的设备剩余空间在4G以上==

同时 PyTorch Vision 的编译时间也非常长 建议使用 screen 命令防止ssh断开连接

```bash
$ wget LINK_OF_PYTHORCH_WHL
$ pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl
$ sudo apt update
$ sudo apt install nvidia-jetpack #运行前请检查设备剩余空间
```

下面是编译 PyTorch Vision 的命令：

```bash
$ sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
$ git clone --branch release/0.11 https://github.com/pytorch/vision.git
$ cd vision
$ export BUILD_VERSION=0.x.0 # 将版本修改为 0.11.1
$ python3 setup.py install --user #编译过程比较久
$ cd ../ # attempting to load torchvision from build dir will result in import error
$ pip install 'pillow<7'
```



**运行前设置**

修改[autorun](autorun.sh)脚本中的YOUR_PASSWORD为设备密码

并修改python 识别颜色

```py
armor_color = "blue"#设置识别装甲板的颜色
```



**运行**

```bash
bash autorun.sh
```



最后感谢Gavin_xiang的基础代码和指导，有任何问题欢迎发issue一起讨论
