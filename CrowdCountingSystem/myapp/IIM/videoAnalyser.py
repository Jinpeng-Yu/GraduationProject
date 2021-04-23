import os
import cv2
import torch
import tqdm
import torch.nn.functional as F
from torch.autograd import Variable
import torchvision.transforms as standard_transforms
from .model.locator import Crowd_locator
from collections import OrderedDict
from .misc.utils import *
from PIL import Image
from collections import OrderedDict

# 数据
dataset = 'NWPU'
dataRoot = '../ProcessedData/' + dataset
video_path = dataRoot + '/videos/test.mp4'
new_video_path = dataRoot + '/videos/new_video4.avi'
# frames_save_path = dataRoot + '/frames'
# frames_path = dataRoot + '/frames/'
frames_save_path = dataRoot + '/frames'
frames_path = dataRoot + '/frames/'
video_list = 'video_list.txt'


# GPUs
# GPU_ID = '0,1,2,3'
GPU_ID = ''
# os.environ["CUDA_VISIBLE_DEVICES"] = GPU_ID
# torch.backends.cudnn.benchmark = True  # 提升卷积神经网络计算速度，但是有条件限制

device = ('cuda' if torch.cuda.is_available() else 'cpu')

# 模型
net_name = 'HR_Net'
model_path = './latest_model/latest_state_model.pth'

# 模型输出
out_file_name = './saved_exp_results/' + dataset + '_' + net_name + '_' + video_list

if dataset == 'NWPU':
    mean_std = ([0.446139603853, 0.409515678883, 0.395083993673], [0.288205742836, 0.278144598007, 0.283502370119])
if dataset == 'SHHA':
    mean_std = ([0.410824894905, 0.370634973049, 0.359682112932], [0.278580576181, 0.26925137639, 0.27156367898])
if dataset == 'SHHB':
    mean_std = ([0.452016860247, 0.447249650955, 0.431981861591], [0.23242045939, 0.224925786257, 0.221840232611])   
if dataset == 'QNRF':
    mean_std = ([0.413525998592, 0.378520160913, 0.371616870165], [0.284849464893, 0.277046442032, 0.281509846449])  
if dataset == 'FDST':
    mean_std = ([0.452016860247, 0.447249650955, 0.431981861591], [0.23242045939, 0.224925786257, 0.221840232611])  
if dataset == 'JHU':
    mean_std = ([0.429683953524, 0.437104910612, 0.421978861094], [0.235549390316, 0.232568427920, 0.2355950474739]) 

# torchvision.transforms是pytorch中的图像预处理包，一般使用Compose把多个步骤整合到一起
img_transform = standard_transforms.Compose([
        standard_transforms.ToTensor(), # convert a PIL image to tensor(H*W*C) in range [0, 255] to a torch.Tensor(C*H*W) in the range[0.0, 1.0]
                                        # c: 图像通道数 h:图像高度 w:图像宽度 
        standard_transforms.Normalize(*mean_std) # Normalized an tensor image with mean and standard devistion
    ])

def main():
    # video2frame(video_path, frames_save_path, 350)
    txtpath = os.path.join(dataRoot, video_list)
    print(txtpath)
    with open(txtpath) as f:
        lines = f.readlines()
    print(lines)
    analysis(lines, model_path)
    # frame_visual()
    # frame2video(frames_path, new_video_path, 30)

def video2frame(video_path, frames_save_path, time_interval):

    video_capture = cv2.VideoCapture(video_path)
    success, frame = video_capture.read()
    flag, count = 0, 1
    while success:
        
        if flag % time_interval == 0:
            cv2.imencode('.jpg', frame)[1].tofile(frames_save_path + '/%04d.jpg' % count)
            count += 1
        
        flag += 1
        success, frame = video_capture.read()

    txtpath = os.path.join(dataRoot, video_list)
    with open(txtpath, 'w') as f:
        for i in range(1, count):
            f.write(str(i).zfill(4) + '\n')
        f.close()

    print(count-1)

def frame2video(frame_dir, video_dir, fps):
    image_list = os.listdir(frame_dir)
    image_list.sort(key=lambda x: int(x.split('.')[0]))
    img = Image.open(os.path.join(frame_dir, image_list[0]))
    image_size = img.size  # 获得图像的分辨率，frame_dir文件夹下的图片分辨率要一致

    # fourcc = cv2.cv.CV_FOURCC('M','J','P','G') #opencv 2
    fourcc = cv2.VideoWriter_fourcc(*'XVID') #opencv 3
    videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, image_size)
    
    for i in image_list:
        image_name = os.path.join(frame_dir + i)
        frame = cv2.imdecode(np.fromfile(image_name, dtype=np.uint8), -1)
        videoWriter.write(frame)
    videoWriter.release()
    print('finish')

def get_boxInfo_from_Binar_map(Binar_numpy, min_area=3):
    Binar_numpy = Binar_numpy.squeeze().astype(np.uint8)
    assert Binar_numpy.ndim == 2
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(Binar_numpy, connectivity=4)  # centriod (w,h)

    boxes = stats[1:, :]
    points = centroids[1:, :]
    index = (boxes[:, 4] >= min_area)
    boxes = boxes[index]
    points = points[index]
    pre_data = {'num': len(points), 'points': points}
    return pre_data, boxes

def analysis(file_list, model_path):
    
    net = Crowd_locator(net_name,GPU_ID,pretrained=True)
    # net.cuda()
    net.to(device)
    state_dict = torch.load(model_path, map_location='cpu')
    if len(GPU_ID.split(','))>1:
        net.load_state_dict(state_dict)
    else:
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k.replace('module.', '')
            new_state_dict[name] = v
        net.load_state_dict(new_state_dict)
    net.eval()

    file_list = tqdm.tqdm(file_list)
    for infos in file_list:
        filename = infos.split()[0]

        imgname = os.path.join(dataRoot, 'frames', filename + '.jpg')
        img = Image.open(imgname)

        if img.mode == 'L':
            img = img.convert('RGB')
        img = img_transform(img)[None, :, :, :]
        slice_h, slice_w = 512, 1024
        slice_h, slice_w = slice_h, slice_w
        with torch.no_grad():
            # img = Variable(img).cuda()
            img = Variable(img).to(device)
            b, c, h, w = img.shape
            crop_imgs, crop_dots, crop_masks = [], [], []
            if h * w < slice_h * 2 * slice_w * 2 and h % 16 == 0 and w % 16 == 0:
                [pred_threshold, pred_map, __] = [i.cpu() for i in net(img, mask_gt=None, mode='val')]
            else:
                if h % 16 != 0:
                    pad_dims = (0, 0, 0, 16 - h % 16)
                    h = (h // 16 + 1) * 16
                    img = F.pad(img, pad_dims, "constant")


                if w % 16 != 0:
                    pad_dims = (0, 16 - w % 16, 0, 0)
                    w = (w // 16 + 1) * 16
                    img = F.pad(img, pad_dims, "constant")


                for i in range(0, h, slice_h):
                    h_start, h_end = max(min(h - slice_h, i), 0), min(h, i + slice_h)
                    for j in range(0, w, slice_w):
                        w_start, w_end = max(min(w - slice_w, j), 0), min(w, j + slice_w)
                        crop_imgs.append(img[:, :, h_start:h_end, w_start:w_end])
                        mask = torch.zeros(1,1,img.size(2), img.size(3)).cpu()
                        mask[:, :, h_start:h_end, w_start:w_end].fill_(1.0)
                        crop_masks.append(mask)
                crop_imgs, crop_masks =  torch.cat(crop_imgs, dim=0), torch.cat(crop_masks, dim=0)

                # forward may need repeating
                crop_preds, crop_thresholds = [], []
                nz, period = crop_imgs.size(0), 4
                for i in range(0, nz, period):
                    [crop_threshold, crop_pred, __] = [i.cpu() for i in net(crop_imgs[i:min(nz, i+period)],mask_gt = None, mode='val')]
                    crop_preds.append(crop_pred)
                    crop_thresholds.append(crop_threshold)

                crop_preds = torch.cat(crop_preds, dim=0)
                crop_thresholds = torch.cat(crop_thresholds, dim=0)

                # splice them to the original size
                idx = 0
                pred_map = torch.zeros(b, 1, h, w).cpu()
                pred_threshold = torch.zeros(b, 1, h, w).cpu().float()
                for i in range(0, h, slice_h):
                    h_start, h_end = max(min(h - slice_h, i), 0), min(h, i + slice_h)
                    for j in range(0, w, slice_w):
                        w_start, w_end = max(min(w - slice_w, j), 0), min(w, j + slice_w)
                        pred_map[:, :, h_start:h_end, w_start:w_end] += crop_preds[idx]
                        pred_threshold[:, :, h_start:h_end, w_start:w_end] += crop_thresholds[idx]
                        idx += 1
                mask = crop_masks.sum(dim=0)
                pred_map = (pred_map / mask)
                pred_threshold = (pred_threshold / mask)

            a = torch.ones_like(pred_map)
            b = torch.zeros_like(pred_map)
            binar_map = torch.where(pred_map >= pred_threshold, a, b)

            pred_data, boxes = get_boxInfo_from_Binar_map(binar_map.cpu().numpy())

            with open(out_file_name, 'a') as f:

                f.write(filename + ' ')
                f.write(str(pred_data['num']) + ' ')
                for ind,point in enumerate(pred_data['points'],1):
                    if ind < pred_data['num']:
                        f.write(str(int(point[0])) + ' ' + str(int(point[1])) + ' ')
                    else:
                            f.write(str(int(point[0])) + ' ' + str(int(point[1])))
                f.write('\n')
                f.close()

def read_pred(pred_file):
    # read pred
    pred_data = {}
    with open(pred_file) as f:
        
        id_read = []
        for line in f.readlines():
            line = line.strip().split(' ')

            # check1
            if len(line) <2 or len(line) % 2 !=0 or (len(line)-2)/2 != int(line[1]):
                flagError = True
                sys.exit(1)

            line_data = [int(i) for i in line]
            idx, num = [line_data[0], line_data[1]]
            id_read.append(idx)

            points = []
            if num>0:
                points = np.array(line_data[2:]).reshape(((len(line)-2)//2,2))
                pred_data[idx] = {'num': num, 'points':points}
            else:
                pred_data[idx] = {'num': num, 'points':[]}
    
    return pred_data

def frame_visual():

    pred_data = read_pred(out_file_name)

    id_std = [i for i in range(1,len(pred_data)+1)]

    print("Waiting")

    for i_sample in id_std:

        # print(i_sample)

        pred_p = pred_data[i_sample]['points']

        img = cv2.imread(frames_path + str(i_sample).zfill(4) + '.jpg')

        point_r_value = 5
        if pred_data[i_sample]['num']  != 0:
            for i in range(pred_p.shape[0]):
                cv2.circle(img,(pred_p[i][0],pred_p[i][1]),point_r_value * 2,(0,255,0),-1)# tp: green
        cv2.putText(img,'number: '+ str(len(pred_p)),(860,100),cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,255,0), 5)
        cv2.imwrite(frames_save_path+'/'+str(i_sample).zfill(4) + '.jpg', img)    



if __name__ == '__main__':
    main()