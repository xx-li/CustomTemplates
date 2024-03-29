//
//  ___FILENAME___
//  ___PROJECTNAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  Copyright (c) ___YEAR___ ___ORGANIZATIONNAME___. All rights reserved.
//
//  This file was generated by MGDT Templates
//

import UIKit

final class ___VARIABLE_moduleName___ViewController: DTBaseViewController {

    // MARK: - properties -

    

    

    

    let engine = ___VARIABLE_moduleName___Engine.init()

    // MARK: - Lifecycle -

    override func viewDidLoad() {
        super.viewDidLoad()

        
        

        requestData()

        NotificationCenter.default.addObserver(
            self,
            selector: #selector(datasDidChange),
            name: .___VARIABLE_moduleName___DidChangedNotification,
            object: nil
        )
    }

    
    // MARK: - request -

    @objc func requestData() {
        view.dt_hiddenAllEmpty()
        self.dt_request = engine.requestData() { [weak self] (isSuccess, msg) in
            guard let self = self else { return }
            if !isSuccess {
                self.view.dt_showNetworkError(
                    withTarget: self,
                    action: #selector(self.requestData)
                )
                QMUITips.show(withText: msg)
                return
            }
            
            //TODO: 更新UI
        }
    }

    
    // MARK: - Data sync -
    
    @objc func datasDidChange(_ notification: Notification) {
        let behavior = notification.getUserInfo(
            for: .___VARIABLE_moduleName___DidChangedNotificationBehaviorKey
        )
        self.syncDataToUI(for: behavior)
    }

    // MARK: - UI -
    
    func syncDataToUI(for behavior: ___VARIABLE_moduleName___Engine.ChangeBehavior) {
        //TODO: update page UI
    }


    
}

