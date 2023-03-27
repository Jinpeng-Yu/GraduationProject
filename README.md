# GraduationProject
This crowd counting system is based on IIM algorithm.  
Reference Paper: [Density Map Regression Guided Detection Network for RGB-D Crowd Counting](https://openaccess.thecvf.com/content_CVPR_2019/papers/Lian_Density_Map_Regression_Guided_Detection_Network_for_RGB-D_Crowd_Counting_CVPR_2019_paper.pdf)

## Display
![数据可视化综合展板](/数据可视化综合展板.png)

# Crowd Counting Model
The crowd counting model I have implemented is based on [Gao](https://github.com/taohan10200/IIM)'s work. 
Because the size of the latest state model I finally got is over 100M, 
so I upload it to google drive. If you need my pretrained model, please click [Google Drive Link](https://drive.google.com/file/d/1JZdV7nN87vO-KBmnFCGAjYbO98s0s4Bp/view?usp=sharing) to download it and 
put it under the `latest_model` folder(`/GraduationProject/myapp/IIM/latest_model/`). 
However, I actually encourage you to implement this crowd counting model.

# Videos
I will share my [test videos](https://drive.google.com/drive/folders/10VDG6s5utLvzMYtXrSn7-30dvrn_06RB?usp=sharing) and [result videos](https://drive.google.com/drive/folders/1UN1jlNwMnBcnYMdAqlHW4w5rZ_MsZvWi?usp=sharing)

# Structure
This system is mainly based on `Vue` and `Django` structures, at the same time, I use the `ElementUI` and `Echarts` components to beautify the front-end display.
