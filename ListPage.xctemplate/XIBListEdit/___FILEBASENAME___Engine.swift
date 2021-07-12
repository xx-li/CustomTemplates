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

extension Notification.UserInfoKey {
    static var ___VARIABLE_moduleName___DidChangedNotificationBehaviorKey: Notification.UserInfoKey<___VARIABLE_moduleName___Engine.ChangeBehavior> {
        return Notification.UserInfoKey(key: "com.tingdao.app.___VARIABLE_moduleName___DidChangedNotification.ChangeBehavior")
    }
}

final class ___VARIABLE_moduleName___Engine {

    // MARK: - 枚举定义 -
    
    enum ChangeBehavior {
        case add([Int])
        case remove([Int])
        case edit([Int])
        case reload
    }
    
    enum RequestBehaviorType {
        case add
        case delete
        case edit
    }


    // MARK: - 数据处理 -

    static func diff(original: [___VARIABLE_moduleName___Model], now: [___VARIABLE_moduleName___Model]) -> ChangeBehavior {
        if original.count == 0 {
            return .reload
        }
        
        let originalSet = Set(original)
        let nowSet = Set(now)

        if originalSet.isSubset(of: nowSet) { // Appended
            let added = nowSet.subtracting(originalSet)
            let indexes = added.compactMap { now.firstIndex(of: $0) }
            return .add(indexes)
        } else if (nowSet.isSubset(of: originalSet)) { // Removed
            let removed = originalSet.subtracting(nowSet)
            let indexes = removed.compactMap { original.firstIndex(of: $0) }
            return .remove(indexes)
        } else { // Both appended and removed
            return .reload
        }
    }

    func operation(behaviorType: RequestBehaviorType, model: ___VARIABLE_moduleName___Model) {
        switch behaviorType {
        case .add:
            totoalCount += 1
            datas.insert(model, at: 0)
        case .delete:
            if let index = datas.firstIndex(of: model) {
                totoalCount -= 1
                datas.remove(at: index)
            }
        case .edit:
            if let index = datas.firstIndex(of: model) {
                datas.remove(at: index)
            }
        }
    }

    //swift array 的元素变化也会触发didSet方法
    private(set) var datas: [___VARIABLE_moduleName___Model] = [] {
        didSet {
            let behavior = ___VARIABLE_moduleName___Engine.diff(original: oldValue, now: datas)
            NotificationCenter.default.post(
                name: .___VARIABLE_moduleName___DidChangedNotification,
                object: self,
                typedUserInfo: [.___VARIABLE_moduleName___DidChangedNotificationBehaviorKey: behavior]
            )
        }
    }


    // MARK: - 请求接口数据 -

    private(set) var totoalCount = 0
    //从第1页开始，下一页下标初始化就是2
    private(set) var nextPage = 2
    
    func requestList(isLoadMore: Bool, complete: ((_ isSuccess: Bool, _ msg: String?)->(Void))?) -> DTBaseRequest {
        let curPage = isLoadMore ? nextPage : 1
        let request = ___VARIABLE_moduleName___ListRequest.init(nextPage: curPage, pageCount: 15)
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
        
        return request
    }

    func requestOperationList(behaviorType: RequestBehaviorType,
                              model: ___VARIABLE_moduleName___Model,
                              operationAfterRequest: Bool = true,
                              complete: ((_ isSuccess: Bool, _ msg: String?)->(Void))?) {
        if operationAfterRequest == false {
            self.operation(behaviorType: behaviorType, model: model)
        }
        let request = ___VARIABLE_moduleName___OperationRequest.init(behaviorType: behaviorType, model: model)
        request.start { [weak self] (res, err) in
            guard let self = self else { return }
            guard res.errorDes == nil else {
                if let complete = complete {
                    complete(false, res.errorDes)
                }
                return
            }

            var flag = false
            if let biz = request.biz as? Dictionary<String, Any>,
                let _ = biz["status"] as? String {
                flag = true
                if operationAfterRequest == true {
                    self.operation(behaviorType: behaviorType, model: model)
                }
            }
            
            if let complete = complete {
                complete(flag, flag ? "请求并解析成功" : "数据格式错误，解析失败！")
            }
        }
    }
    
    func isCanLoadMore() -> Bool {
        return self.datas.count < totoalCount;
    }
}
