//
//  ___FILENAME___
//  ___PROJECTNAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  Copyright (c) ___YEAR___ ___ORGANIZATIONNAME___. All rights reserved.
//
//  This file was generated by ListPage Templates
// 
//  

import Foundation

/// ___VARIABLE_moduleName___OperationRequest
/// 接口文档地址：
/// 接口文档参数说明：
final class ___VARIABLE_moduleName___Request: DTBaseRequest {

    private(set) var nextPage: Int
    private(set) var pageCount: Int
    
    required init(nextPage: Int, pageCount: Int) {
        self.nextPage = nextPage
        self.pageCount = pageCount
        super.init()
    }
    
    override func requestUrl() -> String {
        return ""
    }
    
    override func requestArgument() -> Any? {
        var argument = [String: Any]()
        argument["offset"] = String(nextPage)
        argument["count"] = String(pageCount)
        return packageRequestArgument(argument)
    }
    
    // override func requestMethod() -> YTKRequestMethod {
    //     return .POST
    // }
    
    // override func requestTimeoutInterval() -> TimeInterval {
    //     return TimeInterval(15)
    // }
}


/// ___VARIABLE_moduleName___OperationRequest
/// 接口文档地址：
/// 接口文档参数说明：
final class ___VARIABLE_moduleName___OperationRequest: DTBaseRequest {
    private(set) var behaviorType: ___VARIABLE_moduleName___Engine.RequestBehaviorType
    private(set) var model: ___VARIABLE_moduleName___Model
    
    required init(behaviorType: ___VARIABLE_moduleName___Engine.RequestBehaviorType,
                  model: ___VARIABLE_moduleName___Model) {
        
        self.behaviorType = behaviorType
        self.model = model
        super.init()
    }
    
    override func requestUrl() -> String {
        switch behaviorType {
        case .add:
            return ""
        case .delete:
            return ""
        case .edit:
            return ""
        }
    }
    
    override func requestArgument() -> Any? {
        var argument = [String: Any]()
        
//        argument["cid"] = model.cid
//        switch behaviorType {
//        case .add:
//            //TODO: add args
//        case .delete:
//            //TODO: add args
//        case .edit:
//            //TODO: add args
//        }
        
        return packageRequestArgument(argument)
    }
    
    // override func requestMethod() -> YTKRequestMethod {
    //     return .POST
    // }
    
    // override func requestTimeoutInterval() -> TimeInterval {
    //     return TimeInterval(15)
    // }
}
