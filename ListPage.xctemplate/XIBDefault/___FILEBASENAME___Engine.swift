//
//  ___FILENAME___
//  ___PROJECTNAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  Copyright (c) ___YEAR___ ___ORGANIZATIONNAME___. All rights reserved.
//
//  This file was generated by ListPage Templates
//

import Foundation

extension Notification.Name {
    static let ___VARIABLE_moduleName___DidChangedNotification = Notification.Name(rawValue: 
        "com.tingdao.app.___VARIABLE_moduleName___DidChangedNotification")
}

final class ___VARIABLE_moduleName___Engine {

    // MARK: - 数据处理 -

    //swift array 的元素变化也会触发didSet方法
    private(set) var datas: [___VARIABLE_moduleName___Model] = [] {
        didSet {
            let behavior = ___VARIABLE_moduleName___Engine.diff(original: oldValue, now: datas)
            NotificationCenter.default.post(
                name: .___VARIABLE_moduleName___DidChangedNotification,
                object: self
            )
        }
    }


    // MARK: - 请求接口数据 -

    private(set) var totoalCount = 0
    //从第1页开始，下一页下标初始化就是2
    private(set) var nextPage = 2
    
    func requestList(isLoadMore: Bool, complete: ((_ isSuccess: Bool, _ msg: String?)->(Void))?) -> DTBaseRequest {
        let curPage = isLoadMore ? nextPage : 1
        let request = ___VARIABLE_moduleName___Request.init(nextPage: curPage, pageCount: 15)
        request.start { [weak self] (res, err) in
            guard let self = self else { return }
            guard res.errorDes == nil else {
                if let complete = complete {
                    complete(false, res.errorDes)
                }
                return
            }

            let decoder = JSONDecoder()
            var flag = false
            // 拿到列表数据和列表大小
            if let biz = request.biz as? Dictionary<String, Any>,
                let jsonList = biz["list"] ,
                let listData = try? JSONSerialization.data(withJSONObject: jsonList, options: []),
                let list = try? decoder.decode([___VARIABLE_moduleName___Model].self, from: listData),
                let totoalCount = biz["totoalCount"] as? Int {
                
                if !isLoadMore { self.datas.removeAll() }
                self.nextPage = isLoadMore ? self.nextPage + 1 : 2
                self.totoalCount = totoalCount
                self.datas.append(contentsOf: list)
                flag = true
            }
            
            if let complete = complete {
                complete(flag, flag ? "请求并解析成功" : "数据格式错误，解析失败！")
            }
        }
        
        return api
    }
    
    func isCanLoadMore() -> Bool {
        return self.datas.count < totoalCount;
    }
}