# -*- coding: UTF-8 -*-
# data analysis
# sft data 后处理

import pandas as pd


def mean_ana_two_csv(oricsv, newcsv, acc_c0l):
    # 对比两个csv 文件  
    # acc_c0l 第几列是 acc
    oripd = pd.read_csv(oricsv)
    newpd = pd.read_csv(newcsv)
    print(f"head of csv file \n{oripd.head(12)}\n\n")
    print("________________")
    print(f"head of csv file \n{newpd.head(12)}\n\n")
    a = oripd['dataset'].str.contains('ceval', case=False, na=False)
    filtered_ori = oripd[oripd['dataset'].str.contains('ceval', case=False, na=False)] 
    print(f"{len(filtered_ori)} of task was hit")
    filtered_new = newpd[newpd['dataset'].str.contains('ceval', case=False, na=False)] # ceval  mmlu

    ori_average_value = filtered_ori.iloc[:, acc_c0l]
    new_average_value = filtered_new.iloc[:, acc_c0l]
    print(f"ori ppl: {ori_average_value.mean()}\nnew ppl: {new_average_value.mean()}")
    print("mean_ana_two_csv end")


if __name__ == '__main__':
    oricsv = "/home/centos/mkl/project/opencompass_main/outputs/default/20231212_104222_ceval_ppl_ori7bchat/summary/summary_20231212_104222.csv"
    newcsv = "/home/centos/mkl/project/opencompass_main/outputs/default/20231212_162836_ceval_ppl_sftmodel/summary/summary_20231212_162836.csv"
    dpocsv = "/data/mkl/project/opencompass_main/outputs/default/20231214_175736/summary/summary_20231214_175736.csv"
    acc_c0l = 4
    mean_ana_two_csv(oricsv, newcsv, acc_c0l)
    # mean_ana_two_csv(oricsv, dpocsv, acc_c0l)
print("_end success")