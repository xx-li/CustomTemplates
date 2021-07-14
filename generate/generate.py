# -*- coding: utf-8 -*-
# @Time    : 2021/7/12 下午5:00
# @Author  : 李新星
# @Site    : 
# @File    : generate.py


## 功能
# 生成6种Xcode模板

# 1. 无列表无xib
# 2. 无列表有xib
# 3. 有列表无xib
# 4. 有列表有xib
# 5. 有列表有操作无xib
# 6. 有列表有操作有xib

# 1. 列表相关代码动态创建。
# 2. 操作相关代码动态创建。
# 3. xib相关文件动态创建。


import os
from common import TemplateType
import replace_vc
import replace_engine
import replace_cell

output_path = "../Page.xctemplate"

template_path = "./template"
vc_name = "___FILEBASENAME___ViewController.swift"
vc_xib_name = "___FILEBASENAME___ViewController.xib"
engine_name = "___FILEBASENAME___Engine.swift"
cell_name = "___FILEBASENAME___ListCell.swift"
cell_xib_name = "___FILEBASENAME___ListCell.xib"

request_name = "___FILEBASENAME___Request.swift"
list_request_name = "___FILEBASENAME___ListRequest.swift"
operation_request_name = "___FILEBASENAME___OperationRequest.swift"
model_name = "___FILEBASENAME___Model.swift"

def creatTemplate(name, templateType, path, callback):
    # 1. 读取原生模板信息,并修改原生模板为xcode模板文件
    f = open(os.path.join(template_path, name))
    vcStr = f.read()
    f.close()
    vc_res = callback(vcStr, templateType)
    
    if vc_res != None:
        # 2. 新生成的文件写入到指定目录
        wf = open(os.path.join(path, name), mode='w')
        wf.write(vc_res)
        wf.close()


def replaceRequest(str, type):
    if "List" in type.value:
        return None
    else:
        return str

def replaceListRequest(str, type):
    if "List" in type.value:
        return str
    else:
        return None

def replaceOperationRequest(str, type):
    if "Edit" in type.value:
        return str
    else:
        return None

def replaceModel(str, type):
    return str


for name, templateType in TemplateType.__members__.items():
    name = templateType.value
    print(name, '=>', templateType)
    # 1. 创建模板目录并清空之前老的内容
    path = os.path.join(output_path, name)
    os.makedirs(path, exist_ok=True)
    for subFile in os.listdir(path):
        p = os.path.join(path, subFile)
        os.remove(p)

    # testcreatTemplate(vc_name, templateType, path, replace_vc.replace)

    # 创建VC模板
    creatTemplate(vc_name, templateType, path, callback=replace_vc.replace)
    creatTemplate(vc_xib_name, templateType, path, callback=replace_vc.replaceXib)

    # 创建engine模板
    creatTemplate(engine_name, templateType, path, callback=replace_engine.replace)

    # 创建cell模板
    creatTemplate(cell_name, templateType, path, callback=replace_cell.replace)
    creatTemplate(cell_xib_name, templateType, path, callback=replace_cell.replaceXib)

    # 创建request模板
    creatTemplate(request_name, templateType, path, callback=replaceRequest)

    # 创建list request模板
    creatTemplate(list_request_name, templateType, path, callback=replaceListRequest)

    # 创建operation request模板
    creatTemplate(operation_request_name, templateType, path, callback=replaceOperationRequest)

    # 创建model模板
    creatTemplate(model_name, templateType, path, callback=replaceModel)
    

