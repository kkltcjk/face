# -*- coding: UTF-8 -*-
import os
import sys
import shutil
import subprocess
import threadpool

from face.common import utils

reload(sys)
sys.setdefaultencoding('utf8')

###########################
#函数功能：根据输入文件，读取其下的票务结构化信息
#函数输入：票务信息文件，一天
#函数输出：票务结构化信息，一天
###########################
def get_ticket_struct_info(proc_path):
    ticket_struct_info_list = []
    ticket_file_handle = open(proc_path,"r")
    lines = ticket_file_handle.readlines()
    ticket_file_handle.close()
    # 不处理票务表头信息
    del lines[0]
    for line in lines:
        line = line.strip("\n")
        checkintime_string = line.split("#")[1]
        checkintime_year = int(checkintime_string.split(" ")[0].split("-")[0])
        checkintime_month = int(checkintime_string.split(" ")[0].split("-")[1])
        checkintime_day = int(checkintime_string.split(" ")[0].split("-")[2])
        checkintime_hour = int(checkintime_string.split(" ")[1].split(":")[0])
        checkintime_min = int(checkintime_string.split(" ")[1].split(":")[1])
        checkintime_sec = int(checkintime_string.split(" ")[1].split(":")[2])
        checkintime_in_sec = time_to_sec(checkintime_hour, checkintime_min, checkintime_sec)
        checkinwindow = line.split("#")[3]
        checkidno = line.split("#")[4]

        ticket_struct_info = [checkidno,checkinwindow,checkintime_year,checkintime_month,checkintime_day,checkintime_in_sec]
        ticket_struct_info_list.append(ticket_struct_info)
    return ticket_struct_info_list

###########################
#函数功能：根据输入的时分秒将
#函数输入：时、分、秒
#函数输出：秒
###########################
def time_to_sec(hour,min,sec):
    time_in_sec = 3600 * hour + 60 * min + sec
    return time_in_sec

###########################
#函数功能：根据输入的文件夹，返还需要处理的多天票务信息
#函数输入：票务信息文件夹
#函数输出：票务结构化信息，多天
###########################
def get_ticket_struct_info_days(proc_path):
    days_ticket_info_list = []
    for proc_path_next in os.listdir(proc_path):
        if "ticket_info" not in proc_path_next:
            continue
        ticket_info_path = os.path.join(proc_path,proc_path_next)
        days_ticket_info_list = days_ticket_info_list + get_ticket_struct_info(ticket_info_path)
    return days_ticket_info_list

##########################
#函数功能：获取用于爬虫的身份信息库
#函数输入：爬虫身份信息库路径
#函数输出：爬虫身份信息结构化信息
##########################
def get_cluster_id_struct_info(proc_path):
    id_info_list = []

    for proc_path_next in os.listdir(proc_path):
        if not proc_path_next.endswith(".jpg"):
            continue
        if " " in proc_path_next:
            continue
        id_card_num = proc_path_next.split(".")[0]
        id_card_name = id_card_num + ".jpg"
        id_info_name = id_card_num + ".json"
        id_card_path = os.path.join(proc_path,id_card_name)
        id_info_path = os.path.join(proc_path,id_info_name)

        id_info_list.append([id_card_num,id_card_path,id_info_path])

    return id_info_list

###########################
#函数功能：处理截图文件夹，获取id对应的时间信息
#函数输入：截图文件夹路径
#函数输出：输出截图id的结构化信息
###########################
def get_cut_id_struct_info(proc_path):
    id_base_path = proc_path
    id_frame_list = []
    for id_base_path_next in os.listdir(id_base_path):
        if not os.path.isdir(os.path.join(id_base_path, id_base_path_next)):
            continue
        ipc_path = os.path.join(os.path.join(id_base_path, id_base_path_next))
        ipc_name = id_base_path_next
        ipc_no = id_base_path_next.split("_")[0]
        for ipc_path_path_next in os.listdir(ipc_path):
            if not os.path.isdir(os.path.join(ipc_path, ipc_path_path_next)):
                continue
            id_path = os.path.join(os.path.join(ipc_path, ipc_path_path_next))
            frame_list = []
            for id_path_next in os.listdir(id_path):
                if not id_path_next.endswith('.jpg'):
                    continue
                frame = int(id_path_next.split(".")[0].split("_")[-1])
                frame_list.append(frame)
            if frame_list == []:
                continue
            frame_list.sort()
            all_time_info = get_id_time(ipc_name, frame_list[0])
            id_frame = [id_path,ipc_no,all_time_info[0],all_time_info[1],all_time_info[2],all_time_info[3]]
            id_frame_list.append(id_frame)
    return id_frame_list

#########################
#函数功能：根据视频名和帧号信息获取截图产生id对应的秒数
#函数输入：视频名、id起始帧号
#函数输出：返还id对应的年月日秒信息
#########################
def get_id_time(ipc_name,start_frame):
    #获取视频名中的时间信息
    year = int(ipc_name.split("_")[1])
    month = int(ipc_name.split("_")[2])
    day = int(ipc_name.split("_")[3])
    hour = int(ipc_name.split("_")[4])
    min = int(ipc_name.split("_")[5])
    sec = int(ipc_name.split("_")[6])

    #视频秒数
    video_start_time = time_to_sec(hour,min,sec)
    start_frame_time = get_time_by_frame(start_frame)
    id_time_in_sec = video_start_time + start_frame_time

    return [year,month,day,id_time_in_sec]

##########################
#函数功能：将帧号转换为秒数
#函数输入：帧号
#函数输出：秒数
##########################
def get_time_by_frame(frame_count):
    #定义帧率
    frame_rate = 25.0
    #获取一帧的时间
    time_one_frame = 1 / frame_rate
    #获取总时间,四舍五入
    time_all_frame = int(frame_count * time_one_frame + 0.5)

    return time_all_frame

##########################
#函数功能：按照#连接的方式写二维列表到文件中
#函数输入：二维列表，存储文件路径
#函数输出：无
##########################
def write_2d_list(list_2d,sava_file_path):
    sava_file_path_handle = open(sava_file_path,"w")
    for list_item in list_2d:
        sava_file_path_handle.write("%s\n" % ("#".join([str(a) for a in list_item])))
    sava_file_path_handle.close()

##########################
#函数功能：用于获得每个id的搜索范围
#函数输入：ticket_struct_info_days_list、cut_id_struct_info_list、cluster_id_struct_info_list
#函数输出：id及搜索范围列表
##########################
def get_cluster_id_range(cluster_id_struct_info_list,ticket_struct_info_days_list,cut_id_struct_info_list,IPC_check):
    cluster_id_search_range_list = []
    for cluster_id_struct_info in cluster_id_struct_info_list:
        id_num = cluster_id_struct_info[0]

        find_id_ticket_info = my_find(id_num, 0, ticket_struct_info_days_list)
        #check_window = find_id_ticket_info[1]
        id_ticket_year  = find_id_ticket_info[2]
        id_ticket_month = find_id_ticket_info[3]
        id_ticket_day   = find_id_ticket_info[4]
        id_ticket_sec   = find_id_ticket_info[5]
        #根据条件查找对应id满足条件的cut_id范围
        cluster_id_search_range = find_id_frame_list(cut_id_struct_info_list, IPC_check, id_ticket_year, \
                                                          id_ticket_month, id_ticket_day, id_ticket_sec)
        cluster_id_search_range_list.append([id_num] + cluster_id_search_range)
    return cluster_id_search_range_list

##########################
#函数功能：获取每个id的搜索范围
#函数输入：截图文件列表、年、月、日、秒
#函数输出：对应ID的搜索范围
##########################
def find_id_frame_list(cut_id_struct_info_list,IPC_check,year,month,day,sec):
    cluster_id_list = []
    #人证卡口时间差定义,单位秒：
    check_ipc_before = 3 * 60
    check_ipc_after = 1 * 60
    #其他卡口时间差定义,单位秒：
    other_ipc_before = 20 * 60
    other_ipc_after = 120 * 60
    #全天秒数上限
    one_day_sec = 24 * 3600

    for cut_id_struct_info in cut_id_struct_info_list:
        if cut_id_struct_info[1] in IPC_check:
            before_time_sec = sec - check_ipc_before if sec - check_ipc_before > 0 else 0
            after_time_sec = sec + check_ipc_after if sec + check_ipc_after < one_day_sec else one_day_sec
        else:
            before_time_sec = sec - other_ipc_before if sec - other_ipc_before > 0 else 0
            after_time_sec = sec + other_ipc_after if sec + other_ipc_after < one_day_sec else one_day_sec

        if cut_id_struct_info[1] in IPC_check:
            if cut_id_struct_info[2] != year:
                continue
            if cut_id_struct_info[3] != month:
                continue
            if cut_id_struct_info[4] != day:
                continue

            if cut_id_struct_info[5] >= before_time_sec and cut_id_struct_info[5] <= after_time_sec:
                cluster_id_list.append(cut_id_struct_info[0])
        else:
            if cut_id_struct_info[2] != year:
                continue
            if cut_id_struct_info[3] != month:
                continue
            if cut_id_struct_info[4] != day:
                continue
            if cut_id_struct_info[5] >= before_time_sec and cut_id_struct_info[5] <= after_time_sec:
                cluster_id_list.append(cut_id_struct_info[0])

    return cluster_id_list


##########################
#函数功能：用于以二维数组某列值来查找返还整行
#函数输入：查找关键词、被查列表、查找列数
#函数输出：查找到的第一行
##########################
#根据值和列数返回固定的列,只返还一个
def my_find(value,col_num,query_list):
    return [a for a in query_list if a[col_num] == value][0]
##########################
#函数功能：用于以二维数组某列值来查找返还整行
#函数输入：查找关键词、被查列表、查找列数
#函数输出：查找到的所有行
##########################
def my_finds(value,col_num,query_list):
    return [a for a in query_list if a[col_num] == value]

##########################
#函数功能：写文件用于依图聚类
#函数输入：id_score_path、cut_id_struct_info_list、cluster_id_struct_info_list
#函数输出：无
##########################
def creat_file_to_cluster(id_score_path,cut_id_struct_info_list,cluster_id_struct_info_list):
    id_score_file_handle = open(id_score_path,"a+")
    for cluster_id_struct_info in cluster_id_struct_info_list:
        img_path = cluster_id_struct_info[1]
        image_name = img_path.split("/")[-1]
        img_base_path = "/".join(img_path.split("/")[:-1])
        id_score_file_handle.write("%s#%s\n" % (img_base_path,image_name))
    for cut_id_struct_info in cut_id_struct_info_list:
        id_path = cut_id_struct_info[0]
        id_name = id_path.split("/")[-1]
        id_pic_list =get_id_pic_by_score(id_path)
        id_score_file_handle.write("%s#%s\n" % (id_path, id_pic_list))
    id_score_file_handle.close()

##########################
#函数功能：根据质量分数排出五个质量分数最高的图片
#函数输入：id_path
#函数输出：无
##########################
def get_id_pic_by_score(id_path):
    id_pic_info_list = get_id_pic_list(id_path)
    id_pic_list = sort_list(id_pic_info_list)
    if len(id_pic_list) > 5:
        id_pic_list = id_pic_list[0:5]
    else:
        pass
    return "#".join(id_pic_list)
##########################
#函数功能：根据质量分对图片进行排序
#函数输入：id_list
#函数输出：返还排序后图片
##########################
def sort_list(id_list):
    id_pic_list = []
    id_list = sorted(id_list,key=lambda x:x[0],reverse=True)
    for id in id_list:
        id_pic_list.append(id[1])
    return id_pic_list

##########################
#函数功能：获取id路径下所有的图片路径
#函数输入：id_path
#函数输出：返还图片列表
##########################
def get_id_pic_list(id_path):
    id_pic_list = []

    for id_path_next in os.listdir(id_path):
        if not id_path_next.endswith(".jpg"):
            continue
        score = int(id_path_next.split(".")[0].split("_")[-2])
        id_pic_list.append([score,id_path_next])
    return id_pic_list
###########################
#函数功能：获取聚类结果文件路径
#函数输入：聚类打分文件存储路径
#函数输出：返还聚类结果文件的绝对路径
###########################
def get_cluster_path(score_path):
    for score_path_next in os.listdir(score_path):
        if "id_cluster" not in score_path_next:
            continue
        id_cluster_info_path = os.path.join(score_path,score_path_next)
    return id_cluster_info_path
###########################
#函数功能：分析依图聚类文件
#函数输入：聚类信息存储地址，聚类文件存放路径,id对应的搜索范围
#函数输出: 无
###########################
def get_cluster_result(score_path,result_id_path,cluster_id_search_range_list,cut_pic_name,cluster_id_name,IPC_check):
    id_cluster_info_path = get_cluster_path(score_path)
    id_cluster_info_handle = open(id_cluster_info_path,"r")
    lines = id_cluster_info_handle.readlines()
    id_cluster_info_handle.close()
    #获取tag列表及对应的绝对路径
    cluster_item_tag_abpath_list = []
    for line in lines:
        line = line.strip("\n")
        cluster_item_tag = line.split("@")[-1]

        if cluster_item_tag == "-1":
            continue

        tmp_path = line.split("@")[0]
    #print tmp_path,cut_pic_name,cluster_id_name
        if cut_pic_name in tmp_path:
            cluster_item_abpath = tmp_path.split("#")[0]
        elif cluster_id_name in tmp_path:
            tmp_path = tmp_path.replace("#", "/")
            cluster_item_abpath = tmp_path
        else:
            print "no found!"
        cluster_item_tag_abpath_list.append([cluster_item_tag,cluster_item_abpath])
    #获取tag列表
    all_tag_list = []
    for cluster_item_tag in cluster_item_tag_abpath_list:
        if cluster_item_tag[0] not in all_tag_list:
            all_tag_list.append(cluster_item_tag[0])

    judeg_id_list(all_tag_list, cluster_item_tag_abpath_list, result_id_path,cut_pic_name,cluster_id_name,IPC_check)

###########################
#函数功能：根据输入信息，完成所有聚类结果文件的拷贝
#函数输入：all_tag_list, cluster_item_tag_abpath_list, result_id_path
#函数输出：暂无
###########################
def judeg_id_list(all_tag_list,cluster_item_tag_abpath_list,result_id_path,cut_pic_name,cluster_id_name,IPC_check):
    cp_list = []
    fun_var = []
    for tag in all_tag_list:
        flag = 0
        id_term = ""
        result_list = my_finds(tag, 0, cluster_item_tag_abpath_list)
        cluster_id_name_flag = 0
        cut_pic_name_flag = 0
        ipc_num_flag = 0
        for result_item in result_list:
            if cluster_id_name_flag == 0:
                if cluster_id_name not in result_item[1]:#判断身份信息是否聚类成功
                    continue
                else:
                    id_term = result_item[1].split("/")[-1].split(".")[0]
                    cluster_id_name_flag = 1
            '''
            if ipc_num_flag == 0:
                ipc_num = result_item[1].split("/")[-2].split("_")[0]
                if ipc_num not in IPC_check:
                    continue
                else:
                    ipc_num_flag = 1
            '''
            if cut_pic_name_flag == 0:
                if cut_pic_name not in result_item[1]:#判断是否包含其他摄像头信息
                    continue
                else:
                    cut_pic_name_flag = 1

            if not os.path.exists(os.path.join(result_id_path,id_term)):
                print "mkdir",os.path.join(result_id_path,id_term)
                os.mkdir(os.path.join(result_id_path,id_term))
            flag = 1
            break

        if flag == 1:
            for result_item in result_list:
                if cluster_id_name in result_item[1]:
                    json_path = result_item[1].split(".")[0] + ".json"
                    print result_item[1]
                    print json_path
                    print os.path.join(result_id_path,id_term,id_term + ".jpg")
                    print os.path.join(result_id_path,id_term,id_term + ".json")
                    #shutil.copyfile(result_item[1],os.path.join(result_id_path,id_term,id_term + ".jpg"))
                    cp_list.append([result_item[1],os.path.join(result_id_path,id_term,id_term + ".jpg")])
                    cp_list.append([json_path,os.path.join(result_id_path,id_term,id_term + ".json")])
                else:
                    for img in os.listdir(result_item[1]):
                        img_path = os.path.join(result_item[1], img)
                        print img_path
                        print os.path.join(result_id_path, id_term, img)
                        #shutil.copyfile(img_path,os.path.join(result_id_path, id_term, img))
                        cp_list.append([img_path,os.path.join(result_id_path, id_term, img)])

    for i in range(0,len(cp_list)):
        cpfile_A = cp_list[i][0]
        cpfile_B = cp_list[i][1]
        fun_var.append(([cpfile_A,cpfile_B,i,len(cp_list)-1],None))
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(cp_exec, fun_var)
    [pool.putRequest(req) for req in requests]
    pool.wait()

def cp_exec(cpfile_A,cpfile_B,i,all_num):
    shutil.copyfile(cpfile_A,cpfile_B)
    print u"进度:",str(i) + "/" + str(all_num)


def do_cluster(base_path, cwd, log_path):
    #######################
    #变量定义区
    #######################
    #定义debug开关
    debug = True
    #定义人证合一卡口对应IPC命名范围
    IPC_check = ["IPC1","IPC2","IPC3","IPC4","IPC5","IPC6","IPC7","IPC8","IPC9","IPC10","IPC11","IPC12"]
    #定义基本文件目录
    # base_path = r"/home/z00355208/proc_data_pro"
    #定义配置文件路径
    config_file_path = os.path.join(base_path,"config.txt")
    #定义截图文件存放路径
    cut_pic_name = "output"
    cut_pic_path = os.path.join(base_path,cut_pic_name)
    #定义爬图身份文件存放路径
    cluster_id_name = "identity"
    cluster_id_path = os.path.join(base_path,cluster_id_name)
    #定义票务信息存放存放路径
    cluster_ticket_name = "ticket"
    cluster_ticket_path = os.path.join(base_path,cluster_ticket_name)
    #定义结果存放文件
    result_id_name = "result"
    result_id_path = os.path.join(base_path, result_id_name)
    #聚类相关信息
    score_path = os.path.join(base_path,"score")
    #planB,构造id_score文件夹
    id_score_path = os.path.join(score_path,"id_score.txt")
    #定义聚类脚本位置
    yitu_cluster_path = '/home/kklt/train'
    ########################
    #文件夹预处理
    ########################
    if not os.path.exists(cut_pic_path):
        print u"文件id_data_cut不存在"
    if not os.path.exists(cluster_id_path):
        print u"文件id_data_cluster不存在"
    if not os.path.exists(cluster_ticket_path):
        print u"文件id_data_ticket不存在"

    if os.path.exists(result_id_path):
        shutil.rmtree(result_id_path)
    if not os.path.exists(result_id_path):
        os.mkdir(result_id_path)

    if os.path.exists(score_path):
        shutil.rmtree(score_path)
    if not os.path.exists(score_path):
        os.mkdir(score_path)
    ########################
    #函数调用区
    ########################
    ##调用票务信息存储函数
    print u"正在获取票务信息列表"
    ticket_struct_info_days_list = get_ticket_struct_info_days(cluster_ticket_path)
    print u"成功获取票务信息列表"
    ##调用截图id信息存储函数
    print u"正在获取截图信息列表"
    cut_id_struct_info_list = get_cut_id_struct_info(cut_pic_path)
    print u"成功获取截图信息列表"
    ##调用获取聚类信息获取文件
    print u"正在获取查询id信息列表"
    cluster_id_struct_info_list = get_cluster_id_struct_info(cluster_id_path)
    print u"成功获取查询id信息列表"
    #获取每个id对应的搜索范围
    print u"正在获取查询id搜索范围"
    cluster_id_search_range_list = get_cluster_id_range(cluster_id_struct_info_list, ticket_struct_info_days_list, cut_id_struct_info_list, IPC_check)
    print u"成功获取查询id搜索范围"
    #写打分文件用于聚类
    print u"正在获取打分文件"
    creat_file_to_cluster(id_score_path, cut_id_struct_info_list, cluster_id_struct_info_list)
    print u"成功获取打分文件"
    #调用依图聚类算法
    print u"正在执行依图聚类程序"
    cmd = " ".join(["./do_cluster.sh",id_score_path,"85"])
    kwargs = {'cwd': cwd}
    utils.exec_command(cmd, log_path, **kwargs)
    # subprocess.call(cmd, shell=True, cwd=cwd)
    print u"成功执行依图聚类程序"
    #分析依图聚类结果
    print u"正在获取最终结果"
    get_cluster_result(score_path, result_id_path, cluster_id_search_range_list, cut_pic_name, cluster_id_name,IPC_check)
    print u"成功获取最终结果"
    if debug == False:
        sava_file_path = "ticket_id_file.txt"
        write_2d_list(ticket_struct_info_days_list, sava_file_path)

        sava_file_path = "cut_id_file.txt"
        write_2d_list(cut_id_struct_info_list, sava_file_path)

        sava_file_path = "cluster_id_file.txt"
        write_2d_list(cluster_id_struct_info_list, sava_file_path)

        sava_file_path = "cluster_id_search_range_file.txt"
        write_2d_list(cluster_id_search_range_list, sava_file_path)


if __name__ == '__main__':
    do_cluster('/home/data/test/cluster')
