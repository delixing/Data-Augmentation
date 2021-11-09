# Data-Augmentation
自己写的数据增强算法，请随意取用，包括椭圆旋转，随机复制
椭圆旋转是根据Towards Rotation Invariance in Object Detection这篇论文写的。
https://openaccess.thecvf.com/content/ICCV2021/papers/Kalra_Towards_Rotation_Invariance_in_Object_Detection_ICCV_2021_paper.pdf
通过将旋转的bbox从矩形转换为椭圆形，使得旋转后的bbox更好的拟合目标

![image](https://github.com/delixing/Data-Augmentation/blob/master/img/original.png)
![image](https://github.com/delixing/Data-Augmentation/blob/master/img/rotation.png)

随机复制是根据Augmentation for small object detection这篇论文写的
https://arxiv.org/pdf/1902.07296.pdf
因为在论文中oversample rate最好的情况是3倍，所以程序中用下面的策略进行：
1.首先随机挑选一张图片作为原图。
2.然后从数据集再随机挑选三张图片。
3.将三张图片中的目标拷贝到原图上去。
4.修改annotation文件。
本方法主要针对小目标的数据增强，因为考虑到覆盖的原因，所以请务必使用目标较小的，密度较低的数据集，不然会导致操作时间很长。
![image](https://github.com/delixing/Data-Augmentation/blob/master/img/copy_paste.png)

后续考虑在复制时添加旋转操作
